// skill_validation_system/static/js/main.js

document.addEventListener('DOMContentLoaded', function() {
    console.log("Skill Validation System JS loaded.");

    // Find all elements with the class 'flag-toggle'
    const flagToggles = document.querySelectorAll('.flag-toggle');
    
    // Add a click event listener to each flag button
    flagToggles.forEach(toggle => {
        toggle.addEventListener('click', function(event) {
            event.preventDefault(); // Prevent default button behavior

            const button = this;
            const responseId = button.dataset.responseId;
            // The current flagged status is stored in a data attribute
            const isCurrentlyFlagged = button.dataset.flagged === 'true';
            
            // The new status will be the opposite of the current one
            const newFlaggedStatus = !isCurrentlyFlagged;

            // Send a POST request to the server to update the flag status
            fetch(`/hr/flag_response/${responseId}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Accept': 'application/json'
                },
                body: JSON.stringify({ flagged: newFlaggedStatus })
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                // If the server confirms the update was successful
                if (data.success) {
                    // Update the button's state in the UI
                    button.dataset.flagged = String(newFlaggedStatus);
                    
                    // Find the status cell in the same row and update its text/class
                    const statusCell = document.querySelector(`#status-cell-${responseId}`);
                    
                    if (newFlaggedStatus) {
                        button.textContent = 'Unflag';
                        button.classList.add('flagged-btn'); // Use for different styling if needed
                        if(statusCell) {
                            statusCell.textContent = 'Flagged for Review';
                            statusCell.classList.add('flagged');
                        }
                    } else {
                        button.textContent = 'Flag';
                        button.classList.remove('flagged-btn');
                        if(statusCell) {
                            statusCell.textContent = 'OK';
                            statusCell.classList.remove('flagged');
                        }
                    }
                } else {
                    // Log an error if the server reports failure
                    console.error('Failed to update flag status.');
                }
            })
            .catch(error => console.error('Error:', error));
        });
    });
});
