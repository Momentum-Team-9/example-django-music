console.log('HELLOOOO HI HEY')

const favLink = document.querySelector('.fav-link')

favLink.addEventListener('click', (event) => {
  event.preventDefault()
  const url = event.target.parentNode.href
  const heartIcon = event.target
  fetch(url, {
    headers: { 'X-Requested-With': 'XMLHttpRequest' },
  })
    .then((res) => res.json())
    .then((data) => {
      // here I can do stuff with that data!
      console.log(data)
      if (data['favorited']) {
        heartIcon.classList.replace('far', 'fas')
      } else {
        heartIcon.classList.replace('fas', 'far')
      }
    })
})
