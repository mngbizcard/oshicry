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
 * Initialize work/character selection dependency and custom inputs
 */
function initWorkCharacterSelection() {
    const workSelect = document.getElementById('work-select');
    const characterSelect = document.getElementById('character-select');
    
    if (workSelect && characterSelect) {
        // Character data from server (this would normally be passed from the template)
        const characters = window.charactersData || {};
        
        workSelect.addEventListener('change', function() {
            const workId = this.value;
            
            // Handle custom work input
            const customWorkInput = document.getElementById('custom-work-input');
            const customWorkNote = document.getElementById('custom-work-note');
            if (workId === 'custom') {
                if (customWorkInput) customWorkInput.style.display = 'block';
                if (customWorkNote) customWorkNote.style.display = 'block';
                characterSelect.disabled = true;
                characterSelect.innerHTML = '<option value="">Select Character (Optional)</option>';
            } else {
                if (customWorkInput) customWorkInput.style.display = 'none';
                if (customWorkNote) customWorkNote.style.display = 'none';
            }
            
            // Clear character options
            characterSelect.innerHTML = '<option value="">Select Character (Optional)</option>';
            
            if (workId && workId !== 'custom') {
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
                
                // Add custom option
                const customOption = document.createElement('option');
                customOption.value = 'custom';
                customOption.textContent = 'Other/Custom';
                characterSelect.appendChild(customOption);
            } else if (workId !== 'custom') {
                characterSelect.disabled = true;
            }
        });
        
        // Handle custom character input
        characterSelect.addEventListener('change', function() {
            const characterId = this.value;
            const customCharacterInput = document.getElementById('custom-character-input');
            const customCharacterNote = document.getElementById('custom-character-note');
            
            if (characterId === 'custom') {
                if (customCharacterInput) customCharacterInput.style.display = 'block';
                if (customCharacterNote) customCharacterNote.style.display = 'block';
            } else {
                if (customCharacterInput) customCharacterInput.style.display = 'none';
                if (customCharacterNote) customCharacterNote.style.display = 'none';
            }
        });
    }
    
    // Handle custom scene input
    const sceneSelect = document.getElementById('scene-select');
    if (sceneSelect) {
        sceneSelect.addEventListener('change', function() {
            const sceneValue = this.value;
            const customSceneInput = document.getElementById('custom-scene-input');
            const customSceneNote = document.getElementById('custom-scene-note');
            
            if (sceneValue === 'custom') {
                if (customSceneInput) customSceneInput.style.display = 'block';
                if (customSceneNote) customSceneNote.style.display = 'block';
            } else {
                if (customSceneInput) customSceneInput.style.display = 'none';
                if (customSceneNote) customSceneNote.style.display = 'none';
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
            
            // Handle custom work input
            const customWorkInput = document.getElementById('modal-custom-work-input');
            const customWorkNote = document.getElementById('modal-custom-work-note');
            if (workId === 'custom') {
                if (customWorkInput) customWorkInput.style.display = 'block';
                if (customWorkNote) customWorkNote.style.display = 'block';
                modalCharacterSelect.disabled = true;
                modalCharacterSelect.innerHTML = '<option value="">Select Character</option>';
            } else {
                if (customWorkInput) customWorkInput.style.display = 'none';
                if (customWorkNote) customWorkNote.style.display = 'none';
            }
            
            // Clear character options
            modalCharacterSelect.innerHTML = '<option value="">Select Character</option>';
            
            if (workId && workId !== 'custom') {
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
                
                // Add custom option
                const customOption = document.createElement('option');
                customOption.value = 'custom';
                customOption.textContent = 'Other/Custom';
                modalCharacterSelect.appendChild(customOption);
            } else if (workId !== 'custom') {
                modalCharacterSelect.disabled = true;
            }
        });
        
        // Handle custom character input
        modalCharacterSelect.addEventListener('change', function() {
            const characterId = this.value;
            const customCharacterInput = document.getElementById('modal-custom-character-input');
            const customCharacterNote = document.getElementById('modal-custom-character-note');
            
            if (characterId === 'custom') {
                if (customCharacterInput) customCharacterInput.style.display = 'block';
                if (customCharacterNote) customCharacterNote.style.display = 'block';
            } else {
                if (customCharacterInput) customCharacterInput.style.display = 'none';
                if (customCharacterNote) customCharacterNote.style.display = 'none';
            }
        });
    }
    
    // Handle custom scene input for modal
    const modalSceneSelect = document.getElementById('modal-scene-select');
    if (modalSceneSelect) {
        modalSceneSelect.addEventListener('change', function() {
            const sceneValue = this.value;
            const customSceneInput = document.getElementById('modal-custom-scene-input');
            const customSceneNote = document.getElementById('modal-custom-scene-note');
            
            if (sceneValue === 'custom') {
                if (customSceneInput) customSceneInput.style.display = 'block';
                if (customSceneNote) customSceneNote.style.display = 'block';
            } else {
                if (customSceneInput) customSceneInput.style.display = 'none';
                if (customSceneNote) customSceneNote.style.display = 'none';
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
    const originalContent = submitButton.cloneNode(true);
    
    // Clear button and add loading state using safe DOM methods
    submitButton.textContent = '';
    const spinner = document.createElement('i');
    spinner.className = 'fas fa-spinner fa-spin me-1';
    const text = document.createTextNode('Posting...');
    submitButton.appendChild(spinner);
    submitButton.appendChild(text);
    submitButton.disabled = true;
    
    // Re-enable after form submission (this would normally be handled by page reload)
    setTimeout(() => {
        submitButton.textContent = '';
        while (originalContent.firstChild) {
            submitButton.appendChild(originalContent.firstChild.cloneNode(true));
        }
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

/**
 * Initialize translation functionality
 */
function initTranslation() {
    // Handle translate button clicks
    document.addEventListener('click', function(e) {
        if (e.target.closest('.translate-btn')) {
            const button = e.target.closest('.translate-btn');
            const postId = button.dataset.postId;
            const content = button.dataset.content;
            const currentLang = document.documentElement.lang || 'en';
            
            // Show loading state
            button.innerHTML = '<i class="fas fa-spinner fa-spin me-1"></i>Translating...';
            button.disabled = true;
            
            // Simulate translation with placeholder
            setTimeout(() => {
                const translatedText = translateText(content, currentLang);
                showTranslation(postId, translatedText);
                
                // Reset button
                button.innerHTML = '<i class="fas fa-language me-1"></i>Translate';
                button.disabled = false;
            }, 1000);
        }
        
        if (e.target.closest('.hide-translation-btn')) {
            const button = e.target.closest('.hide-translation-btn');
            const postId = button.dataset.postId;
            hideTranslation(postId);
        }
    });
}

/**
 * Placeholder translation function
 * In production, this would call a real translation API
 */
function translateText(text, currentLang) {
    // Simple placeholder translations for demo
    const translations = {
        'en_to_ja': {
            "Gojo's domain expansion is literally the most beautiful thing in anime! The visual effects are insane! 🔥": "五条の領域展開は文字通りアニメで最も美しいものです！視覚効果が狂っています！🔥",
            "Yuji's character development this season has me crying every episode... he deserves the world 😭": "虎杖の今シーズンのキャラクター開発は毎回泣かせます...彼は世界に値します😭",
            "That final scene with Eren... I'm still not over it. What a masterpiece of storytelling!": "エレンとの最終シーン...まだ立ち直れていません。何という物語の傑作でしょう！",
            "Tanjiro's kindness towards demons makes him the best protagonist in shounen anime!": "炭治郎の悪魔に対する優しさは、彼を少年アニメで最高の主人公にしています！"
        },
        'ja_to_en': {
            "禰豆子ちゃんが可愛すぎる！保護したい！": "Nezuko-chan is too cute! I want to protect her!",
            "五条先生最高です！": "Gojo-sensei is the best!",
            "進撃の巨人の最終回を見た後、まだ泣いています。。。": "I'm still crying after watching the final episode of Attack on Titan...",
            "新しいアニメシーズンが楽しみです！皆さんのおすすめはありますか？": "I'm looking forward to the new anime season! Do you have any recommendations?"
        }
    };
    
    const targetLang = currentLang === 'ja' ? 'en' : 'ja';
    const translationKey = currentLang === 'ja' ? 'ja_to_en' : 'en_to_ja';
    
    // Try to find exact match first
    if (translations[translationKey][text]) {
        return translations[translationKey][text];
    }
    
    // Fallback: simple placeholder based on detected content
    if (targetLang === 'ja') {
        if (text.includes('Gojo') || text.includes('gojo')) {
            return "五条について: " + text.substring(0, 50) + "... [Translation placeholder]";
        } else if (text.includes('anime') || text.includes('character')) {
            return "アニメについて: " + text.substring(0, 50) + "... [Translation placeholder]";
        } else {
            return "翻訳: " + text.substring(0, 50) + "... [Translation placeholder]";
        }
    } else {
        if (text.includes('五条') || text.includes('ゴジョウ')) {
            return "About Gojo: " + text.substring(0, 50) + "... [Translation placeholder]";
        } else if (text.includes('アニメ') || text.includes('キャラ')) {
            return "About anime: " + text.substring(0, 50) + "... [Translation placeholder]";
        } else {
            return "Translation: " + text.substring(0, 50) + "... [Translation placeholder]";
        }
    }
}

/**
 * Show translation for a post
 */
function showTranslation(postId, translatedText) {
    const translationContainer = document.getElementById(`translation-${postId}`);
    const translationTextElement = document.getElementById(`translation-text-${postId}`);
    
    if (translationContainer && translationTextElement) {
        translationTextElement.textContent = translatedText;
        translationContainer.style.display = 'block';
    }
}

/**
 * Hide translation for a post
 */
function hideTranslation(postId) {
    const translationContainer = document.getElementById(`translation-${postId}`);
    if (translationContainer) {
        translationContainer.style.display = 'none';
    }
}

// Initialize everything when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    initCharacterCounter();
    initWorkCharacterSelection();
    initModalForm();
    initFlashMessages();
    initAnimeInteractions();
    initTranslation();
});

// Export functions for potential use by other scripts
window.OshiCRY = {
    formatRelativeTime,
    createSparkleEffect,
    initCharacterCounter,
    initWorkCharacterSelection,
    initTranslation
};
