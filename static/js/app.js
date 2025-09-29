// Main JavaScript file for MIS 3010 Web Application
// Author: Ryan Herren

// Global App Object
const MIS3010App = {
    // Configuration
    config: {
        timeUpdateInterval: 1000, // 1 second
        apiEndpoints: {
            time: '/api/time',
            users: '/api/users'
        }
    },

    // Initialize the application
    init() {
        console.log('MIS 3010 App initialized');
        this.setupEventListeners();
        this.initializeComponents();
        this.startTimeUpdates();
    },

    // Set up global event listeners
    setupEventListeners() {
        // Handle navigation active states
        this.updateActiveNavigation();
        
        // Handle form submissions with loading states
        const forms = document.querySelectorAll('form');
        forms.forEach(form => {
            form.addEventListener('submit', this.handleFormSubmit.bind(this));
        });

        // Handle card hover effects
        this.initializeCardEffects();
        
        // Handle responsive navigation
        this.setupResponsiveNavigation();
    },

    // Initialize various components
    initializeComponents() {
        // Initialize tooltips if Bootstrap is loaded
        if (typeof bootstrap !== 'undefined') {
            const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]');
            [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl));
        }

        // Initialize any animations
        this.initializeAnimations();
        
        // Load user preferences
        this.loadUserPreferences();
    },

    // Update active navigation based on current page
    updateActiveNavigation() {
        const currentPath = window.location.pathname;
        const navLinks = document.querySelectorAll('.navbar-nav .nav-link');
        
        navLinks.forEach(link => {
            const href = link.getAttribute('href');
            if (href === currentPath) {
                link.classList.add('active');
            } else {
                link.classList.remove('active');
            }
        });
    },

    // Handle form submissions with loading states
    handleFormSubmit(event) {
        const form = event.target;
        const submitButton = form.querySelector('button[type="submit"], input[type="submit"]');
        
        if (submitButton) {
            submitButton.classList.add('loading');
            submitButton.disabled = true;
            
            // Re-enable after 5 seconds as fallback
            setTimeout(() => {
                submitButton.classList.remove('loading');
                submitButton.disabled = false;
            }, 5000);
        }
    },

    // Initialize card hover effects
    initializeCardEffects() {
        const cards = document.querySelectorAll('.card');
        
        cards.forEach(card => {
            // Add subtle animation on hover
            card.addEventListener('mouseenter', function() {
                this.style.transition = 'transform 0.3s ease, box-shadow 0.3s ease';
            });
        });
    },

    // Setup responsive navigation
    setupResponsiveNavigation() {
        const navbarToggler = document.querySelector('.navbar-toggler');
        const navbarCollapse = document.querySelector('.navbar-collapse');
        
        if (navbarToggler && navbarCollapse) {
            // Close mobile menu when clicking on a link
            const navLinks = navbarCollapse.querySelectorAll('.nav-link');
            navLinks.forEach(link => {
                link.addEventListener('click', () => {
                    if (window.innerWidth < 992) { // Bootstrap lg breakpoint
                        const bsCollapse = bootstrap.Collapse.getInstance(navbarCollapse);
                        if (bsCollapse) {
                            bsCollapse.hide();
                        }
                    }
                });
            });
        }
    },

    // Start time updates for home page
    startTimeUpdates() {
        const timeElement = document.getElementById('current-time');
        const dateElement = document.getElementById('current-date');
        
        if (timeElement || dateElement) {
            this.updateDateTime();
            setInterval(() => this.updateDateTime(), this.config.timeUpdateInterval);
        }
    },

    // Update date and time display
    updateDateTime() {
        const now = new Date();
        
        // Update date
        const dateElement = document.getElementById('current-date');
        if (dateElement) {
            const dateOptions = { 
                weekday: 'long', 
                year: 'numeric', 
                month: 'long', 
                day: 'numeric' 
            };
            dateElement.textContent = now.toLocaleDateString('en-US', dateOptions);
        }
        
        // Update time
        const timeElement = document.getElementById('current-time');
        if (timeElement) {
            const timeOptions = {
                hour12: false,
                hour: '2-digit',
                minute: '2-digit',
                second: '2-digit'
            };
            timeElement.textContent = now.toLocaleTimeString('en-US', timeOptions);
        }
    },

    // Initialize animations
    initializeAnimations() {
        // Add fade-in animation to main content
        const mainContent = document.querySelector('main');
        if (mainContent) {
            mainContent.classList.add('fade-in');
        }

        // Intersection Observer for scroll animations
        if ('IntersectionObserver' in window) {
            const observerOptions = {
                threshold: 0.1,
                rootMargin: '0px 0px -50px 0px'
            };

            const observer = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        entry.target.classList.add('slide-up');
                        observer.unobserve(entry.target);
                    }
                });
            }, observerOptions);

            // Observe cards and sections
            const animatedElements = document.querySelectorAll('.card, section');
            animatedElements.forEach(element => {
                observer.observe(element);
            });
        }
    },

    // Load user preferences from localStorage
    loadUserPreferences() {
        const preferences = localStorage.getItem('mis3010_preferences');
        if (preferences) {
            try {
                const prefs = JSON.parse(preferences);
                this.applyUserPreferences(prefs);
            } catch (e) {
                console.warn('Failed to load user preferences:', e);
            }
        }
    },

    // Apply user preferences
    applyUserPreferences(preferences) {
        // Apply theme preference
        if (preferences.theme) {
            document.documentElement.setAttribute('data-bs-theme', preferences.theme);
        }
        
        // Apply any other preferences
        if (preferences.animations === false) {
            document.body.classList.add('no-animations');
        }
    },

    // Save user preferences to localStorage
    saveUserPreferences(preferences) {
        try {
            localStorage.setItem('mis3010_preferences', JSON.stringify(preferences));
        } catch (e) {
            console.warn('Failed to save user preferences:', e);
        }
    },

    // API utility functions
    api: {
        // Generic API call function
        async call(endpoint, options = {}) {
            try {
                const response = await fetch(endpoint, {
                    headers: {
                        'Content-Type': 'application/json',
                        ...options.headers
                    },
                    ...options
                });

                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }

                return await response.json();
            } catch (error) {
                console.error('API call failed:', error);
                throw error;
            }
        },

        // Get current time from server
        async getTime() {
            return this.call('/api/time');
        },

        // Get users (admin only)
        async getUsers() {
            return this.call('/api/users');
        }
    },

    // Utility functions
    utils: {
        // Format date for display
        formatDate(date, options = {}) {
            const defaultOptions = {
                year: 'numeric',
                month: 'long',
                day: 'numeric'
            };
            return new Date(date).toLocaleDateString('en-US', { ...defaultOptions, ...options });
        },

        // Format time for display
        formatTime(date, options = {}) {
            const defaultOptions = {
                hour: '2-digit',
                minute: '2-digit',
                second: '2-digit',
                hour12: false
            };
            return new Date(date).toLocaleTimeString('en-US', { ...defaultOptions, ...options });
        },

        // Debounce function
        debounce(func, wait) {
            let timeout;
            return function executedFunction(...args) {
                const later = () => {
                    clearTimeout(timeout);
                    func(...args);
                };
                clearTimeout(timeout);
                timeout = setTimeout(later, wait);
            };
        },

        // Show notification (using Bootstrap alerts or custom implementation)
        showNotification(message, type = 'info', duration = 5000) {
            const alertContainer = document.getElementById('alert-container') || document.querySelector('.container');
            
            const alertElement = document.createElement('div');
            alertElement.className = `alert alert-${type} alert-dismissible fade show`;
            alertElement.innerHTML = `
                ${message}
                <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
            `;
            
            alertContainer.insertBefore(alertElement, alertContainer.firstChild);
            
            // Auto-remove after duration
            setTimeout(() => {
                if (alertElement.parentNode) {
                    alertElement.remove();
                }
            }, duration);
        },

        // Copy text to clipboard
        async copyToClipboard(text) {
            try {
                await navigator.clipboard.writeText(text);
                this.showNotification('Copied to clipboard!', 'success', 2000);
            } catch (err) {
                console.error('Failed to copy text: ', err);
                this.showNotification('Failed to copy to clipboard', 'danger', 3000);
            }
        }
    }
};

// Initialize app when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    MIS3010App.init();
});

// Handle page visibility changes
document.addEventListener('visibilitychange', () => {
    if (document.visibilityState === 'visible') {
        // Resume time updates when page becomes visible
        const timeElement = document.getElementById('current-time');
        if (timeElement) {
            MIS3010App.updateDateTime();
        }
    }
});

// Handle window resize for responsive features
window.addEventListener('resize', MIS3010App.utils.debounce(() => {
    // Handle any responsive adjustments
    MIS3010App.setupResponsiveNavigation();
}, 250));

// Export for use in other scripts
window.MIS3010App = MIS3010App;
