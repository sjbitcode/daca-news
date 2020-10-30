const hamburger = document.querySelector('#hamburger');
const smallNav = document.querySelector('#sm-nav');

hamburger.addEventListener('click', () => {
    // showing small nav
    hamburger.classList.toggle('is-active');
    smallNav.classList.toggle('hidden');
})
