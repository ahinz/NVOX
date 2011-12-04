$(function() {
$(document).ajaxSend(function(event, xhr, settings) {
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
    function sameOrigin(url) {
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
    function safeMethod(method) {
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    if (!safeMethod(settings.type) && sameOrigin(settings.url)) {
        xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
    }
});


    function createVoteHandler(evt) {
	evt.preventDefault();
	var lnk = $(this);

	var id = lnk.attr("id").split("_");

	var href = "/vote/" + id[0]

	$.ajax({
	    url: href,
	    dataType: 'json',
	    data: {
		project: id[1],
		format: "json"
	    },
	    success: function(data) {
		if (data.success) {
		    $("#votes_" + id[1]).text(data.votes);
		} else {
		    var data = { "username": "administrator", "password": "12345" };

		    alert("failed... trying to log you in");
		    $.ajax({
			dataType: 'json',
			type: "POST",
			url: "/plogin",
			data: data,
			success: function(json) {
			    alert(JSON.stringify(json));
			    if (json.not_authenticated) {
			    }
			}
		    })
		};
	    }
	});

    }

//href="/vote/up?project={{ project.pk }}"
//href="/vote/down?project={{ project.pk }}"
    $(".vote").each(function() {
	$(this).click(createVoteHandler);
    });
});