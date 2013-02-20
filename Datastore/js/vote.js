var app = app || {}; // application namespace

/**
 * Cast a vote via Ajax. Updates vote total.
 * articleId - article to vote for
 * vote - type of vote to cast (up/down)
 */
app.vote = function(articleId, vote) {
   if(vote != "up" && vote != "down") { // sanity check
       throw new Exception('"vote" must be "up" or "down"');
   }

    $.post("/vote/" + articleId, '{"vote": "' + vote +'"}')
        .done(function(data){ // success callback
            // find article count element
            var voteCount = $("#" + data.article + " .vote-count");
            // set new vote count
            voteCount.text(data.votes);
        });
}

/**
 * Extract an articleId from vote element
 * el - element from which to extract article id
 * returns articleId as extracted from element
 */
app.getArticleId = function(el) {
    var path = $(el).attr("href");
    return path.match(/\d+$/);
}

/**
 * Bind to events
 */
$(function() {
   $(".vote .up").click(function() {
       app.vote(app.getArticleId(this), "up");
       return false;
   });

   $(".vote .down").click(function() {
       app.vote(app.getArticleId(this), "down");
       return false;
   });
});
