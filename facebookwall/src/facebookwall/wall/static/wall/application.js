$(document).ready(function() {
    $('.edit').click(function() {
        var btn = this.value;
        //alert(btn);
        var p = $('p#'+btn);
        p.wrap(function() {
            return '<form action="" class="post-form" method="post"></form>';
        });

        p.replaceWith($("<textarea/>", {
            "class": "edit",
            "name": "message",
            "text": p.text().replace("\n", "").replace(/\s{2,}/g, " ").trim(),
            "css": { "width": p.css('width') }
        }));

          $("<input type='hidden' value='"+btn+"' />")
            .attr("id", "status_id")
            .attr("name", "status_id")
            .appendTo(".post-form");

        $('.edit').keypress(function (e) {
            if (e.which == 13) {
                $('.post-form').submit();
                return false;
            }
        });
        console.log($('.post-form'))

        $('.post-form').on('submit', function(e){
            e.preventDefault();
            console.log(this);
            edit_status(this);
            return false
        });

        function edit_status(status) {
            $.ajax({
                url : "edit_status/", // the endpoint
                type : "POST", // http method
                data : { status_id: status.status_id.value, message : status.message.value }, // data sent with the post request

                // handle a successful response
                success : function(json) {
                    var p = $('#edit-container-'+status.status_id.value);
                    p.html('<p id="'+ status.status_id.value +'">'+status.message.value+'</p>')
                    p.attr("id", 'edit-container-'+status.status_id.value)
                    p.prepend('<div class="alert alert-success alert-dismissible" role="alert"><button type="button" class="close" data-dismiss="alert" aria-label="Close"><span aria-hidden="true">&times;</span></button>'+json.result+'</div>');
                },

                // handle a non-successful response
                error : function(xhr,errmsg,err) {
                    var p = $('#edit-container-'+status.status_id.value);
                    p.prepend('<div class="alert alert-danger alert-dismissible" role="alert"><button type="button" class="close" data-dismiss="alert" aria-label="Close"><span aria-hidden="true">&times;</span></button>Oops! We have encountered an error: '+errmsg+'</div>');
                    console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
                }
            });
        };

    });

    $('.loadreply').click(function() {
        var btn = this.value;
        load_replies(btn)
        this.remove();
    });

    function load_replies(id) {
        $.ajax({
            url : "load_reply/", // the endpoint
            type : "POST", // http method
            data : { pk: id }, // data sent with the post request

            // handle a successful response
            success : function(json) {
               $('#reply-container-'+id).prepend(json);
            },

            // handle a non-successful response
            error : function(xhr,errmsg,err) {
                $('#reply-container-'+id).append('error in loading...');
            }
        });
    };


    $('.comment-container').each(function() {
        var status_id = this.id
        $(this).load("load_reply_to_index?in_reply_to="+status_id);

        $(this).ready(function() {
            $('#message-reply-'+status_id).ready(function() {
                $(document).on('submit','#message-reply-'+status_id , function(e){
                    e.preventDefault();
                    post_reply(this, status_id);
                    return false
                });

            });
        });
    })

    function post_reply(status, reply_to) {
        $.ajax({
            url : "load_reply_to_index/", // the endpoint
            type : "POST", // http method
            data : { status_id: reply_to, message : status.message.value }, // data sent with the post request

            // handle a successful response
            success : function(json) {
                console.log(json)
                console.log($('#reply-container-'+reply_to))
                $('#reply-container-'+reply_to).append(json);
            },

            // handle a non-successful response
            error : function(xhr,errmsg,err) {
    
            }
        });
    };
});

// This function gets cookie with a given name
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');
 
/*
The functions below will create a header with csrftoken
*/
 
function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
function sameOrigin(url) {
    // test that a given url is a same-origin URL
    // url could be relative or scheme relative or absolute
    var host = document.location.host; // host + port
    var protocol = document.location.protocol;
    var sr_origin = '//' + host;
    var origin = protocol + sr_origin;
    // Allow absolute or scheme relative URLs to same origin
    return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
        (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
        // or any other URL that isn't scheme relative or absolute i.e relative.
        !(/^(\/\/|http:|https:).*/.test(url));
}
 
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
            // Send the token to same-origin, relative URLs only.
            // Send the token only if the method warrants CSRF protection
            // Using the CSRFToken value acquired earlier
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});