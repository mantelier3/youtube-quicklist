// sets callback for removing a video from playlist
function set_btn_remove_callback(button_list) {
    console.log("removecb "+button_list);
    button_list.on("click", function (event) {
        console.log("clicked btn-remove number "+event.target.value);
        my_event = event;
        event.preventDefault();
        // console.log("button is " + event.target.id);
        $.ajax({
            url: "/quicklist/remove/"+event.target.value,
            // data: {video_index_remove: event.target.value},
            success: function (position) {
                $(event.target).parent().remove();
                $(".btn_remove").each(function(index) {
                    if(index >= position){
                        console.log($(this));
                        $(this).attr("id",$(this).attr("id").replace(/.$/, function(x) {return x-1})); 
                        $(this).attr("value", $(this).val() - 1); 
                    }
                });
                // postrihaj indexe v html in django
            }
        });
    }); 
}
var results1;
// var new_playlist_item;
function set_btn_add_callback(button_list) {
    console.log("addcb "+button_list);
    button_list.on("click", function (event) {
        console.log("clicked btn-add number "+event.target.value)
        event.preventDefault();
        my_event = event; 
        $.ajax({
            // to position X add video Y from search results, -1 means at end
            url: "/quicklist/add/"+$(".btn_remove").length+"/"+event.target.value,
            // data: {video_index_add: event.target.value},
            success: function (results) {
                parsed_json = JSON.parse(results);
                rendered_item = parsed_json.rendered_item;
                position = parsed_json.position;
                results1=results;
                // console.log(results)
                // new_playlist_item = $(js_playlist)
                // console.log("new_playlist_item" + new_playlist_item)
                // console.log("!asdf");
                // console.log(asdf);
                $("#form_playlist").append(rendered_item);
                // set_btn_remove_callback(new_playlist_item.children("button"));
                set_btn_remove_callback($("#btn_remove_"+position));
                console.log("inner callback")
                // asdf.attr("id","foobar222");
            }
        });
    });
}

$(document).ready(function () {
    
    set_btn_remove_callback($(".btn_remove"));
    set_btn_add_callback($(".btn_add"));





    //move js from template to here
    //fix positioning when there is no video



    // Search - query youtube for search results and display new results
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

    // plays next video in playlist
    $("#btn_next").click( function() {
        $.ajax({
            url: "/quicklist/next_video",
            data: {},
            success: function (results) {
                new_video_id = JSON.parse(results);
                player.loadVideoById(new_video_id);
            }
        });
    });


    // console.log("foo")
    // display_video_player();
    // console.log("bar")
    // Add - add video to playlist

});




// function mark_buttons_as_clicked_when_clicked() {
//     $(".btn_add").click(function () {
//         $(this).data("clicked", true);
//     });
// }

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