/**
 * FinanceBro Pro - Main JavaScript
 */

document.addEventListener('DOMContentLoaded', function() {
    console.log('FinanceBro Pro initialized');
    
    // Initialize Bootstrap tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Handle ticker form submission with validation and auto-uppercase
    const tickerForms = document.querySelectorAll('form');
    tickerForms.forEach(form => {
        const tickerInput = form.querySelector('input[name="ticker"]');
        if (tickerInput) {
            // Auto uppercase as you type
            tickerInput.addEventListener('input', function() {
                this.value = this.value.toUpperCase();
            });
            
            // Add validation - ticker should be 1-5 chars, alphanumeric
            tickerInput.addEventListener('blur', function() {
                const value = this.value.trim();
                const isValid = /^[A-Z0-9.]{1,5}$/.test(value);
                
                if (!isValid && value !== '') {
                    this.classList.add('is-invalid');
                    let feedback = form.querySelector('.invalid-feedback');
                    if (!feedback) {
                        feedback = document.createElement('div');
                        feedback.className = 'invalid-feedback d-block';
                        this.parentNode.appendChild(feedback);
                    }
                    feedback.textContent = 'Please enter a valid ticker symbol (1-5 characters)';
                } else {
                    this.classList.remove('is-invalid');
                    const feedback = form.querySelector('.invalid-feedback');
                    if (feedback) feedback.remove();
                }
            });
        }
        
        form.addEventListener('submit', function(e) {
            const tickerInput = this.querySelector('input[name="ticker"]');
            if (tickerInput && tickerInput.value) {
                // Convert to uppercase as user types
                tickerInput.value = tickerInput.value.toUpperCase();
                
                // Add loading state to submit button
                const submitBtn = this.querySelector('button[type="submit"]');
                if (submitBtn) {
                    submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span> Loading...';
                    submitBtn.disabled = true;
                }
            }
        });
    });
    
    // Add animation to cards
    animateCards();
    
    // Financial data formatting
    formatFinancialData();
});

/**
 * Add animation to cards when they come into view
 */
function animateCards() {
    const cards = document.querySelectorAll('.card');
    
    // Add observer only if IntersectionObserver is supported
    if ('IntersectionObserver' in window) {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('card-visible');
                    observer.unobserve(entry.target);
                }
            });
        }, { threshold: 0.1 });
        
        cards.forEach(card => {
            card.classList.add('card-animated');
            observer.observe(card);
        });
    }
}

/**
 * Format currency values
 * @param {number} value - The number to format
 * @param {string} currency - Currency code (default: USD)
 * @returns {string} Formatted currency string
 */
function formatCurrency(value, currency = 'USD') {
    if (value === null || isNaN(value)) return 'N/A';
    
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: currency,
        minimumFractionDigits: 2
    }).format(value);
}

/**
 * Format percentage values
 * @param {number} value - The number to format
 * @returns {string} Formatted percentage string
 */
function formatPercent(value) {
    if (value === null || isNaN(value)) return 'N/A';
    
    return new Intl.NumberFormat('en-US', {
        style: 'percent',
        minimumFractionDigits: 2,
        maximumFractionDigits: 2
    }).format(value / 100);
}

/**
 * Get appropriate CSS class based on trend
 * @param {string} trend - Trend string (Bullish, Bearish, Neutral)
 * @returns {string} CSS class name
 */
function getTrendClass(trend) {
    switch (trend?.toLowerCase()) {
        case 'bullish': return 'trend-bullish';
        case 'bearish': return 'trend-bearish';
        default: return 'trend-neutral';
    }
}

/**
 * Format all financial data on the page
 */
function formatFinancialData() {
    // Format currency values
    document.querySelectorAll('[data-format="currency"]').forEach(el => {
        const value = parseFloat(el.dataset.value);
        if (!isNaN(value)) {
            el.textContent = formatCurrency(value);
        }
    });
    
    // Format percentage values
    document.querySelectorAll('[data-format="percent"]').forEach(el => {
        const value = parseFloat(el.dataset.value);
        if (!isNaN(value)) {
            el.textContent = formatPercent(value);
        }
    });
    
    // Apply trend styling
    document.querySelectorAll('[data-trend]').forEach(el => {
        el.classList.add(getTrendClass(el.dataset.trend));
    });
} 