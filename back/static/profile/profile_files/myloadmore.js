jQuery(function($){ // use jQuery code inside this to avoid "$ is not defined" error

    let showCount = Number($("#js-show_faq_count").val());
    let pages = showCount;

    $('.loadmore').click(function(){

        var button = $(this),
            filtered = $(this).data('filtered'),
            count = $(this).data('count'),
            data = {
                'action': 'loadmore',
                'query': loadmore_params.posts, // that's how we get params from wp_localize_script() function
                'page' : loadmore_params.current_page,
                'filtered': filtered
            };

        pages += showCount;

        $ .ajax({ // you can also use $.post here
            url : loadmore_params.ajaxurl, // AJAX handler
            data : data,
            type : 'POST',
            beforeSend : function ( xhr ) {
                button.text('Загружаю...'); // change the button text, you can also add a preloader image
            },
            success : function( data ){
                if( data ) {
                    button.text( 'Показать еще' );
                    //button.text( 'More posts' ).prev().before(data); // insert new posts
                    loadmore_params.current_page++;

                    $('.result_' + filtered).before(data);

                    if ( pages == count ){
                        button.remove(); // if last page, remove the button
                    }
                    // you can also fire the "post-load" event here if you use a plugin that requires it
                    // $( document.body ).trigger( 'post-load' );
                } else {
                    button.remove(); // if no data, remove the button as well
                }
            }
        });
    });
});
