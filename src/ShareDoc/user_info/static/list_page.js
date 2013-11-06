/*
var hide_dom = function(dom_str) {
	$(dom_str).hide();
}

var set_trigger_link = function(link_dom_str) {
	$(link_dom_str).click(function(event) {
		event.preventDefault();
		$(this).parent().children('div').slideDown('fast');
		$(this).parent().find('input[type="text"]').val("");
		$(this).fadeOut('fast');
	});
}

var set_cancel_button = function(button_dom_str) {
	$(button_dom_str).click(function(event) {
		$(this).parent().parent().slideUp('fast');
		$(this).parent().parent().parent().children('a').fadeIn('fast');
	});
}
*/
var set_trigger_link = function(link_dom_str, common_ancestor, show_dom_str, hide_dom_str, callback) {
	callback = typeof callback !== 'undefined' ? callback : function() {}; 
	$(link_dom_str).click(function(event) {
		event.preventDefault();
		var show_dom = $(this).parents(common_ancestor).children(show_dom_str);
		var hide_dom = $(this).parents(common_ancestor).children(hide_dom_str);

		callback(hide_dom, show_dom);

		if(hide_dom_str !== null){
			hide_dom.fadeOut('fast');
		}
		show_dom.slideDown('fast');
	});
}

var set_cancel_button = function(button_dom_str, common_ancestor, hide_dom_str, show_dom_str) {
	$(button_dom_str).click(function(event) {
		event.preventDefault();
		$(this).parents(common_ancestor).children(hide_dom_str).slideUp('fast');
		if(show_dom_str !== null){
			$(this).parents(common_ancestor).children(show_dom_str).fadeIn('fast');
		}
	});
}

var get_post_str = function() {
	var form = $(this);
	var post_str = form.serialize();
	var submit_name = form.find('input[type="submit"]').attr('name');
	post_str += ('&' + submit_name + '=');
	return post_str;
};

/*
var set_search_form = function(form_dom_str) {
	$(form_dom_str).submit(function(event) {
		event.preventDefault();
		var post_str = get_post_str.call(this);
		form = $(this);
		$.post('.', post_str, function(json_data) {
			if(json_data.error) {
				error_msg = "";
				$.each(json_data.error, function(index, value) {
					error_msg += index + ":" + value;
				});
				form.parent().children('p.error').text(error_msg);	
			}
			else {
				var search_result = form.parent().children('div.search_result');
				var html = "";
				if($.isEmptyObject(json_data.data)) {
					html = "<p>Can't Find Anything</p>";
				}
				else {
					$.each(json_data.data, function(index, value) {
						entry_html = "<p>";
					       	entry_html += index;
					       	entry_html += '<a href="' + value + '">';
						entry_html += "Attend";
						entry_html += "</a>";
						entry_html += "</p>";
						html += entry_html;
					});
				}
				search_result.html(html);
				search_result.find('a').click(function(event) {
					event.preventDefault();
					var add_item = $(this).parent();
					$.get($(this).attr('href'), function(data) {
						add_item.fadeOut('fast');
					});
				});
			}
		});
	});
}
*/

var set_search_form = function(form_dom_str, common_ancestor, error_dom_str, result_dom_str) {
	$(form_dom_str).submit(function(event) {
		event.preventDefault();
		post_str = get_post_str.call(this);
		var form = $(this);
		$.post('.', post_str, function(json_data) {
			if(json_data.error) {
				error_msg = "";
				$.each(json_data.error, function(index, value) {
					error_msg += index + ":" + value;
				});
				form.parents(common_ancestor).children(error_dom_str).text(error_msg);
			}
			else {
				var search_result = form.parents(common_ancestor).children(result_dom_str);
				var html = "";
				if($.isEmptyObject(json_data.data)) {
					html = "<p>Can't Find Anything</p>";
				}
				else {
					$.each(json_data.data, function(index, value) {
						entry_html = '<div class="result_item">';
					       	entry_html += '<span>' + index + '</span>';
					       	entry_html += '<a href="' + value + '">';
						entry_html += '[添加]';
						entry_html += '</a>';
						entry_html += '</div>';
						html += entry_html;
					});
				}
				search_result.html(html);
				search_result.find('a').click(function(event) {
					event.preventDefault();
					var add_item = $(this).parent();
					$.get($(this).attr('href'), function(data) {
						add_item.fadeOut('fast');
					});
				});
			}
		});
	});
}

var set_create_form = function(form_dom_str) {
	$(form_dom_str).submit(function(event) {
		event.preventDefault();
		var post_str = get_post_str.call(this);
		form = $(this);
		$.post('.', post_str, function(json_data) {
			if(json_data.error) {
				form.parent().children('p.error').text(json_data.error);
			}
			else {
				window.location.href = json_data.url;
			}
		});

	});
}
