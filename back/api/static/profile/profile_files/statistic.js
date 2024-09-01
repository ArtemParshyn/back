jQuery(document).ready(function ($) {

	var ajaxurl = clicks_ajax.ajaxurl;

	$('.pr-menu-item').on('click', function(e){
		//event.preventDefault();
		//alert('111');
		var data = {
			action: 'rec_menu_clicks',
			event: 'click',
		};
		$.post(ajaxurl, data, function(response) {
			//alert('Получено с сервера: ' + response);
			console.log(response);
		});

	});

	//клики по баннерам

	// $('.rec_banners_item').on('click', function(e){
	// 	//alert('id banner: ' + $(this).attr('data-banner_id'));
	//
	// 	var rec_banner_id= $(this).attr('data-banner_id');
	// 	// console.log(rec_banner_id);
	// 	var data = {
	// 		action: 'banner_clicks',
	// 		//event: 'click',
	// 		send_banner_id: rec_banner_id,
	// 	};
	// 	$.post(ajaxurl, data, function(response) {
	// 		//alert('Получено с сервера: ' + response);
	// 		console.log(response);
	// 	});
	// });

	$('.right-popup .popup-btn').on('click', function(e){
		//alert('id banner: ' + $(this).attr('data-banner_id'));

		var rec_banner_id= $(this).attr('data-banner_id');
		// console.log(rec_banner_id);
		var data = {
			action: 'banner_clicks',
			//event: 'click',
			send_banner_id: rec_banner_id,
		};
		$.post(ajaxurl, data, function(response) {
			//alert('Получено с сервера: ' + response);
			console.log(response);
		});
	});

});

