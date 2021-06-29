// listen for click on the heart
// submit the request to favorite the album
// update the heart's color

const favLink = document.querySelector(".fav-link")

const toggleFavorite = (event) => {
  event.preventDefault() // disable the link
  const heartIcon = event.target
  const url = event.currentTarget.href // get the url from the a element in the DOM
  fetch(url, {
    headers: {'X-Requested-With': 'XMLHttpRequest'},
  })
    .then(res => res.json())
    .then(data => {
      // The data can tell me if the album is favorited or not
        // Based on that, I can change the heart to the way it should look
        console.log("DATA: ", data)
        if (data["favorited"]) {
          heartIcon.classList.replace("far", "fas")
        } else {
          heartIcon.classList.replace("fas", "far")
        }
    } )
}

favLink.addEventListener('click', toggleFavorite)
