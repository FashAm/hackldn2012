############################
# CSS and JS dependencies  #
############################

# CSS Dependencies.
css_deps = ("css", "css",
            [
              ("/circles/*", ["joanna.css", "circles.css"]),  
              ("/trending", ["trending.css"]),
              ("/", ["joanna.css"])

            ])

# JS Dependencies.
js_deps = ("js", "js",
            [
             ("/circles/*", ["circles.js", "fb.js", "bootstrap-tooltip.js"]),
             ("/", ["joanna.js", "fb.js"]),	
	    ])

