const hamburger = document.querySelector('#hamburger');
const smallNav = document.querySelector('#sm-nav');

hamburger.addEventListener('click', () => {
    // showing small nav
    hamburger.classList.toggle('is-active');
    smallNav.classList.toggle('hidden');
})

const setPage = () => {
    const url = document.location.pathname;

    // Change main nav
    document.querySelectorAll('#main-nav a').forEach(item => {
        if (item.getAttribute('href') == url) {
            item.classList.add('text-blue-700')
        }
        else {
            // remove class from any other elements
            item.classList.remove('text-blue-700')
        }

    });

    // Change mobile nav
    document.querySelectorAll('#sm-nav a').forEach(item => {
        if (item.getAttribute('href') == url) {
            item.classList.add('text-blue-700')
        }
        else {
            // remove class from any other elements
            item.classList.remove('text-blue-700')
        }
    });


};

document.addEventListener('DOMContentLoaded', () => {
    setPage()
})


