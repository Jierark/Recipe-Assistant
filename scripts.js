// script.js
async function searchRecipes() {
    const query = document.getElementById('searchQuery').value;
    if (!query) {
        alert('Please enter a search query');
        return;
    }

    try {
        // 2 calls to openAI is going to take some time, so update front_end to avoid users spamming the button.
        const resultsContainer = document.getElementById('recipeResults');
        resultsContainer.innerHTML = '<p>Searching for recipes...</p>';
        const response = await fetch(`http://127.0.0.1:8000/api/recipes?query=${encodeURIComponent(query)}`);
        const data = await response.json();
        
        if (response.ok) {
            displayResults(data);
        } else {
            const resultsContainer = document.getElementById('recipeResults');
            resultsContainer.innerHTML = "<div class='error'><p>There was an error in parsing your request. Please try again.</p></div>";   
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Error fetching recipes. Please try again.');
    }
}

function displayResults(recipes) {
    const resultsContainer = document.getElementById('recipeResults');
    console.log(recipes)
    if (!recipes || recipes.trim() === '') {
        resultsContainer.innerHTML = `<p>No recipes found :(</>`;
        return
    }
    // TODO: Format results better.
    const recipeList = recipes.trim().split("\n").map(recipe => `<li>${recipe.trim()}</li>`)
    resultsContainer.innerHTML = `<div class="recipes-list">
        <ul>
        ${recipeList.join('')}
        </ul>
    </div>`;
}