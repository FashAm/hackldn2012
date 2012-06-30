/**
 * @fileOverview This file contains all the JavaScript functionality for the home page.
 * 
 * @author l </a>
 */


    // =============================== Listeners =============================== //
    
    
    
 function ajaxFileUpload(handler)
    {
        var settings = {
                url: "/u/settings/ppic",
                secureuri: false,
                data: {"_xsrf": CYP.xsrf},
                fileElementId: "ppic-upload",
                dataType: "json",
                success: function(response) {
                    if (_loader) {
                        _loader.hide();
                    }
                    _requestCompleted = true;
                    if (response === "ok") {
                        response['s'] = true;
                        changeSuccess(handler, {s: true});
                    } else {
                        var r = {s: true,
                                 err: response.split(",")[1]};
                        changeErr(handler, r);
                    } 
                },
                error: function(response) {
                    if (_loader) {
                        _loader.hide();
                    }
                    _requestCompleted = true;
                    changeErr(handler, response);
                }
        };
        _loader = $("#loader");
        if (_loader.length > 0 && !_loader.is(":visible")) {
            window.setTimeout(function(){
                if (!_requestCompleted) {
                    _loader.show();
                }
            }, 200);
        }
        _request_completed = false;
        $.ajaxFileUpload(settings);
        return false;
    }    



