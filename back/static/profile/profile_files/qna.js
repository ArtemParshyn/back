jQuery(document).ready(function ($) {

// Preloader
    let preloader = {
        $content: '.js-preload__content',
        $text: '.js-preload__text',
        activeClass: 'is--preload',

        showPreload(container) {
            container.addClass(this.activeClass)
            container.attr('disabled', 'disabled');
            container.find(this.$text).hide();
        },

        hidePreload(container) {
            container.removeClass(this.activeClass)
            container.removeAttr('disabled');
            container.find(this.$text).show();
        }
    };

    var ajaxurl = clicks_ajax.ajaxurl;


// add New Question
    let addQuestionForm = $('#add_question_form');
    let btnAddQuestion = $('#btn_add_question');


    btnAddQuestion.click(function () {

        addQuestionForm.validate({
            submitHandler: function () {
                preloader.showPreload(btnAddQuestion);

                $.ajax({
                    url: "/wp-content/themes/ptf/modules/question-answer/qna_question_function.php",
                    type: "POST",
                    data: $('#add_question_form').serialize(),
                    success: function (request) {
                        // console.log(request);

                        preloader.hidePreload(btnAddQuestion);

                        $('.question_title').removeClass('error_mess');
                        $('.question_content').removeClass('error_mess');
                        $('.error-question_title').remove() ;
                        $('.error-question_content').remove() ;

                        if(request.data == 'SUCCESS'){

                            $('#add_question_form').trigger('reset');
                            $('#btn_add_question').attr('style', 'display:none');
                            $('#qna_add_qwes_mess').html('Вопрос отправлен на модерацию');
                            setTimeout(function () {
                                location.href = '/qna';
                            }, 100);
                        } else {
                            $.each(request.data, function (key, val) {
                                console.log(key);
                                $('.' + key).addClass('error_mess');
                                $('.' + key).after('<span style="font-size: 14px" class="mb-2 d-block is--red error-' + key + '">' + val + '</span>');
                            });
                        };
                    },
                    error: function (request) {
                        preloader.hidePreload(btnAddQuestion);
                        mess_err();
                        //$('#qna_add_qwes_mess').html(response);
                        console.log(response);
                    }
                }).done(function (request) {
                });
            }
        })
        function mess_save() {
            $('.status-save').show(200);
            setTimeout(function () {
                $('.status-save').hide(300);
            }, 2000);
        }

        function mess_draft() {
            $('.status-draft').show(200);
            setTimeout(function () {
                $('.status-draft').hide(300);
            }, 2000);
        }

        function mess_moder() {
            $('.status-moderation').show(200);
            setTimeout(function () {
                $('.status-moderation').hide(300);
            }, 2000);
        }

        function mess_err() {
            $('.status-err').show(200);
            setTimeout(function () {
                $('.status-err').hide(300);
            }, 2000);
        }
    })

    // /**
    //  * Добавление отзыва
    //  **/
    // $('#add_review').submit(function (e) {
    //     e.preventDefault();
    //     $.ajax({
    //         type: 'POST',
    //         url: '/wp-content/themes/ptf/inc/add_review.php',
    //         data: $(this).serialize(),
    //         success: () => {
    //             console.log('Спасибо. Ваш отзыв отправлен.');
    //             $(this).trigger('reset'); // очищаем поля формы
    //         },
    //         error: () => console.log('Ошибка отправки.')
    //     });
    // });

    //$('.text-content').find('img').wrap('<figure class="wp-block-image size-large"></figure>');
    // $('.text-content').find('img').after('</div>');
    //let pp = $('.text-content').find('img');
    //console.log(pp);
})
