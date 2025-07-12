// ReWear - Main JavaScript functionality
// Handles UI interactions, animations, and user experience enhancements

document.addEventListener('DOMContentLoaded', function() {
    // Initialize all functionality
    initNavigation();
    initFlashMessages();
    initFormEnhancements();
    initImagePreviews();
    initAnimations();
    initItemCards();
    initUserMenu();
});

// Navigation functionality
function initNavigation() {
    const navToggle = document.getElementById('navToggle');
    const navMenu = document.getElementById('navMenu');
    
    if (navToggle && navMenu) {
        navToggle.addEventListener('click', function() {
            navMenu.classList.toggle('active');
            navToggle.classList.toggle('active');
            
            // Animate hamburger menu
            const spans = navToggle.querySelectorAll('span');
            spans.forEach((span, index) => {
                if (navToggle.classList.contains('active')) {
                    if (index === 0) span.style.transform = 'rotate(45deg) translate(5px, 5px)';
                    if (index === 1) span.style.opacity = '0';
                    if (index === 2) span.style.transform = 'rotate(-45deg) translate(7px, -6px)';
                } else {
                    span.style.transform = 'none';
                    span.style.opacity = '1';
                }
            });
        });
        
        // Close menu when clicking on a link
        const navLinks = navMenu.querySelectorAll('.nav-link');
        navLinks.forEach(link => {
            link.addEventListener('click', () => {
                navMenu.classList.remove('active');
                navToggle.classList.remove('active');
            });
        });
        
        // Close menu when clicking outside
        document.addEventListener('click', function(event) {
            if (!navToggle.contains(event.target) && !navMenu.contains(event.target)) {
                navMenu.classList.remove('active');
                navToggle.classList.remove('active');
            }
        });
    }
}

// Flash messages functionality
function initFlashMessages() {
    const flashMessages = document.querySelectorAll('.flash-message');
    
    flashMessages.forEach(message => {
        // Auto-dismiss after 5 seconds
        setTimeout(() => {
            dismissFlashMessage(message);
        }, 5000);
        
        // Close button functionality
        const closeBtn = message.querySelector('.flash-close');
        if (closeBtn) {
            closeBtn.addEventListener('click', () => {
                dismissFlashMessage(message);
            });
        }
        
        // Animate in
        message.style.opacity = '0';
        message.style.transform = 'translateX(100%)';
        
        setTimeout(() => {
            message.style.transition = 'all 0.3s ease';
            message.style.opacity = '1';
            message.style.transform = 'translateX(0)';
        }, 100);
    });
}

function dismissFlashMessage(message) {
    message.style.transform = 'translateX(100%)';
    message.style.opacity = '0';
    
    setTimeout(() => {
        if (message.parentNode) {
            message.parentNode.removeChild(message);
        }
    }, 300);
}

// Form enhancements
function initFormEnhancements() {
    // File input styling
    const fileInputs = document.querySelectorAll('input[type="file"]');
    fileInputs.forEach(input => {
        const label = input.nextElementSibling;
        if (label && label.classList.contains('file-label')) {
            input.addEventListener('change', function() {
                const fileName = this.files[0] ? this.files[0].name : 'Choose file';
                const span = label.querySelector('span');
                if (span) {
                    span.textContent = fileName;
                }
            });
        }
    });
    
    // Form validation enhancements
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const requiredFields = form.querySelectorAll('[required]');
            let isValid = true;
            
            requiredFields.forEach(field => {
                if (!field.value.trim()) {
                    isValid = false;
                    field.classList.add('error');
                    
                    // Remove error class after user starts typing
                    field.addEventListener('input', function() {
                        this.classList.remove('error');
                    });
                }
            });
            
            if (!isValid) {
                e.preventDefault();
                showNotification('Please fill in all required fields', 'error');
            }
        });
    });
    
    // Password strength indicator
    const passwordInputs = document.querySelectorAll('input[type="password"]');
    passwordInputs.forEach(input => {
        if (input.name === 'password') {
            input.addEventListener('input', function() {
                const strength = calculatePasswordStrength(this.value);
                showPasswordStrength(this, strength);
            });
        }
    });
}

function calculatePasswordStrength(password) {
    let strength = 0;
    if (password.length >= 8) strength++;
    if (password.match(/[a-z]/)) strength++;
    if (password.match(/[A-Z]/)) strength++;
    if (password.match(/[0-9]/)) strength++;
    if (password.match(/[^a-zA-Z0-9]/)) strength++;
    
    return strength;
}

function showPasswordStrength(input, strength) {
    let indicator = input.parentNode.querySelector('.password-strength');
    if (!indicator) {
        indicator = document.createElement('div');
        indicator.className = 'password-strength';
        input.parentNode.appendChild(indicator);
    }
    
    const labels = ['Very Weak', 'Weak', 'Fair', 'Good', 'Strong'];
    const colors = ['#f44336', '#ff9800', '#ffc107', '#4caf50', '#2196f3'];
    
    indicator.textContent = labels[strength] || '';
    indicator.style.color = colors[strength] || '#666';
    indicator.style.fontSize = '0.8rem';
    indicator.style.marginTop = '0.25rem';
}

// Image preview functionality
function initImagePreviews() {
    const imageInputs = document.querySelectorAll('input[type="file"][accept*="image"]');
    
    imageInputs.forEach(input => {
        input.addEventListener('change', function(e) {
            const file = e.target.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = function(e) {
                    showImagePreview(input, e.target.result);
                };
                reader.readAsDataURL(file);
            }
        });
    });
}

function showImagePreview(input, src) {
    let preview = input.parentNode.querySelector('.image-preview');
    if (!preview) {
        preview = document.createElement('div');
        preview.className = 'image-preview';
        preview.style.cssText = `
            margin-top: 1rem;
            text-align: center;
        `;
        input.parentNode.appendChild(preview);
    }
    
    preview.innerHTML = `
        <img src="${src}" alt="Preview" style="
            max-width: 200px;
            max-height: 200px;
            border-radius: 8px;
            border: 2px solid var(--border-color);
            object-fit: cover;
        ">
        <p style="
            margin-top: 0.5rem;
            font-size: 0.9rem;
            color: var(--text-secondary);
        ">Image preview</p>
    `;
}

// Animations and transitions
function initAnimations() {
    // Scroll-triggered animations
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate-in');
            }
        });
    }, observerOptions);
    
    // Observe elements that should animate on scroll
    const animateElements = document.querySelectorAll('.item-card, .step-card, .stat-card');
    animateElements.forEach(el => {
        observer.observe(el);
    });
    
    // Smooth scrolling for anchor links
    const anchorLinks = document.querySelectorAll('a[href^="#"]');
    anchorLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
}

// Item card interactions
function initItemCards() {
    const itemCards = document.querySelectorAll('.item-card');
    
    itemCards.forEach(card => {
        // Add hover effect with mouse movement
        card.addEventListener('mousemove', function(e) {
            const rect = card.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;
            
            const centerX = rect.width / 2;
            const centerY = rect.height / 2;
            
            const rotateX = (y - centerY) / 20;
            const rotateY = (centerX - x) / 20;
            
            card.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) translateZ(10px)`;
        });
        
        card.addEventListener('mouseleave', function() {
            card.style.transform = 'perspective(1000px) rotateX(0deg) rotateY(0deg) translateZ(0px)';
        });
        
        // Add click animation
        card.addEventListener('click', function() {
            card.style.transform = 'scale(0.95)';
            setTimeout(() => {
                card.style.transform = '';
            }, 150);
        });
    });
}

// User menu functionality
function initUserMenu() {
    const userMenus = document.querySelectorAll('.user-menu');
    
    userMenus.forEach(menu => {
        const button = menu.querySelector('.user-btn');
        const dropdown = menu.querySelector('.dropdown');
        
        if (button && dropdown) {
            button.addEventListener('click', function(e) {
                e.stopPropagation();
                dropdown.style.display = dropdown.style.display === 'block' ? 'none' : 'block';
            });
            
            // Close dropdown when clicking outside
            document.addEventListener('click', function() {
                dropdown.style.display = 'none';
            });
        }
    });
}

// Utility functions
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `flash-message flash-${type}`;
    notification.innerHTML = `
        <span>${message}</span>
        <button class="flash-close">&times;</button>
    `;
    
    const container = document.querySelector('.flash-messages') || createFlashContainer();
    container.appendChild(notification);
    
    // Auto-dismiss
    setTimeout(() => {
        dismissFlashMessage(notification);
    }, 5000);
    
    // Close button
    const closeBtn = notification.querySelector('.flash-close');
    closeBtn.addEventListener('click', () => {
        dismissFlashMessage(notification);
    });
}

function createFlashContainer() {
    const container = document.createElement('div');
    container.className = 'flash-messages';
    document.body.appendChild(container);
    return container;
}

// Image gallery functionality for item details
function initImageGallery() {
    const thumbnails = document.querySelectorAll('.thumbnail');
    const mainImage = document.getElementById('mainImage');
    
    thumbnails.forEach(thumbnail => {
        thumbnail.addEventListener('click', function() {
            if (mainImage) {
                mainImage.src = this.src;
                
                // Update active thumbnail
                thumbnails.forEach(t => t.classList.remove('active'));
                this.classList.add('active');
            }
        });
    });
}

// Initialize image gallery if on item detail page
if (document.getElementById('mainImage')) {
    initImageGallery();
}

// Loading states for forms
function initLoadingStates() {
    const forms = document.querySelectorAll('form');
    
    forms.forEach(form => {
        form.addEventListener('submit', function() {
            const submitBtn = form.querySelector('button[type="submit"], input[type="submit"]');
            if (submitBtn) {
                submitBtn.disabled = true;
                const originalText = submitBtn.textContent || submitBtn.value;
                
                if (submitBtn.tagName === 'BUTTON') {
                    submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Loading...';
                } else {
                    submitBtn.value = 'Loading...';
                }
                
                // Re-enable after 10 seconds as fallback
                setTimeout(() => {
                    submitBtn.disabled = false;
                    if (submitBtn.tagName === 'BUTTON') {
                        submitBtn.textContent = originalText;
                    } else {
                        submitBtn.value = originalText;
                    }
                }, 10000);
            }
        });
    });
}

// Initialize loading states
initLoadingStates();

// Keyboard navigation enhancements
document.addEventListener('keydown', function(e) {
    // Close flash messages with Escape key
    if (e.key === 'Escape') {
        const flashMessages = document.querySelectorAll('.flash-message');
        flashMessages.forEach(message => {
            dismissFlashMessage(message);
        });
    }
    
    // Quick navigation shortcuts
    if (e.ctrlKey || e.metaKey) {
        switch(e.key) {
            case 'k':
                e.preventDefault();
                const searchInput = document.querySelector('input[name="search"]');
                if (searchInput) {
                    searchInput.focus();
                }
                break;
        }
    }
});

// Add custom CSS for animations
const animationStyles = `
    .animate-in {
        animation: fadeInUp 0.6s ease-out;
    }
    
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .item-card {
        transition: transform 0.3s ease;
    }
    
    .form-input.error {
        border-color: var(--error-color);
        box-shadow: 0 0 0 2px rgba(244, 67, 54, 0.2);
    }
    
    .thumbnail.active {
        border-color: var(--primary-color);
        box-shadow: 0 0 0 2px rgba(0, 212, 255, 0.3);
    }
`;

// Inject animation styles
const styleSheet = document.createElement('style');
styleSheet.textContent = animationStyles;
document.head.appendChild(styleSheet);

// Initialize particles.js configuration for pages that need it
window.particlesConfig = {
    particles: {
        number: { value: 80, density: { enable: true, value_area: 800 } },
        color: { value: '#ffffff' },
        shape: { type: 'circle' },
        opacity: { value: 0.5, random: false },
        size: { value: 3, random: true },
        line_linked: {
            enable: true,
            distance: 150,
            color: '#ffffff',
            opacity: 0.4,
            width: 1
        },
        move: {
            enable: true,
            speed: 6,
            direction: 'none',
            random: false,
            straight: false,
            out_mode: 'out',
            bounce: false
        }
    },
    interactivity: {
        detect_on: 'canvas',
        events: {
            onhover: { enable: true, mode: 'repulse' },
            onclick: { enable: true, mode: 'push' },
            resize: true
        }
    },
    retina_detect: true
};

// Debug information in development
if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
    console.log('ReWear - Community Clothing Exchange');
    console.log('JavaScript initialized successfully');
}
