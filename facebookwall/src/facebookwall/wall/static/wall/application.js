$(document).ready(function() {
    action_buttons();

    bindlike($('.like'));
    bindpopover($('[data-toggle="popover"]'));
    bindedit($('.edit'));

    //postmessage
    $('.reply-form').on('submit', function(e) {
        e.preventDefault();
        $.post($(this).attr("action"), $(this).serialize(), function(data) {
            $(data).hide().appendTo('#reply-container').fadeIn('slow');
            $('#reply-container .panel:last').ready(function() {
                load_like_info($('#reply-container .panel:last div.like-info').get(0));
                action_buttons();
                bindlike($('#reply-container .panel:last .like'));
                bindpopover($('#reply-container .panel:last a.like-popover'));
                bindedit($('#reply-container .panel:last .edit'));
            });
        });
        $('form.message-form #message-content').val('');
    });

    //postmessage
    $('.message-form').on('submit', function(e) {
        e.preventDefault();
        $.post($(this).attr("action"), $(this).serialize(), function(data) {
            $(data).hide().prependTo('.status-container').fadeIn('slow');
            $('.status-container .panel:first').ready(function() {
                load_message_box($('.status-container .panel:first div.comment-container').get(0));
                load_like_info($('.status-container .panel:first div.like-info').get(0));
                action_buttons();
                $('#no-status').remove();
                bindlike($('.status-container .panel:first .like'));
                bindpopover($('.status-container .panel:first a.like-popover'));
                bindedit($('.status-container .panel:first .edit'));
            });
        });
        $('form.message-form #message-content').val('');
    });

    //deletestatus
    function action_buttons() {
        //delete status
        $('.delete').click(function() {
            var btn = this.value;
            $.get('delete_status/', { pk: btn }, function(data) {
                $('.panel#'+btn).fadeOut(300, function(){ 
                    $(this).remove();
                });
            });
        });

        $('.like-info').each(function() {
            load_like_info(this);
        });
    }

    //load replies
    $('.loadreply').click(function() {
        var btn = this.value;
        this.remove();
        $.get('load_reply/', { pk: btn }, function(data) {
            $('#reply-container-'+btn).prepend(data);
            action_buttons();
            bindpopover($('#reply-container-'+btn+ ' .like-popover'))
            bindlike($('#reply-container-'+btn+ ' .like'));
            bindedit($('#reply-container-'+btn+ ' .edit'));
        });
    });

    //reply to message
    $('.comment-container').each(function() {
        load_message_box(this);
    });

    function load_like_info(container) {
        var status_id = container.id
        $.get("like_info/", { pk: status_id }, function(data) {
            if (data.like_counts == 0) {
                $('#'+status_id+'.like-info').html("");
            } else if (data.like_counts == 1) {
                if (data.user_liked) {
                    $('#'+status_id+'.like-info').html("You like this");
                } else {
                    $('#'+status_id+'.like-info').html("1 like this");
                }
            } else {
                if (data.user_liked) {
                    $('#'+status_id+'.like-info').html("You and "+ --data.like_counts +" others like this");
                } else {
                    $('#'+status_id+'.like-info').html(data.like_counts +" like this");
                }
            }
        });
    }

    function load_message_box(container) {
        var status_id = container.id
        $(container).load("load_reply_to_index?in_reply_to="+status_id);

        $(container).ready(function() {
            $('#message-reply-'+status_id).ready(function() {
                $(document).on('submit','#message-reply-'+status_id , function(e){
                    e.preventDefault();
                    var post_data = $(this).serializeArray();
                    post_data.push({name: "status_id", value: status_id })
                    $.post("load_reply_to_index/", $.param(post_data), function(data) {
                        $('#reply-container-'+status_id).append(data);
                        $('form#message-reply-'+ status_id +' #message-content').val('');
                        action_buttons();
                        bindpopover($('#reply-container-'+status_id+ ' .like-popover:last'))
                        bindlike($('#reply-container-'+status_id+ ' .like:last'));
                        bindedit(('#reply-container-'+status_id+ ' .edit:last'));
                    });
                    return false;
                });

            });
        });
    }

    function bindedit(container) {
        //edit status
        container.click(function() {
            var btn = this.value;
            $("#edit-container-"+btn).load("edit_status/"+btn)

            $('#message-content').ready(function() {
                $(this).keypress(function (e) {
                    if (e.which == 13) {
                        $('.post-form').submit();
                        return false;
                    }
                });
            });

            $('.post-form').ready(function() {
                $(document).on('submit','.post-form' , function(e) {
                    e.preventDefault();
                    $.post('edit_status/'+btn, $(this).serialize(), function(data) {
                        var p = $('#edit-container-'+btn);
                        p.html('<p id="'+ btn +'">'+data.message+'</p>')
                        p.attr("id", 'edit-container-'+btn)
                        p.prepend('<div class="alert alert-success alert-dismissible" role="alert"><button type="button" class="close" data-dismiss="alert" aria-label="Close"><span aria-hidden="true">&times;</span></button>'+data.result+'</div>');
                    });
                });
            });
        });
    }

    function bindlike(container) {
        //like status
        container.click(function() {
            var btn = this.value;
            $.get('like_status/', { pk: btn }, function(data) {
                $('.like#'+btn+' span').text(data.result)
                load_like_info($('#'+btn+'.like-info').get(0));
            });
        });
    }

    function bindpopover(container) {
        container.popover({
            html: true,
            trigger: 'manual',
            content: function () {
                return $.ajax({url: 'show_likers/'+this.id,
                    dataType: 'html',
                    async: false}).responseText;
            }
        }).click(function(e) {
            $(this).popover('toggle');
        });
    }
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