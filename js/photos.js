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

var photosVue = new Vue({
  el: "#photos",
  data: {
    images: null,
    modalVisible: false,
    modalIndex: null
  },
  created: function() {
    window.addEventListener('keyup', this.keyHandler)
  },
  beforeDestroy: function() {
    window.removeEventListener('keyup', this.keyHandler)
  },
  methods: {
    keyHandler: function(e) {
      if (!this.modalVisible) return
      if (e.key === 'Escape') this.closeModal()
      else if (e.key === 'ArrowLeft') this.prevImage()
      else if (e.key === 'ArrowRight') this.nextImage()
    },
    gradientBackground: function(index) {
      var colors = this.images[index].colors
      return {backgroundImage: 'linear-gradient(45deg,' + colors.slice(0, 3) + ')'}
    },
    preloadImages: function(currentIndex) {
      for (var i = currentIndex - 1; i < currentIndex + 5; i++) {
        if (i >= 0 && i < this.images.length) {
          new Image().src = this.images[i].url
        }
      }
    },
    showModal: function showModal(index) {
      this.preloadImages(index)
      this.modalIndex = index
      this.modalVisible = true
    },
    closeModal: function() {
      this.modalVisible = false
      this.modalUrl = null
    },
    prevImage: function() {
      if (this.modalIndex <= 0) {
        this.modalIndex = this.images.length - 1
      } else {
        this.modalIndex--
      }
      this.preloadImages(this.modalIndex)
    },
    nextImage: function() {
      if (this.modalIndex >= this.images.length - 1) {
        this.modalIndex = 0
      } else {
        this.modalIndex++
      }
      this.preloadImages(this.modalIndex)
    }
  }
})


fetch("https://imghost.djones.co/api/c/bsrcc")
.then(function(response) {
  if (response.status === 200) {
    response.json().then(function(resData) {
      photosVue.images = sort_images(resData.images)
    })
  }
})
