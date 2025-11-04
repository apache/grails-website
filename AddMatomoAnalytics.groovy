// Define the Matomo tracking code to insert
def matomoCode = '''    <!-- Matomo -->
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

// Get the current directory
def currentDir = new File('.')

// Find all .html and .htm files recursively
def htmlFiles = []
currentDir.eachFileRecurse { file ->
    if (file.name.endsWith('.html') || file.name.endsWith('.htm')) {
        htmlFiles << file
    }
}

println "Found ${htmlFiles.size()} HTML files"

// Process each file
htmlFiles.each { file ->
    def content = file.text

    // Check if Matomo code already exists
    if (content.contains('<!-- Matomo -->') || content.contains('matomo.js')) {
        println "Skipping ${file.name} - Matomo code already present"
        return
    }

    def updatedContent

    // Check if file has a closing </head> tag
    // Insert Matomo code before </head>
    if (content.contains('</head>')) {
        updatedContent = content.replaceFirst('</head>', "${matomoCode}\n</head>")
    } else if (content.contains('</HEAD>')) {
        updatedContent = content.replaceFirst('</HEAD>', "${matomoCode}\n</HEAD>")
    } else {
        println "Skipping ${file.name} - No </head> tag found"
        return
    }

    // Write the updated content back to the file
    file.write(updatedContent)
    println "Updated ${file.name}"
}

println "Processing complete!"