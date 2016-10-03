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






    //move js from template to here
    //fix positioning when there is no video










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
                    $("#form_add").append(js_results);
                    mark_buttons_as_clicked_when_clicked();
                } else {
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

    ajax_form_add_video();
    mark_buttons_as_clicked_when_clicked();
    // console.log("foo")
    // display_video_player();
    // console.log("bar")
    // Add - add video to playlist

});

function ajax_form_add_video() {
    $("#form_add").on("submit", function (event) {
        console.log("form add submit ajax")
        event.preventDefault();
        my_event = event;
        add_video_index = $(".btn_add").map( function (i, el) { 
            if ($(el).data("clicked")) { return i } 
        });
        console.log(add_video_index);
        if (add_video_index.length != 1) {
            alert("error, more or less than one button clicked, but not one")
        }
        $(".btn_add").data("clicked", false);
        console.log("foobar1234")   
        $.ajax({
            url: "/quicklist/add",
            data: {add_video_index: add_video_index[0]},
            success: function (results) {
                js_playlist = JSON.parse(results);
                $("#form_playlist").append(js_playlist);

            }
        });
    });
}

function mark_buttons_as_clicked_when_clicked() {
    $(".btn_add").click(function () {
        $(this).data("clicked", true);
    });
}

// function display_video_player(){
//     //2. This code loads the IFrame Player API code asynchronously.
//     var tag = document.createElement('script');
//     console.log("asdf")
//     tag.src = "https://www.youtube.com/iframe_api";
//     var firstScriptTag = document.getElementsByTagName('script')[0];
//     firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);
//     //$("div#player").append(tag);

//     // 3. This function creates an <iframe> (and YouTube player)
//     //    after the API code downloads.
//     var player;
//     function onYouTubeIframeAPIReady() {
//         player = new YT.Player('player', {
//             height: '200', // 390
//             width: '320', // 640
//             videoId: "-tL91n51K9k",
//             events: {
//             //'onReady': onPlayerReady,
//             'onStateChange': onPlayerStateChange
//             }
//         });
//     }

//     // 4. The API will call this function when the video player is ready.
//     function onPlayerReady(event) {
//         event.target.playVideo();
//     }

//     // 5. The API calls this function when the player's state changes.
//     var done = false;
//     function onPlayerStateChange(event) {
//         if (event.data == 0) {
//             window.location.href = "next_video"
//         }
//     }
//     function stopVideo() {
//         player.stopVideo();
//     }
// }