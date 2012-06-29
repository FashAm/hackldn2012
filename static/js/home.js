/**
 * @fileOverview This file contains all the JavaScript functionality for the home page.
 * 
 * @author l </a>
 */


    // =============================== Listeners =============================== //
    
    
    
    $("#btnSearch2").live("click", function() {
        var txt = $("#txtSearch").attr("value");
        CYP.post("/timeline", {
            keywords: txt
        }, true, function(response) {
            if (response.s) {
	 	CYP.successNotifier.show(response.feed);

            }
        });
    });
    
    



