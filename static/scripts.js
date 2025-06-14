// DOM Elements
const searchInput = document.getElementById('searchQuery');
const recipeResults = document.getElementById('recipeResults');
const loadingElement = document.getElementById('loading');
const errorElement = document.getElementById('error');

// In static/scripts.js
async function searchRecipes() {
    const query = document.getElementById('searchQuery').value.trim();
    if (!query) {
        showError('Please enter a search term');
        return;
    }

    showLoading(true);
    clearResults();
    hideError();

    try {
        const response = await fetch(`/api/recipes?query=${encodeURIComponent(query)}`);
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const recipes = await response.json();
        console.log('Received recipes:', recipes);
        displayResults(recipes);
    } catch (error) {
        console.error('Search error:', error);
        showError('Failed to load recipes. Please try again.');
    } finally {
        showLoading(false);
    }
}

function displayResults(recipes) {
    const recipeResults = document.getElementById('recipeResults');
    recipeResults.innerHTML = '';
    
    if (!recipes || recipes.length === 0) {
        showError('No recipes found. Try a different search term.');
        return;
    }

    const recipeCards = recipes.map(recipe => `
        <div class="recipe-card">
            <div class="recipe-content">
                <h3>${recipe.title || 'Recipe'}</h3>
                <a href="/recipe/${recipe.id}" class="view-recipe">View Recipe</a>
            </div>
        </div>
    `).join('');

    recipeResults.innerHTML = recipeCards;
}

function showLoading(show) {
    document.getElementById('loading').classList.toggle('hidden', !show);
}

function showError(message) {
    const errorEl = document.getElementById('error');
    errorEl.textContent = message;
    errorEl.classList.remove('hidden');
}

function hideError() {
    document.getElementById('error').classList.add('hidden');
}

function clearResults() {
    document.getElementById('recipeResults').innerHTML = '';
}

// Add event listener for Enter key
document.getElementById('searchQuery').addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
        searchRecipes();
    }
});