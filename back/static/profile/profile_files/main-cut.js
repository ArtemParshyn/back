document.addEventListener('DOMContentLoaded', () => {
  const adminAjax = send_object.url;
  const bannersContainerClass = 'rec_banners_container';
  const bannersItemsClass = 'rec_banners_item';
  const time = 30000;

  function sendAjax(ajaxLink, action, id) {
    let xhr = new XMLHttpRequest();
    xhr.open('POST', (ajaxLink + '?action=' + action));
    xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8');
    xhr.send(`ID=${id}`);
  }

  document.querySelectorAll(`.${bannersItemsClass}`).forEach(banner => {
    banner.addEventListener('click', () => {
      sendAjax(adminAjax, 'bnnr_clicks', banner.dataset.bannerId);
    })
  })

  function bnnrs(containerClass, bannerClass, bannerDelay) {
    document.querySelectorAll(`.${containerClass}`).forEach(container => {
      const banners = container.querySelectorAll(`.${bannerClass}`);
      container.dataset.showIndex = '0';
      let showIndex = Number(container.dataset.showIndex)

      function show() {
        if (showIndex === banners.length) showIndex = 0;
        banners.forEach(banner => banner.classList.remove('show'));
        banners[showIndex].classList.add('show')
        showIndex++;
        container.dataset.showIndex = showIndex;
        if (showIndex === banners.length) container.dataset.showIndex = '0';
      }

      show();
      setInterval(show, bannerDelay);
    })
  }
  bnnrs(bannersContainerClass, bannersItemsClass, time);
})

