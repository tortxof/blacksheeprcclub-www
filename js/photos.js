var images_div = document.querySelector('.images')

function sort_images(images) {
  return images.map(function(image, i) {return {i: i, v: image.s3_key.split('/')[1]}})
  .sort(function(a, b) {
    if (a.v > b.v) {
      return -1
    } else if (a.v === b.v) {
      return 0
    } else {
      return 1
    }
  })
  .map(function(el) {return images[el.i]})
}

function show_image(url) {
  var modal = document.createElement('div')
  modal.style.backgroundImage = 'url(' + url + '), linear-gradient(rgba(0,0,0,0.5), rgba(0,0,0,0.5))'
  modal.style.backgroundSize = 'contain'
  modal.style.backgroundRepeat = 'no-repeat'
  modal.style.backgroundPosition = 'center center'
  modal.style.position = 'fixed'
  modal.style.top = '0'
  modal.style.bottom = '0'
  modal.style.left = '0'
  modal.style.right = '0'
  document.body.appendChild(modal)
  modal.addEventListener('click', function(e) {
    e.target.parentNode.removeChild(e.target)
  })

}

fetch('https://imghost.djones.co/api/c/bsrcc')
.then(function(response) {
  if (response.status === 200) {
    response.json().then(function(collection) {
      sort_images(collection.images).forEach(function(image) {
        var image_container = document.createElement('div')
        var image_inner = document.createElement('div')
        var anchor = document.createElement('a')
        var img = document.createElement('img')
        image_inner.style.backgroundImage = 'linear-gradient(45deg,' + image.colors.slice(0, 3) + ')'
        image_inner.style.width = image.thumbs['128'].size.width + 'px'
        image_inner.style.height = image.thumbs['128'].size.height + 'px'
        image_inner.classList.add('image')
        image_container.classList.add('thumbnail')
        anchor.href = image.url
        anchor.appendChild(img)
        image_inner.appendChild(anchor)
        image_container.appendChild(image_inner)
        images_div.appendChild(image_container)
        img.src = image.thumbs['128'].url
      })
      Array.prototype.forEach.call(document.querySelectorAll('.image > a'), function(el) {
        el.addEventListener('click', function(e) {
          show_image(e.target.parentNode.href)
          e.preventDefault()
        })
      })
    })
  }
})
