@Grab(group='org.codehaus.gpars', module='gpars', version='1.2.1')
import groovyx.gpars.GParsPool
import java.util.concurrent.atomic.AtomicInteger

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

// Thread-safe counters
def updatedCount = new AtomicInteger(0)
def skippedCount = new AtomicInteger(0)

// Get number of available processors
def numThreads = Runtime.runtime.availableProcessors()
println "Processing files using ${numThreads} threads with GPars..."

// Process files in parallel using GPars
GParsPool.withPool(numThreads) {
    htmlFiles.eachParallel { file ->
        try {
            def content = file.text

            // Check if Matomo code already exists
            if (content.contains('<!-- Matomo -->') || content.contains('matomo.js')) {
                synchronized(System.out) {
                    println "Skipping ${file.absolutePath} - Matomo code already present"
                }
                skippedCount.incrementAndGet()
                return
            }

            def updatedContent

            // Check if file has a closing </head> tag
            // Insert Matomo code before </head>
            if (content.contains('</head>')) {
                updatedContent = content.replaceFirst('</head>', "${matomoCode}\n</head>")
            } else if (content.contains('</HEAD>')) {
                updatedContent = content.replaceFirst('</HEAD>', "${matomoCode}\n</HEAD>")
            } else if (content.contains('<body class="center">')) {
                updatedContent = content.replaceFirst('<body class="center">', "${matomoCode}\n<body class=\"center\">")
            } else {
                synchronized(System.out) {
                    println "Skipping ${file.absolutePath} - No </head> tag found"
                }
                skippedCount.incrementAndGet()
                return
            }

            // Write the updated content back to the file
            file.write(updatedContent)
            synchronized(System.out) {
                println "Updated ${file.absolutePath}"
            }
            updatedCount.incrementAndGet()
        } catch (Exception e) {
            synchronized(System.out) {
                println "Error processing ${file.absolutePath}: ${e.message}"
            }
        }
    }
}

println "\nProcessing complete!"
println "Files updated: ${updatedCount.get()}"
println "Files skipped: ${skippedCount.get()}"
println "Total files processed: ${htmlFiles.size()}"
