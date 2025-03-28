document.addEventListener('DOMContentLoaded', function() {
    // Initialize MathJax
    if (typeof MathJax !== 'undefined') {
        MathJax.Hub.Config({
            tex2jax: {
                inlineMath: [['$', '$'], ['\\(', '\\)']],
                displayMath: [['$$', '$$'], ['\\[', '\\]']],
                processEscapes: true
            },
            "HTML-CSS": { fonts: ["TeX"] }
        });
    }
    
    // Problem submission form
    const problemForm = document.getElementById('problem-form');
    if (problemForm) {
        problemForm.addEventListener('submit', function(e) {
            e.preventDefault();
            submitProblem();
        });
    }
    
    // Waitlist form
    const waitlistForm = document.getElementById('waitlist-form');
    if (waitlistForm) {
        waitlistForm.addEventListener('submit', function(e) {
            // Form will be handled by Flask route
        });
    }
    
    // Load example problems
    loadExamples();
    
    // Initialize tooltips and popovers if Bootstrap is available
    if (typeof bootstrap !== 'undefined') {
        const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
        tooltipTriggerList.map(function(tooltipTriggerEl) {
            return new bootstrap.Tooltip(tooltipTriggerEl);
        });
        
        const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
        popoverTriggerList.map(function(popoverTriggerEl) {
            return new bootstrap.Popover(popoverTriggerEl);
        });
    }
});

/**
 * Submit a math problem to be solved
 */
function submitProblem() {
    const problemText = document.getElementById('problem-text').value;
    const problemType = document.getElementById('problem-type').value;
    const solutionDisplay = document.getElementById('solution-display');
    const loadingSpinner = document.getElementById('loading-spinner');
    
    if (!problemText.trim()) {
        showAlert('Please enter a math problem to solve', 'danger');
        return;
    }
    
    // Show loading state
    solutionDisplay.innerHTML = '';
    loadingSpinner.classList.remove('d-none');
    
    // Create form data
    const formData = new FormData();
    formData.append('problem_text', problemText);
    formData.append('problem_type', problemType);
    
    // Send request to server
    fetch('/solve', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        loadingSpinner.classList.add('d-none');
        
        if (data.status === 'success') {
            // Display the solution
            solutionDisplay.innerHTML = `
                <div class="solution-display">
                    <h5 class="mb-3">Solution:</h5>
                    <div class="math-formula">$$${data.solution}$$</div>
                </div>
            `;
            
            // Render math expressions
            if (typeof MathJax !== 'undefined') {
                MathJax.Hub.Queue(["Typeset", MathJax.Hub, solutionDisplay]);
            }
        } else {
            // Show error message
            showAlert(data.message || 'Failed to solve the problem. Please try again.', 'danger');
        }
    })
    .catch(error => {
        loadingSpinner.classList.add('d-none');
        showAlert('An error occurred while solving the problem. Please try again.', 'danger');
        console.error('Error:', error);
    });
}

/**
 * Load example problems
 */
function loadExamples() {
    const examplesContainer = document.getElementById('examples-container');
    if (!examplesContainer) return;
    
    fetch('/examples')
    .then(response => response.json())
    .then(examples => {
        examplesContainer.innerHTML = '';
        
        examples.forEach(example => {
            const exampleCard = document.createElement('div');
            exampleCard.className = 'col-md-6 mb-4';
            exampleCard.innerHTML = `
                <div class="card example-card h-100">
                    <div class="card-body">
                        <h5 class="card-title">Example: ${example.type.charAt(0).toUpperCase() + example.type.slice(1)}</h5>
                        <p class="card-text">
                            <strong>Problem:</strong> ${example.problem}
                        </p>
                        <p class="card-text">
                            <strong>Solution:</strong> ${example.solution}
                        </p>
                        <button class="btn btn-sm btn-outline-info try-example" 
                                data-problem="${example.problem}" 
                                data-type="${example.type}">
                            Try this example
                        </button>
                    </div>
                </div>
            `;
            examplesContainer.appendChild(exampleCard);
        });
        
        // Add event listeners to example buttons
        document.querySelectorAll('.try-example').forEach(button => {
            button.addEventListener('click', function() {
                const problem = this.getAttribute('data-problem');
                const type = this.getAttribute('data-type');
                
                document.getElementById('problem-text').value = problem;
                
                const problemTypeSelect = document.getElementById('problem-type');
                if (problemTypeSelect) {
                    // Select the right option if it exists
                    const option = Array.from(problemTypeSelect.options).find(opt => opt.value === type);
                    if (option) {
                        problemTypeSelect.value = type;
                    }
                }
                
                // Scroll to form
                document.getElementById('solve-section').scrollIntoView({ behavior: 'smooth' });
            });
        });
    })
    .catch(error => {
        console.error('Error loading examples:', error);
        examplesContainer.innerHTML = '<div class="alert alert-danger">Failed to load example problems</div>';
    });
}

/**
 * Show an alert message
 */
function showAlert(message, type = 'info') {
    const alertsContainer = document.getElementById('alerts-container');
    if (!alertsContainer) return;
    
    const alert = document.createElement('div');
    alert.className = `alert alert-${type} alert-dismissible fade show`;
    alert.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    `;
    
    alertsContainer.appendChild(alert);
    
    // Auto-dismiss after 5 seconds
    setTimeout(() => {
        alert.classList.remove('show');
        setTimeout(() => {
            alertsContainer.removeChild(alert);
        }, 150);
    }, 5000);
}

/**
 * Animate the math symbols on the page
 */
function animateMathSymbols() {
    const symbols = document.querySelectorAll('.animated-math-symbol');
    symbols.forEach((symbol, index) => {
        setTimeout(() => {
            symbol.style.opacity = '1';
            symbol.style.transform = 'translateY(0)';
        }, index * 100);
    });
}
