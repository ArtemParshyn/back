jQuery(document).ready(function ($) {

    var ajaxurl = clicks_ajax.ajaxurl;

    $('.js-counter__btn').on('click', function(e){
        //alert('karma_action: ' + $(this).attr('data-curent_user_id'));

        var karma_action = $(this).attr('data-action');
        var current_user = $(this).attr('data-curent_user_id');
        var author_id = $(this).attr('data-author_id');
        var karma_type = $(this).attr('data-karma_type');
        var post_id = $(this).attr('data-post_id');
        var karma_block_id = $(this).closest('.js-counter__container').attr('id');
        // console.log(rec_banner_id);
        let self = $(this);
        let container = self.closest('.karma');
        var data = {
            action: 'send_carma',
            //event: 'click',
            karma_action: karma_action,
            current_user: current_user,
            author_id: author_id,
            karma_type:karma_type,
            post_id:post_id
        };
        //console.log(data);
        $.post(ajaxurl, data, function(response) {

            console.log(location.href + ' ' + '#' + karma_block_id);

            container.addClass('opa');

            container.load(location.href + ' ' + '#' + karma_block_id);
            //$('#karma_load').load('http://dev.protraffic.loc/news/tweetiktok-8214.html #elem_8214').addClass('opa');

            //location.reload();
            //$('.karma').load(location.href + '.karma_wrap' )

            //alert('Получено с сервера: ' + response);
            // console.log(response);
            //console.log($(this).html("<?php the_karma('author'); ?>"));
            // $(".it1").after("<li class='item'>Тест</li>");

            // let container = self.closest('.js-counter__container');
            // container.find('.js-counter__input').html(response);
            // container.find('.js-counter__btn').removeClass('js-counter__btn');
        });
    });

    // $('.js-counter__btn').on('click', function(e){
    //     //alert('karma_action: ' + $(this).attr('data-curent_user_id'));
    //
    //     var karma_action = $(this).attr('data-action');
    //     var current_user = $(this).attr('data-curent_user_id');
    //     var author_id = $(this).attr('data-author_id');
    //     // console.log(rec_banner_id);
    //     var data = {
    //         action: 'karma_post_click',
    //         //event: 'click',
    //         karma_action: karma_action,
    //         current_user: current_user,
    //         author_id: author_id,
    //     };
    //     console.log(data);
    //     $.post(ajaxurl, data, function(response) {
    //         alert('Получено с сервера: ' + response);
    //         console.log(response);
    //     });
    // });

});
