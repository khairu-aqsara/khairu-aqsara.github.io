// Main JavaScript bundle for personal blog
// Contains core functionality and interactive features

(function() {
    'use strict';

    // DOM Ready function
    function ready(fn) {
        if (document.readyState === 'complete' || document.readyState === 'interactive') {
            setTimeout(fn, 1);
        } else {
            document.addEventListener('DOMContentLoaded', fn);
        }
    }

    // Theme Management
    const ThemeManager = {
        init() {
            this.applyTheme();
            this.bindEvents();
        },

        getTheme() {
            return localStorage.getItem('theme') || 'auto';
        },

        setTheme(theme) {
            localStorage.setItem('theme', theme);
            this.applyTheme();
        },

        applyTheme() {
            const theme = this.getTheme();
            const isDark = theme === 'dark' || 
                (theme === 'auto' && window.matchMedia('(prefers-color-scheme: dark)').matches);
            
            document.documentElement.setAttribute('data-theme', isDark ? 'dark' : 'light');
            document.body.classList.toggle('dark', isDark);
        },

        bindEvents() {
            // Listen for system theme changes
            window.matchMedia('(prefers-color-scheme: dark)')
                .addEventListener('change', () => {
                    if (this.getTheme() === 'auto') {
                        this.applyTheme();
                    }
                });

            // Theme toggle button
            const themeToggle = document.querySelector('#theme-toggle');
            if (themeToggle) {
                themeToggle.addEventListener('click', () => {
                    const currentTheme = this.getTheme();
                    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
                    this.setTheme(newTheme);
                });
            }
        }
    };

    // Smooth Scrolling for anchor links
    const SmoothScroll = {
        init() {
            document.querySelectorAll('a[href^="#"]').forEach(anchor => {
                anchor.addEventListener('click', (e) => {
                    const href = anchor.getAttribute('href');
                    if (href === '#') return;
                    
                    const target = document.querySelector(href);
                    if (target) {
                        e.preventDefault();
                        target.scrollIntoView({
                            behavior: 'smooth',
                            block: 'start'
                        });
                        
                        // Update URL without jumping
                        history.pushState(null, null, href);
                    }
                });
            });
        }
    };

    // Copy Code Functionality
    const CodeCopy = {
        init() {
            document.querySelectorAll('pre code').forEach(block => {
                this.addCopyButton(block);
            });
        },

        addCopyButton(codeBlock) {
            const pre = codeBlock.parentNode;
            const button = document.createElement('button');
            
            button.className = 'copy-code-btn';
            button.textContent = 'Copy';
            button.setAttribute('aria-label', 'Copy code to clipboard');
            
            button.addEventListener('click', () => {
                this.copyCode(codeBlock, button);
            });
            
            pre.style.position = 'relative';
            pre.appendChild(button);
        },

        async copyCode(codeBlock, button) {
            const code = codeBlock.textContent;
            
            try {
                await navigator.clipboard.writeText(code);
                button.textContent = 'Copied!';
                button.classList.add('copied');
                
                setTimeout(() => {
                    button.textContent = 'Copy';
                    button.classList.remove('copied');
                }, 2000);
            } catch (err) {
                console.error('Failed to copy code:', err);
                button.textContent = 'Failed';
                
                setTimeout(() => {
                    button.textContent = 'Copy';
                }, 2000);
            }
        }
    };

    // Reading Progress Indicator
    const ReadingProgress = {
        init() {
            if (!document.querySelector('.post-content')) return;
            
            this.createProgressBar();
            this.updateProgress();
            window.addEventListener('scroll', () => this.updateProgress());
        },

        createProgressBar() {
            const progressBar = document.createElement('div');
            progressBar.className = 'reading-progress';
            progressBar.innerHTML = '<div class="reading-progress-fill"></div>';
            document.body.appendChild(progressBar);
        },

        updateProgress() {
            const article = document.querySelector('.post-content');
            if (!article) return;
            
            const articleTop = article.offsetTop;
            const articleHeight = article.offsetHeight;
            const scrollTop = window.pageYOffset;
            const windowHeight = window.innerHeight;
            
            const progress = Math.min(100, Math.max(0, 
                ((scrollTop - articleTop + windowHeight) / articleHeight) * 100
            ));
            
            const fill = document.querySelector('.reading-progress-fill');
            if (fill) {
                fill.style.width = `${progress}%`;
            }
        }
    };

    // Back to Top Button
    const BackToTop = {
        init() {
            this.createButton();
            this.bindEvents();
        },

        createButton() {
            const button = document.createElement('button');
            button.className = 'back-to-top';
            button.innerHTML = '↑';
            button.setAttribute('aria-label', 'Back to top');
            button.style.display = 'none';
            document.body.appendChild(button);
        },

        bindEvents() {
            const button = document.querySelector('.back-to-top');
            if (!button) return;

            // Show/hide on scroll
            window.addEventListener('scroll', () => {
                if (window.pageYOffset > 300) {
                    button.style.display = 'flex';
                } else {
                    button.style.display = 'none';
                }
            });

            // Scroll to top on click
            button.addEventListener('click', () => {
                window.scrollTo({
                    top: 0,
                    behavior: 'smooth'
                });
            });
        }
    };

    // External Link Handler
    const ExternalLinks = {
        init() {
            document.querySelectorAll('a[href^="http"]').forEach(link => {
                if (!link.href.includes(window.location.hostname)) {
                    link.setAttribute('target', '_blank');
                    link.setAttribute('rel', 'noopener noreferrer');
                    link.setAttribute('aria-label', `${link.textContent} (opens in new tab)`);
                }
            });
        }
    };

    // Image Lazy Loading (for older browsers)
    const LazyLoading = {
        init() {
            if ('IntersectionObserver' in window) {
                this.setupIntersectionObserver();
            } else {
                // Fallback for older browsers
                this.loadAllImages();
            }
        },

        setupIntersectionObserver() {
            const images = document.querySelectorAll('img[data-src]');
            
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

            images.forEach(img => imageObserver.observe(img));
        },

        loadAllImages() {
            document.querySelectorAll('img[data-src]').forEach(img => {
                img.src = img.dataset.src;
                img.classList.remove('lazy');
            });
        }
    };

    // Search functionality (if search is enabled)
    const Search = {
        init() {
            const searchInput = document.querySelector('#search-input');
            const searchResults = document.querySelector('#search-results');
            
            if (!searchInput || !searchResults) return;
            
            this.loadSearchIndex().then(() => {
                this.bindEvents();
            });
        },

        async loadSearchIndex() {
            try {
                const response = await fetch('/index.json');
                this.searchIndex = await response.json();
            } catch (error) {
                console.error('Failed to load search index:', error);
                this.searchIndex = [];
            }
        },

        bindEvents() {
            const searchInput = document.querySelector('#search-input');
            let searchTimeout;

            searchInput.addEventListener('input', (e) => {
                clearTimeout(searchTimeout);
                searchTimeout = setTimeout(() => {
                    this.performSearch(e.target.value);
                }, 300);
            });
        },

        performSearch(query) {
            const results = document.querySelector('#search-results');
            if (!query.trim()) {
                results.innerHTML = '';
                return;
            }

            const matches = this.searchIndex.filter(item => 
                item.title.toLowerCase().includes(query.toLowerCase()) ||
                item.content.toLowerCase().includes(query.toLowerCase())
            ).slice(0, 10);

            if (matches.length === 0) {
                results.innerHTML = '<p>No results found.</p>';
                return;
            }

            results.innerHTML = matches.map(match => `
                <div class="search-result">
                    <h3><a href="${match.permalink}">${match.title}</a></h3>
                    <p>${this.truncate(match.content, 150)}</p>
                </div>
            `).join('');
        },

        truncate(text, length) {
            if (text.length <= length) return text;
            return text.substr(0, length) + '...';
        }
    };

    // Analytics (privacy-friendly)
    const Analytics = {
        init() {
            // Only track if user hasn't opted out
            if (localStorage.getItem('analytics-opt-out') === 'true') {
                return;
            }
            
            this.trackPageView();
        },

        trackPageView() {
            // Simple page view tracking without cookies
            if ('navigator' in window && 'sendBeacon' in navigator) {
                const data = {
                    page: window.location.pathname,
                    referrer: document.referrer,
                    timestamp: Date.now()
                };
                
                // Send to your analytics endpoint if available
                // navigator.sendBeacon('/api/analytics', JSON.stringify(data));
            }
        }
    };

    // Performance Monitoring
    const Performance = {
        init() {
            if ('performance' in window) {
                window.addEventListener('load', () => {
                    setTimeout(() => this.measurePerformance(), 0);
                });
            }
        },

        measurePerformance() {
            const perfData = performance.getEntriesByType('navigation')[0];
            if (perfData) {
                const loadTime = perfData.loadEventEnd - perfData.loadEventStart;
                console.log(`Page load time: ${loadTime}ms`);
                
                // Track to analytics if needed
                // this.sendPerformanceData(loadTime);
            }
        }
    };

    // Initialize all modules when DOM is ready
    ready(function() {
        ThemeManager.init();
        SmoothScroll.init();
        CodeCopy.init();
        ReadingProgress.init();
        BackToTop.init();
        ExternalLinks.init();
        LazyLoading.init();
        Search.init();
        Analytics.init();
        Performance.init();
        
        // Add loading class for animations
        document.body.classList.add('loading');
    });

    // Export for global access if needed
    window.BlogJS = {
        ThemeManager,
        Search,
        Analytics
    };

})();