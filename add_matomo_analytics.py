#!/usr/bin/env python3
"""
Add Apache Analytics (Matomo) tracking to historical documentation pages.
This script injects Matomo tracking code into HTML files that are missing analytics.
"""

import os
import re
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

# Matomo tracking code to be inserted before </head>
MATOMO_CODE = '''    <!-- Matomo -->
    <script>
      var _paq = window._paq = window._paq || [];
      /* tracker methods like "setCustomDimension" should be called before "trackPageView" */
      _paq.push(["setDoNotTrack", true]);
      _paq.push(["disableCookies"]);
      _paq.push(['trackPageView']);
      _paq.push(['enableLinkTracking']);
      (function() {
        var u="https://analytics.apache.org/";
        _paq.push(['setTrackerUrl', u+'matomo.php']);
        _paq.push(['setSiteId', '79']);
        var d=document, g=d.createElement('script'), s=d.getElementsByTagName('script')[0];
        g.async=true; g.src=u+'matomo.js'; s.parentNode.insertBefore(g,s);
      })();
    </script>
    <!-- End Matomo Code -->
'''

# Directories containing historical documentation
DOC_DIRECTORIES = [
    'docs',
    'docs-legacy-async',
    'docs-legacy-gorm',
    'docs-legacy-gsp',
    'docs-legacy-testing',
    'docs-legacy-views',
]

# Patterns indicating Matomo is already present
MATOMO_PATTERNS = [
    '<!-- Matomo -->',
    'matomo.js',
    'analytics.apache.org'
]


def has_matomo_analytics(content):
    """Check if the file already contains Matomo analytics."""
    content_lower = content.lower()
    return any(pattern.lower() in content_lower for pattern in MATOMO_PATTERNS)


def process_html_file(filepath):
    """
    Process a single HTML file and add Matomo analytics if missing.
    Returns tuple: (filepath, status, message)
    """
    try:
        with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
            content = f.read()

        # Skip files that already have Matomo
        if has_matomo_analytics(content):
            return (filepath, 'skipped', 'Matomo already present')

        # Insert before </head> (case insensitive)
        head_pattern = re.compile(r'(</head>)', re.IGNORECASE)
        match = head_pattern.search(content)
        
        if match:
            updated_content = content[:match.start()] + MATOMO_CODE + '\n' + content[match.start():]
        # Try inserting before </HEAD> explicitly
        elif '</HEAD>' in content:
            updated_content = content.replace('</HEAD>', MATOMO_CODE + '\n</HEAD>')
        # For frameset pages, insert after opening <head> or <html>
        elif '<head>' in content.lower():
            head_open = re.compile(r'(<head[^>]*>)', re.IGNORECASE)
            head_match = head_open.search(content)
            if head_match:
                insert_pos = head_match.end()
                updated_content = content[:insert_pos] + '\n' + MATOMO_CODE + content[insert_pos:]
            else:
                return (filepath, 'skipped', 'No suitable insertion point found')
        else:
            return (filepath, 'skipped', 'No </head> tag found')

        # Write the updated content
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(updated_content)

        return (filepath, 'updated', 'Matomo analytics added')

    except Exception as e:
        return (filepath, 'error', str(e))


def find_html_files(base_path, directories):
    """Find all HTML files in the specified directories."""
    html_files = []
    
    for dir_name in directories:
        dir_path = Path(base_path) / dir_name
        if not dir_path.exists():
            print(f"Warning: Directory '{dir_name}' not found, skipping...")
            continue
            
        for filepath in dir_path.rglob('*.html'):
            html_files.append(filepath)
        for filepath in dir_path.rglob('*.htm'):
            html_files.append(filepath)
    
    return html_files


def main():
    """Main entry point for the script."""
    base_path = Path(__file__).parent
    
    print("=" * 60)
    print("Apache Analytics (Matomo) Injection Script")
    print("=" * 60)
    print()
    
    # Find all HTML files
    print("Scanning for HTML files in historical documentation...")
    html_files = find_html_files(base_path, DOC_DIRECTORIES)
    total_files = len(html_files)
    print(f"Found {total_files:,} HTML files to process")
    print()
    
    if total_files == 0:
        print("No HTML files found. Exiting.")
        return 0
    
    # Process files in parallel
    num_workers = min(os.cpu_count() or 4, 16)
    print(f"Processing files using {num_workers} parallel workers...")
    print()
    
    updated_count = 0
    skipped_count = 0
    error_count = 0
    processed = 0
    
    with ThreadPoolExecutor(max_workers=num_workers) as executor:
        futures = {executor.submit(process_html_file, f): f for f in html_files}
        
        for future in as_completed(futures):
            filepath, status, message = future.result()
            processed += 1
            
            if status == 'updated':
                updated_count += 1
            elif status == 'skipped':
                skipped_count += 1
            elif status == 'error':
                error_count += 1
                print(f"Error: {filepath} - {message}")
            
            # Progress indicator every 10000 files
            if processed % 10000 == 0:
                print(f"Progress: {processed:,}/{total_files:,} files processed...")
    
    # Summary
    print()
    print("=" * 60)
    print("Processing Complete!")
    print("=" * 60)
    print(f"Total files processed: {total_files:,}")
    print(f"Files updated:         {updated_count:,}")
    print(f"Files skipped:         {skipped_count:,}")
    print(f"Errors:                {error_count:,}")
    print()
    
    return 0 if error_count == 0 else 1


if __name__ == '__main__':
    sys.exit(main())
