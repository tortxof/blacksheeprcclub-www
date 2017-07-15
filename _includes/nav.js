var vue_nav = new Vue({
  el: '#nav',
  data: {
    small_screen: false,
    visible: false
  },
  methods: {
    toggle: function() {
      this.visible = !this.visible
    }
  }
})

function navResize() {
  vue_nav.small_screen = !(document.getElementById('small_bp_trigger').offsetWidth > 0)
}

window.addEventListener('resize', navResize)

navResize()
