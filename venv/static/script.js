// script.js

// Function to display a confirmation dialog for delete actions
function confirmDelete() {
    return confirm("Are you sure you want to delete this item?");
}

// Function to show a message to the user
function showMessage(message, success = true) {
    alert(message);
}

// Function to handle form submissions
function handleFormSubmit(event) {
    event.preventDefault();

    // Get form data
    const form = event.target;
    const formData = new FormData(form);

    fetch(form.action, {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Form submitted successfully
            showMessage(data.message, true);
        } else {
            // Handle form submission errors
            showMessage(data.message, false);
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

// Add event listeners when the document is loaded
document.addEventListener("DOMContentLoaded", function() {
    // Add a click event listener to an element with the ID "myButton"
    const button = document.getElementById("myButton");
    button.addEventListener("click", function() {
        // Handle the click event here
        // Example: confirmDelete() or any other action
    });

    // Add form submission event listeners to all forms on the page
    document.querySelectorAll('form').forEach(form => {
        form.addEventListener('submit', handleFormSubmit);
    });
});
