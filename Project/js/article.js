var app = app || {}; // application namespace

app.isValidUrl = function(url) {
    return url.match(/^https?:\/\//i);
};

/**
 * Bind to events
 */
$(function() {
    // Checks if link_url is a valid url
   $("textarea[name='link_url']").blur(function(e) {
       var url = $("textarea[name='link_url']").val();   
       var errorNode = $(".error");
       var submitButton = $("#post-article input[type='submit']");

       if(!app.isValidUrl(url)) {
           submitButton.attr("disabled", "disabled");
           if(errorNode.children().length == 0) {
               errorNode.append("<p>Please enter a valid url " +
                                   "(http://www.ex.com)</p>");
           }
           errorNode.show();
       }
       else {
           submitButton.removeAttr("disabled");
           errorNode.hide();
           errorNode.empty();
       }
   });
});
