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

    function submitVote(updown, project, errorhdlr) {

	var href = "/vote/" + updown

	$.ajax({
	    url: href,
	    dataType: 'json',
	    data: {
		project: project,
		format: "json"
	    },
	    success: function(data) {
		if (data.success) {
		    $("#votes_" + project).text(data.votes);
		} else {
		    if (errorhdlr) errorhdlr();
		}
	    }
	});
    }

    function createVoteHandler(evt) {
	evt.preventDefault();
	var lnk = $(this);

	var id = lnk.attr("id").split("_");

	var un = "user5";
	var pw = un;

	submitVote(id[0], id[1], function() {
	    $.ajax({
		dataType: 'json',
		type: "POST",
		url: "/plogin",
		data: { username: un,
			password: pw },
		error: function(jqXHR, textStatus, errorThrown) {
			    alert("error"); 
		},
		success: function(json) {
		    submitVote(id[0], id[1]);
		}
	    });
	});
    }

    var options = { backdrop: true, keyboard: true, show: false };

    function createToggleHandler(btn, div) {
	return function() {
	    if (div.css("display") == "none") {
		div.css("display","block");
	    } else {
		div.css("display","none");
	    }
	}
    }

    $(".commentmgr").each(function(idx,cmt) {
	var toggle = $(cmt).parent().siblings(".comments")[0]; 
	$(cmt).click(createToggleHandler($(cmt), $(toggle)));
    });

//href="/vote/up?project={{ project.pk }}"
//href="/vote/down?project={{ project.pk }}"
    $(".vote").each(function() {
	$(this).click(createVoteHandler);
    });
});

function drawChart(points, minx, maxx) {
	var chart = new Highcharts.Chart({
	    chart: {
		renderTo: 'chartdiv', 
		defaultSeriesType: 'scatter'
	    },
	    title: {
		text: 'nVox Project Analysis'
	    },
	    xAxis: {
		tickColor: "#ffffff",
	        min: minx-1,
		max: maxx+1,
		minPadding: 0.1,
		maxPadding: 0.1,
		labels: {
		    enabled: false
		},
		title: {
		    enabled: true,
		    text: 'Implementation Difficulty'
		}
	    },
	    yAxis: {
		title: {
		    text: 'Cost'
		}
	    },
	    tooltip: {
		formatter: function() {
		    return '<b>'+ this.point.name +'</b><br/>'+
			this.point.desc +'<br/>'+
			'Est. Cost: $'+ this.y +'<br/>Complexity: ' + this.x;;
		}
	    },
	    legend: {
		layout: 'vertical',
		style: {
		    left: '100px',
		    top: '70px',
		    bottom: 'auto'
		},
		backgroundColor: '#FFFFFF',
		borderWidth: 1,
		enabled: false,
	    },
	    plotOptions: {
		scatter: {
		    marker: {
			radius: 5,
			states: {
			    hover: {
				enabled: true,
				lineColor: 'rgb(100,100,100)'
			    }
			}
		    },
		    states: {
			hover: {
			    marker: {
				enabled: false
			    }
			}
		    }
		}
	    },
	    series: [{
		name: 'Projects',
		data: points
		
	    }]
	});
    }


