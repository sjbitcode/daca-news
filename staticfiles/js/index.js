// ------------------------------------------------------------------
// Init
// ------------------------------------------------------------------

const hamburger = document.querySelector('#hamburger');
const smallNav = document.querySelector('#sm-nav');
const searchInput = document.querySelector('#dacanews-search');
const searchButton = document.querySelector('#search-icon');

// Setup things when the page has loaded.
document.addEventListener('DOMContentLoaded', (e) => {

    setActivePageLink()

    // toggle mobile/larger nav on screen size changes
    hamburger.addEventListener('click', () => {
        hamburger.classList.toggle('is-active')
        smallNav.classList.toggle('hidden')
    })

    if (searchInput) {
        // When Enter is hit on search bar, trigger the onclick function from searchButton
        searchInput.addEventListener('keyup', (e) => {
            if (e.keyCode === 13) {
                e.preventDefault();
                searchButton.click();
            }
        })
    }
});


// ------------------------------------------------------------------
// Utils / Helper functions
// ------------------------------------------------------------------

// Apply active styles on the current page nav link 
const setActivePageLink = () => {

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


// Remove featured and recent articles if they are there
const clearFeaturedAndRecentArticles = () => {

    let featured_articles = document.getElementById('featured-articles')
    if (featured_articles !== null) {
        featured_articles.remove()
    }

    let recent_articles = document.getElementById('recent-articles')
    if (recent_articles !== null) {
        recent_articles.remove()
    }
}


// Insert html in div.search-results
const updateSearchResultsDiv = (html, divId) => {

    searchResults = document.getElementById(divId)
    searchResults.innerHTML = "";
    searchResults.insertAdjacentHTML('afterbegin', html)
}


// Utility function for making requests
const makeRequest = async (url) => {
    console.log(`Making request to ${url}`)
    const response = await fetch(url)
    if (!response.ok) {
        throw new Error(`Cannot request ${url}, got ${response.status}`)
    }
    return await response.text()
}


// Make search request
const searchAction = () => {
    const url = `${document.location.origin}/search?q=${searchInput.value}`

    makeRequest(url).then(articles => {
        clearFeaturedAndRecentArticles()
        updateSearchResultsDiv(articles, 'search-results')
    })
    .catch(e => alert(e.message))

}


// Make AJAX paginated request
const fetchPaginated = async (el) => {
    const url = `${document.location.origin}/${el.getAttribute('data-pagination-url')}`

    makeRequest(url).then(articles => {
        clearFeaturedAndRecentArticles()
        updateSearchResultsDiv(articles, 'search-results')
    })
    .catch(e => alert(e.message))
}