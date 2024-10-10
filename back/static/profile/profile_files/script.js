jQuery(document).ready(function () {
  function view_marquee() {
    let marquee = $('.marquee');
    if ($.cookie('marquee') == null && $.cookie('marquee') !== 'false') {
      setTimeout(function () {
        marquee.addClass('view_marquee');
      }, 2500)
    }
    $('.marquee_close').on('click', function () {
      $.cookie('marquee', 'false', {expires: 7, path: '/'});
      marquee.removeClass('view_marquee');
    })
  }

  view_marquee();

  $('.ajax-form').submit(function (e) {
    e.preventDefault();

    let thisForm = $(this);
    let data = thisForm.serialize();
    let ajaxurl = send_object.url;

    jQuery.post(
      ajaxurl,
      data,
      function (request) {
        if (request.success === true) {
          document.querySelector('.sub__inner h2').textContent = 'Успешно!';
          document.querySelector('.sub__inner p').textContent = 'Спасибо за подписку.';
          thisForm.remove()
        }
        if (request.success === false) {
          $.each(request.data, function (key, val) {
            thisForm.find('input[name="' + key + '"]').attr("placeholder", val);
            thisForm.find('input[name="' + key + '"]').addClass('err');
            thisForm.find('textarea[name="' + key + '"]').attr("placeholder", val);
            thisForm.find('textarea[name="' + key + '"]').addClass('err');
          });
        }
      }
    );
  })

  // const imgContainers = document.querySelectorAll('.wp-block-image')
  // if (imgContainers) {
  //   const addLinksForFancybox = () => {
  //     imgContainers.forEach(el => {
  //       const a = document.createElement('a');
  //       const img = el.querySelector('img');
  //       a.setAttribute('data-fancybox', '')
  //       a.href = img.src;
  //       a.appendChild(img.cloneNode());
  //       img.remove();
  //       el.prepend(a);
  //     })
  //   }
  //   addLinksForFancybox();
  // }
})

