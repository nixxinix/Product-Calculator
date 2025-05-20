// Adds a new ingredient input block to the ingredient list container
function addIngredient() {
    const container = document.getElementById("ingredient-list");

    // Create a new div element for the ingredient inputs
    const ingredientDiv = document.createElement("div");
    ingredientDiv.classList.add("ingredient", "mb-3", "border", "rounded", "p-3", "bg-light");

    // Set inner HTML with inputs and select elements for the ingredient
    ingredientDiv.innerHTML = `
        <input class="form-control mb-2" name="name" placeholder="Ingredient Name" required />
        <div class="row g-2 mb-2">
            <div class="col-md">
                <select class="form-select" name="available_unit" required>
                    <option value="">Available Unit</option>
                    <option value="kg">kg</option>
                    <option value="g">g</option>
                    <option value="l">l</option>
                    <option value="ml">ml</option>
                    <option value="pcs">pcs</option>
                </select>
            </div>
            <div class="col-md">
                <input class="form-control" name="available_qty" placeholder="Available Quantity" type="number" step="0.01" min="0" required />
            </div>
        </div>
        <div class="row g-2 mb-2">
            <div class="col-md">
                <select class="form-select" name="required_unit" required>
                    <option value="">Required Unit</option>
                    <option value="kg">kg</option>
                    <option value="g">g</option>
                    <option value="l">l</option>
                    <option value="ml">ml</option>
                    <option value="pcs">pcs</option>
                </select>
            </div>
            <div class="col-md">
                <input class="form-control" name="required_per_unit" placeholder="Required per Product Unit" type="number" step="0.01" min="0" required />
            </div>
        </div>
        <input class="form-control mb-2" name="cost_per_unit" placeholder="Cost per Unit" type="number" step="0.01" min="0" required />
        <!-- Remove button for this ingredient -->
        <button type="button" class="btn btn-sm btn-danger remove-ingredient-btn" onclick="this.parentElement.remove()">Remove</button>
    `;
    container.appendChild(ingredientDiv); // Add the new ingredient block to the DOM
}

// Saves the current ingredient list with a given name to the server
async function saveIngredientList() {
    const saveName = document.getElementById('save_name').value;

    // Validate save name input
    if (!saveName) {
        alert('Please enter a name for the list.');
        return;
    }

    const ingredients = [];
    // Collect all ingredient input data into an array
    const ingredientDivs = document.querySelectorAll('#ingredient-list .ingredient');
    ingredientDivs.forEach(div => {
        ingredients.push({
            name: div.querySelector('[name="name"]').value,
            available_unit: div.querySelector('[name="available_unit"]').value,
            available_qty: parseFloat(div.querySelector('[name="available_qty"]').value),
            required_unit: div.querySelector('[name="required_unit"]').value,
            required_per_unit: parseFloat(div.querySelector('[name="required_per_unit"]').value),
            cost_per_unit: parseFloat(div.querySelector('[name="cost_per_unit"]').value),
        });
    });

    // POST the data to the backend endpoint
    const response = await fetch('/save_ingredients', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ name: saveName, ingredients: ingredients }),
    });

    if (response.ok) {
        alert('Ingredients saved successfully!');
        loadSavedLists(); // Refresh the saved lists dropdown
        document.getElementById('save_name').value = ''; // Clear input after saving
    } else {
        alert('Failed to save ingredients.');
    }
}

// Loads the saved ingredient lists from the server and updates the dropdown
async function loadSavedLists() {
    const response = await fetch('/get_saved_ingredients');

    if (response.ok) {
        const savedLists = await response.json();
        const loadListDropdown = document.getElementById('load_list');

        // Clear current options except the default
        loadListDropdown.innerHTML = '<option value="">-- Select a list --</option>';

        // Add each saved list as an option
        savedLists.forEach(list => {
            const option = document.createElement('option');
            option.value = list.name;
            option.textContent = list.name;
            loadListDropdown.appendChild(option);
        });
    } else {
        console.error('Failed to load saved ingredient lists.');
    }
}

// Loads a selected ingredient list and populates the form inputs with it
async function loadIngredientList() {
    const listName = document.getElementById('load_list').value;
    if (!listName) return; // Do nothing if no list is selected

    // Fetch saved ingredients data for the selected list
    const response = await fetch(`/load_ingredients/${listName}`);

    if (response.ok) {
        const loadedIngredients = await response.json();
        const ingredientListDiv = document.getElementById('ingredient-list');

        ingredientListDiv.innerHTML = ''; // Clear existing ingredients

        // For each loaded ingredient, create and append an ingredient input block prefilled with saved data
        loadedIngredients.forEach(ing => {
            const ingredientDiv = document.createElement("div");
            ingredientDiv.classList.add("ingredient", "mb-3", "border", "rounded", "p-3", "bg-light");
            ingredientDiv.innerHTML = `
                <input class="form-control mb-2" name="name" value="${ing.name}" placeholder="Ingredient Name" required />
                <div class="row g-2 mb-2">
                    <div class="col-md">
                        <select class="form-select" name="available_unit" required>
                            <option value="">Available Unit</option>
                            <option value="kg" ${ing.available_unit === 'kg' ? 'selected' : ''}>kg</option>
                            <option value="g" ${ing.available_unit === 'g' ? 'selected' : ''}>g</option>
                            <option value="l" ${ing.available_unit === 'l' ? 'selected' : ''}>l</option>
                            <option value="ml" ${ing.available_unit === 'ml' ? 'selected' : ''}>ml</option>
                            <option value="pcs" ${ing.available_unit === 'pcs' ? 'selected' : ''}>pcs</option>
                        </select>
                    </div>
                    <div class="col-md">
                        <input class="form-control" name="available_qty" value="${ing.available_qty}" placeholder="Available Quantity" type="number" step="0.01" min="0" required />
                    </div>
                </div>
                <div class="row g-2 mb-2">
                    <div class="col-md">
                        <select class="form-select" name="required_unit" required>
                            <option value="">Required Unit</option>
                            <option value="kg" ${ing.required_unit === 'kg' ? 'selected' : ''}>kg</option>
                            <option value="g" ${ing.required_unit === 'g' ? 'selected' : ''}>g</option>
                            <option value="l" ${ing.required_unit === 'l' ? 'selected' : ''}>l</option>
                            <option value="ml" ${ing.required_unit === 'ml' ? 'selected' : ''}>ml</option>
                            <option value="pcs" ${ing.required_unit === 'pcs' ? 'selected' : ''}>pcs</option>
                        </select>
                    </div>
                    <div class="col-md">
                        <input class="form-control" name="required_per_unit" value="${ing.required_per_unit}" placeholder="Required per Product Unit" type="number" step="0.01" min="0" required />
                    </div>
                </div>
                <input class="form-control mb-2" name="cost_per_unit" value="${ing.cost_per_unit}" placeholder="Cost per Unit" type="number" step="0.01" min="0" required />
                <!-- Remove button for each ingredient -->
                <button type="button" class="btn btn-sm btn-danger remove-ingredient-btn" onclick="this.parentElement.remove()">Remove</button>
            `;
            ingredientListDiv.appendChild(ingredientDiv);
        });
    } else {
        alert('Failed to load ingredients.');
    }
}

// Removes the selected saved ingredient list from the server and UI
async function removeIngredientList() {
    const listName = document.getElementById('load_list').value;

    // Validate if a list is selected
    if (!listName) {
        alert('Please select a list to remove.');
        return;
    }

    // Send DELETE request to backend to remove the list
    const response = await fetch(`/remove_ingredients/${listName}`, {
        method: 'DELETE',
    });

    if (response.ok) {
        alert('List removed successfully!');
        loadSavedLists(); // Refresh the saved lists dropdown
        document.getElementById('load_list').value = ''; // Clear the selection
        document.getElementById('ingredient-list').innerHTML = ''; // Clear the ingredients displayed
    } else {
        alert('Failed to remove list.');
    }
}

// Load saved ingredient lists when the page loads
window.onload = loadSavedLists;
