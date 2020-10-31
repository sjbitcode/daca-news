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
            item.classList.add('text-gray-700')
        }
    });
};

document.addEventListener('DOMContentLoaded', () => {
    setPage()
})

///////////////////////////////////////////////////////////////

const searchInput = document.querySelector('#dacanews-search');
const searchButton = document.querySelector('#search-icon');

searchInput.addEventListener('keyup', (e) => {
    if (e.keyCode === 13) {
        e.preventDefault();
        searchButton.click();
    }
})

const fetchArticles = async () => {
    const url = document.location.origin + '/search?q=' + searchInput.value
    const response = await fetch(url)
    
    if (!response.ok) {
        throw new Error(`Error -- ${response.status}`)
    }
    const articles = await response.text()
    console.log(articles)

    // remove featured articles section if it exists
    let featured_articles = document.getElementById('featured-articles')
    if (featured_articles !== null) {
        featured_articles.remove()
    }

    // add search results
    searchResults = document.getElementById('search-results')
    searchResults.innerHTML = "";
    searchResults.insertAdjacentHTML('afterbegin', articles)
}

const searchAction = () => {
    const url = document.location.origin + '/search?q=' + searchInput.value
    console.log(url);
    fetchArticles().catch(err => {
        console.log(err.message)
    })
}





