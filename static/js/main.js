// OshiCRY - Main JavaScript File

document.addEventListener('DOMContentLoaded', function() {
    // Character counter for post forms
    initCharacterCounter();
    
    // Work/Character selection dependency
    initWorkCharacterSelection();
    
    // Modal form functionality
    initModalForm();
    
    // Auto-hide flash messages
    initFlashMessages();
    
    // Initialize tooltips if Bootstrap tooltips are available
    initTooltips();
    
    // Add anime-style interactions
    initAnimeInteractions();
});

/**
 * Initialize character counter for textareas
 */
function initCharacterCounter() {
    const textareas = document.querySelectorAll('textarea[maxlength]');
    
    textareas.forEach(textarea => {
        const maxLength = parseInt(textarea.getAttribute('maxlength'));
        const charCountElement = document.getElementById('char-count') || document.getElementById('modal-char-count');
        
        if (charCountElement) {
            // Update counter on input
            textarea.addEventListener('input', function() {
                const remaining = maxLength - this.value.length;
                charCountElement.textContent = remaining;
                
                // Add warning/danger classes
                charCountElement.classList.remove('warning', 'danger');
                if (remaining < 50) {
                    charCountElement.classList.add('warning');
                }
                if (remaining < 20) {
                    charCountElement.classList.remove('warning');
                    charCountElement.classList.add('danger');
                }
            });
        }
    });
}

/**
 * Initialize work/character selection dependency
 */
function initWorkCharacterSelection() {
    const workSelect = document.getElementById('work-select');
    const characterSelect = document.getElementById('character-select');
    
    if (workSelect && characterSelect) {
        // Character data from server (this would normally be passed from the template)
        const characters = window.charactersData || {};
        
        workSelect.addEventListener('change', function() {
            const workId = this.value;
            
            // Clear character options
            characterSelect.innerHTML = '<option value="">Select Character (Optional)</option>';
            
            if (workId) {
                characterSelect.disabled = false;
                
                // Add characters for selected work
                Object.values(characters).forEach(character => {
                    if (character.work_id == workId) {
                        const option = document.createElement('option');
                        option.value = character.id;
                        option.textContent = character.name;
                        characterSelect.appendChild(option);
                    }
                });
            } else {
                characterSelect.disabled = true;
            }
        });
    }
}

/**
 * Initialize modal form functionality
 */
function initModalForm() {
    const modalWorkSelect = document.getElementById('modal-work-select');
    const modalCharacterSelect = document.getElementById('modal-character-select');
    const modalTextarea = document.querySelector('#createPostModal textarea[maxlength]');
    const modalCharCount = document.getElementById('modal-char-count');
    
    // Modal work/character selection
    if (modalWorkSelect && modalCharacterSelect) {
        const characters = window.charactersData || {};
        
        modalWorkSelect.addEventListener('change', function() {
            const workId = this.value;
            
            // Clear character options
            modalCharacterSelect.innerHTML = '<option value="">Select Character</option>';
            
            if (workId) {
                modalCharacterSelect.disabled = false;
                
                // Add characters for selected work
                Object.values(characters).forEach(character => {
                    if (character.work_id == workId) {
                        const option = document.createElement('option');
                        option.value = character.id;
                        option.textContent = character.name;
                        modalCharacterSelect.appendChild(option);
                    }
                });
            } else {
                modalCharacterSelect.disabled = true;
            }
        });
    }
    
    // Modal character counter
    if (modalTextarea && modalCharCount) {
        const maxLength = parseInt(modalTextarea.getAttribute('maxlength'));
        
        modalTextarea.addEventListener('input', function() {
            const remaining = maxLength - this.value.length;
            modalCharCount.textContent = remaining;
            
            // Add warning/danger classes
            modalCharCount.classList.remove('warning', 'danger');
            if (remaining < 50) {
                modalCharCount.classList.add('warning');
            }
            if (remaining < 20) {
                modalCharCount.classList.remove('warning');
                modalCharCount.classList.add('danger');
            }
        });
    }
    
    // Reset modal form when closed
    const modal = document.getElementById('createPostModal');
    if (modal) {
        modal.addEventListener('hidden.bs.modal', function() {
            const form = modal.querySelector('form');
            if (form) {
                form.reset();
                if (modalCharacterSelect) {
                    modalCharacterSelect.disabled = true;
                    modalCharacterSelect.innerHTML = '<option value="">Select Character</option>';
                }
                if (modalCharCount) {
                    modalCharCount.textContent = '280';
                    modalCharCount.classList.remove('warning', 'danger');
                }
            }
        });
    }
}

/**
 * Initialize flash message auto-hide
 */
function initFlashMessages() {
    const alerts = document.querySelectorAll('.alert');
    
    alerts.forEach(alert => {
        // Auto-hide success and info messages after 5 seconds
        if (alert.classList.contains('alert-success') || alert.classList.contains('alert-info')) {
            setTimeout(() => {
                const bsAlert = new bootstrap.Alert(alert);
                bsAlert.close();
            }, 5000);
        }
    });
}

/**
 * Initialize Bootstrap tooltips
 */
function initTooltips() {
    if (typeof bootstrap !== 'undefined' && bootstrap.Tooltip) {
        const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
        tooltipTriggerList.map(function(tooltipTriggerEl) {
            return new bootstrap.Tooltip(tooltipTriggerEl);
        });
    }
}

/**
 * Add anime-style interactions
 */
function initAnimeInteractions() {
    // Add sparkle effect to buttons on click
    const buttons = document.querySelectorAll('.btn-primary');
    
    buttons.forEach(button => {
        button.addEventListener('click', function(e) {
            createSparkleEffect(e.target);
        });
    });
    
    // Add floating animation to empty state icons
    const emptyIcons = document.querySelectorAll('.empty-state i');
    emptyIcons.forEach(icon => {
        icon.style.animation = 'float 3s ease-in-out infinite';
    });
    
    // Add hover effect to post cards
    const postCards = document.querySelectorAll('.post-card');
    postCards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-4px)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
        });
    });
}

/**
 * Create sparkle effect for button clicks
 */
function createSparkleEffect(element) {
    const sparkle = document.createElement('div');
    sparkle.className = 'sparkle-effect';
    sparkle.style.cssText = `
        position: absolute;
        width: 4px;
        height: 4px;
        background: #fff;
        border-radius: 50%;
        pointer-events: none;
        animation: sparkle 0.6s ease-out forwards;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        z-index: 1000;
    `;
    
    element.style.position = 'relative';
    element.appendChild(sparkle);
    
    // Create multiple sparkles
    for (let i = 0; i < 5; i++) {
        setTimeout(() => {
            const spark = sparkle.cloneNode();
            spark.style.left = Math.random() * 100 + '%';
            spark.style.top = Math.random() * 100 + '%';
            element.appendChild(spark);
            
            setTimeout(() => {
                if (spark.parentNode) {
                    spark.parentNode.removeChild(spark);
                }
            }, 600);
        }, i * 100);
    }
    
    setTimeout(() => {
        if (sparkle.parentNode) {
            sparkle.parentNode.removeChild(sparkle);
        }
    }, 600);
}

/**
 * Format relative time for posts
 */
function formatRelativeTime(dateString) {
    const date = new Date(dateString);
    const now = new Date();
    const diffInSeconds = Math.floor((now - date) / 1000);
    
    if (diffInSeconds < 60) return 'just now';
    if (diffInSeconds < 3600) return Math.floor(diffInSeconds / 60) + 'm';
    if (diffInSeconds < 86400) return Math.floor(diffInSeconds / 3600) + 'h';
    if (diffInSeconds < 604800) return Math.floor(diffInSeconds / 86400) + 'd';
    
    return date.toLocaleDateString();
}

/**
 * Handle form submission with loading state
 */
function handleFormSubmission(form) {
    const submitButton = form.querySelector('button[type="submit"]');
    const originalText = submitButton.innerHTML;
    
    submitButton.innerHTML = '<i class="fas fa-spinner fa-spin me-1"></i>Posting...';
    submitButton.disabled = true;
    
    // Re-enable after form submission (this would normally be handled by page reload)
    setTimeout(() => {
        submitButton.innerHTML = originalText;
        submitButton.disabled = false;
    }, 2000);
}

/**
 * Add CSS animations
 */
const style = document.createElement('style');
style.textContent = `
    @keyframes sparkle {
        0% {
            transform: translate(-50%, -50%) scale(1);
            opacity: 1;
        }
        100% {
            transform: translate(-50%, -50%) scale(0) translateY(-20px);
            opacity: 0;
        }
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
    }
    
    .btn-primary {
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    .btn-primary:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(139, 92, 246, 0.3);
    }
    
    .btn-primary:active {
        transform: translateY(0);
    }
    
    .post-card {
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    .avatar-circle {
        transition: all 0.3s ease;
    }
    
    .avatar-circle:hover {
        transform: scale(1.1);
    }
`;

document.head.appendChild(style);

/**
 * Lazy loading for images (if implemented later)
 */
function initLazyLoading() {
    if ('IntersectionObserver' in window) {
        const imageObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    img.src = img.dataset.src;
                    img.classList.remove('lazy');
                    observer.unobserve(img);
                }
            });
        });
        
        document.querySelectorAll('img[data-src]').forEach(img => {
            imageObserver.observe(img);
        });
    }
}

/**
 * PWA-like features for mobile
 */
if ('serviceWorker' in navigator && window.location.protocol === 'https:') {
    // Service worker would be registered here for PWA features
    console.log('Service Worker support detected');
}

/**
 * Keyboard shortcuts
 */
document.addEventListener('keydown', function(e) {
    // Ctrl/Cmd + Enter to submit post forms
    if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
        const activeElement = document.activeElement;
        if (activeElement.tagName === 'TEXTAREA') {
            const form = activeElement.closest('form');
            if (form) {
                form.submit();
            }
        }
    }
});

/**
 * Character data for work/character selection
 * This would normally be populated from the server
 */
window.charactersData = {};

// Export functions for potential use by other scripts
window.OshiCRY = {
    formatRelativeTime,
    createSparkleEffect,
    initCharacterCounter,
    initWorkCharacterSelection
};
