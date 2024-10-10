jQuery(document).ready(function ($) {

    // $('div[data-name="event_location_city"]').find('select').attr('disabled',true)

    $('div[data-name="event_location_city"]').find('select').addClass('event_location_city')
         $('.event_location_city').attr('disabled',true)

    // $('#acf-field_60532f591abbb-field_6053334b58b2e').change(function (){
    $('div[data-name="event_location_country"]').find('select').change(function (){
        var data = {
            action: 'add_country_select',
            country: $('option:selected',this).text()
        };

        jQuery.post( ajaxurl, data, function(response) {
            $('.event_location_city').empty();
            $('.event_location_city').attr('disabled',false)
            // alert('Получено с сервера: ' + response);
            // console.log(response);
            $.each(response.data.choices, function(key , val) {
                $('.event_location_city').append('<option value="' + key + '">' + val + '</option>');
            });

        });
    })

    // Select 2
    $('.js-event-filter').select2();


    $('#event_city_filter').attr('disabled',true);

    $('#event_country_filter').change(function (){
        var data = {
            action: 'add_country_select',
            country: $('option:selected',this).text()
        };

        jQuery.post( clicks_ajax.ajaxurl, data, function(response) {
            $('#event_city_filter').empty();
            $('#event_city_filter').attr('disabled',false)
            // alert('Получено с сервера: ' + response);<option slected>Выберите страну проведения</option>
            //                         >
            // console.log(response);
            $('#event_city_filter').append('<option value="all">Все</option');
            $.each(response.data.choices, function(key , val) {
                $('#event_city_filter').append('<option value="' + key + '">' + val + '</option>');
            });

        });
    })

    $('#submit_event_filter').on('click', function (e){
        // alert('...');
        e.preventDefault();
        var data = {
            action: 'event_filter',
            format: $('#event_format_filter').val(),
            country: $('#event_country_filter').val(),
            city: $('#event_city_filter').val(),
            category: $('#event_category_filter').val(),
        };

        jQuery.post( clicks_ajax.ajaxurl, data, function(response) {
             $('#event_wrapper').empty();
            // $('#event_city_filter').attr('disabled',false)
            // alert('Получено с сервера: ' + response);
            // console.log(response);
             $('#event_wrapper').append(response);
            // $('#event_city_filter').append('<option value="all">Все</option');
            // $.each(response.data.choices, function(key , val) {
            //     $('#event_city_filter').append('<option value="' + key + '">' + val + '</option>');
            // });

        });

    })

    $('#event_format_filter').change(function (){
        let format = $('#event_format_filter').val();

        if(format == 'online'){
            $('#event_country_filter_wrap').hide();
            $('#event_city_filter_wrap').hide();
            console.log(format);
        } else {
            $('#event_country_filter_wrap').show();
            $('#event_city_filter_wrap').show();
        }
    });

    // $('div[data-name="event_start_day"]').find('input').addClass('event_start_day_input')
    //    $('.event_start_day_input').change(function (){
    //     var date_ev = $(this).val();
    //
    // })

    // $('div[data-name="event_start_day"]').find('select').change(function (){
    //     var date_ev = $(this).val();
    //
    // })


    $('div[data-name="event_start_day"]').find('select').change(function (){
        convert_unix();
    })
    $('div[data-name="event_finish_day"]').find('select').change(function (){
        convert_unix();
    })
    $('div[data-name="event_start_month"]').find('select').change(function (){
        convert_unix();
    })
    $('div[data-name="event_finish_month"]').find('select').change(function (){
        convert_unix();
    })
    $('div[data-name="event_year"]').find('select').change(function (){
        convert_unix();
    })


    function convert_unix(){

        let uStartDay = $('div[data-name="event_start_day"]').find('select').val();
        let uFinishDay = $('div[data-name="event_finish_day"]').find('select').val();

        let uStartMonth = $('div[data-name="event_start_month"]').find('select').val();
        let uFinishMonth = $('div[data-name="event_finish_month"]').find('select').val();

        let uYear = $('div[data-name="event_year"]').find('select').val();

        let unixStartEventData = new Date(uYear  +','+ uStartMonth +','+ uStartDay );
        let unixFinishEventData = new Date(uYear  +','+ uFinishMonth +','+ uFinishDay);

        let unixStartEvent = (unixStartEventData.getTime())/1000;
        // $("#unix_time_event_start").('');
        $("#unix_time_event_start").val(unixStartEvent);
        let unixFinishEvent = (unixFinishEventData.getTime())/1000;
        // $("#unix_time_event_finish").after('');
        $("#unix_time_event_finish").val(unixFinishEvent);

        console.log(unixStartEventData);
        var dt=eval(1612224000*1000);
        var myDate = new Date(dt);
        console.log(myDate);
    }
    convert_unix();

});
