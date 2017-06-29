function nav_resize() {
  if (window.innerWidth < 550) {
    document.getElementById('nav').style.display = 'none'
    document.getElementById('nav-expand').style.display = 'block'
    nav_toggle_change_button();
  } else {
    document.getElementById('nav').style.display = 'block'
    document.getElementById('nav-expand').style.display = 'none'
  }
}

function nav_toggle_change_button() {
  var nav_toggle = document.querySelector('#nav-expand > i')
  if (document.getElementById('nav').style.display === 'block') {
    nav_toggle.classList.add('fa-times')
    nav_toggle.classList.remove('fa-bars')
  } else {
    nav_toggle.classList.add('fa-bars')
    nav_toggle.classList.remove('fa-times')
  }
}

window.addEventListener('resize', nav_resize)

document.getElementById('nav-expand').addEventListener('click', function() {
  var nav_el = document.getElementById('nav')
  if (nav_el.style.display === 'block') {
    nav_el.style.display = 'none'
  } else {
    nav_el.style.display = 'block'
  }
  nav_toggle_change_button()
})


nav_resize();
