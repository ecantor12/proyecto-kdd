$(document).ready(function() {
		$(".btn-report").click(function() {
			var url = $(this).attr("url");
			var cookie_csrftoken = $('meta[name=csrf_token]').attr("content");

			$.ajax({
				url: url,
				beforeSend: function(xhr, settings) {
					xhr.setRequestHeader("X-CSRFToken", cookie_csrftoken);
				},
				success: function(data) {
					if (data) {
						console.log("Ignite generation (OK)");
					}
				}

			});
		});
	});