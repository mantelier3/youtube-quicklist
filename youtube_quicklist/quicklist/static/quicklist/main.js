a = 5;
//$("#clickable_button").click(function () {
//    $("#clickable_button").text = "foobar"
//});
/*$(document).ready (function () {
    $("button#clickable_button").click(function () {
        $("#clickable_button").text("foo")
    });
});*/
$(document).ready(function () {
    $("#clickable_button").click(function () {
        $.ajax({
            url: "/quicklist/index",
            success: function (result) {
                alert(result);
                my_results = result;
            }
        });
    });
    // Search - query youtbe for search results and display new results
    $("#form_search").on("submit", function (event) {
        event.preventDefault();
        my_event = event;
        need_html_results = ($(".div_results").length === 0);
        $.ajax({
            url: "/quicklist/index",
            data: {query: $("#text_query").val(),
                    need_html_results: need_html_results},
            success: function (results) {
                //$("#test_p").text(results);
                js_results = JSON.parse(results).results;
                if (need_html_results) {
                    $("#div_results_container").append(js_results);
                }
                else {
                    thumbnail_urls = js_results.map(function (js_results) {
                        return js_results.thumbnail_url;
                    });
                    $(".div_results > img").each(function (index) {
                        $(this).attr("src", thumbnail_urls[index]);
                    });
                }
            }
        });
    });
    $(".btn_add").click(function () {
        $(this).data("clicked", true);
    });
    // Add - add video to playlist
    $("#form_add").on("submit", function (event) {
        event.preventDefault();
        my_event = event;
        video_index = $(".btn_add").filter( function () {
            return $(this).data("clicked") === true 
        } ).val()
        $(".btn_add").data("clicked", false);
        $.ajax({
            url: "/quicklist/add",
            data: {add_video_index: video_index},
            success: function (results) {
                js_playlist = JSON.parse(results);
                $("#form_playlist").append(js_playlist)
            }
        });
    });
});
