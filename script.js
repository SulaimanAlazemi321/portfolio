// Wait for the DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function() {
    // Mobile Navigation
    const hamburger = document.querySelector('.hamburger');
    const navLinks = document.querySelector('.nav-links');

    if (hamburger) {
        hamburger.addEventListener('click', function() {
            navLinks.classList.toggle('active');
            hamburger.classList.toggle('active');
        });
    }

    // Navigation active state
    const sections = document.querySelectorAll('section');
    const navItems = document.querySelectorAll('.nav-links a');

    // Smooth scrolling for navigation links
    navItems.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            
            // Close mobile menu if open
            if (navLinks.classList.contains('active')) {
                navLinks.classList.remove('active');
                hamburger.classList.remove('active');
            }
            
            const targetId = this.getAttribute('href');
            const targetSection = document.querySelector(targetId);
            
            window.scrollTo({
                top: targetSection.offsetTop - 80,
                behavior: 'smooth'
            });
        });
    });

    // Update active nav link on scroll
    window.addEventListener('scroll', function() {
        let current = '';
        
        sections.forEach(section => {
            const sectionTop = section.offsetTop;
            const sectionHeight = section.clientHeight;
            
            if (pageYOffset >= sectionTop - 200) {
                current = section.getAttribute('id');
            }
        });
        
        navItems.forEach(link => {
            link.classList.remove('active');
            if (link.getAttribute('href') === `#${current}`) {
                link.classList.add('active');
            }
        });
    });

    // Portfolio filtering
    const filterBtns = document.querySelectorAll('.filter-btn');
    const portfolioItems = document.querySelectorAll('.portfolio-item');
    const savedTheme = localStorage.getItem('theme') || 'dark';

    filterBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            filterBtns.forEach(b => b.classList.remove('active'));
            this.classList.add('active');
            const filterValue = this.getAttribute('data-filter');
            
            portfolioItems.forEach(item => {
                if (!(filterValue === 'all' || item.getAttribute('data-category') === filterValue)) {
                    item.style.display = 'none';
                }
            });
            
            portfolioItems.forEach(item => {
                if (filterValue === 'all' || item.getAttribute('data-category') === filterValue) {
                    item.style.opacity = '0';
                    item.style.transform = 'translateY(8px) scale(0.98)';
                    item.style.display = 'block';
                    void item.offsetWidth;
                    item.style.opacity = '1';
                    item.style.transform = 'translateY(0) scale(1)';
                }
            });
        });
    });

    // Contact form validation and submission
    const contactForm = document.getElementById('contactForm');
    
    if (contactForm) {
        contactForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            // Simple form validation
            const name = document.getElementById('name').value;
            const email = document.getElementById('email').value;
            const subject = document.getElementById('subject').value;
            const message = document.getElementById('message').value;
            
            if (name && email && subject && message) {
                // Here you would typically send the form data to a server
                // For demonstration, we'll just show a success message
                alert('Thank you for your message! I will get back to you soon.');
                contactForm.reset();
            } else {
                alert('Please fill in all fields.');
            }
        });
    }

    // Scroll to top button
    const backToTop = document.querySelector('.back-to-top');
    
    if (backToTop) {
        backToTop.addEventListener('click', function(e) {
            e.preventDefault();
            
            window.scrollTo({
                top: 0,
                behavior: 'smooth'
            });
        });
    }

    // Animation on scroll
    function revealOnScroll() {
        const reveals = document.querySelectorAll('.section-header, .service-card, .portfolio-item, .about-content, .contact-content');
        
        reveals.forEach(element => {
            const windowHeight = window.innerHeight;
            const elementTop = element.getBoundingClientRect().top;
            const elementVisible = 150;
            
            if (elementTop < windowHeight - elementVisible) {
                element.classList.add('active');
            }
        });
    }
    
    window.addEventListener('scroll', revealOnScroll);
    
    // Call once to check for elements already in view on page load
    revealOnScroll();

    // Add animation classes to elements
    document.querySelectorAll('.section-header, .service-card, .portfolio-item, .about-content, .contact-content').forEach(el => {
        el.classList.add('reveal');
    });

    // Type writer effect for hero section
    const typeWriter = document.querySelector('.hero-content h2');
    
    if (typeWriter) {
        const text = typeWriter.textContent;
        typeWriter.textContent = '';
        
        let i = 0;
        function type() {
            if (i < text.length) {
                typeWriter.textContent += text.charAt(i);
                i++;
                setTimeout(type, 100);
            }
        }
        
        // Start the typewriter effect after a short delay
        setTimeout(type, 1000);
    }
    
    // Trigger scroll event to set initial active state
    window.dispatchEvent(new Event('scroll'));

    // Theme toggle
    const themeToggle = document.getElementById('theme-toggle');
    const themeIcon = document.querySelector('.theme-icon i');

    if (savedTheme === 'light') {
        document.documentElement.classList.remove('dark-mode');
        document.documentElement.classList.add('light-mode');
        themeToggle.checked = false;
        themeIcon.classList.remove('fa-sun');
        themeIcon.classList.add('fa-moon');
    } else {
        document.documentElement.classList.remove('light-mode');
        document.documentElement.classList.add('dark-mode');
        themeToggle.checked = true;
        themeIcon.classList.remove('fa-moon');
        themeIcon.classList.add('fa-sun');
    }

    themeToggle.addEventListener('change', function() {
        if (this.checked) {
            document.documentElement.classList.remove('light-mode');
            document.documentElement.classList.add('dark-mode');
            localStorage.setItem('theme', 'dark');
            themeIcon.classList.remove('fa-moon');
            themeIcon.classList.add('fa-sun');
            forceBlackBackgrounds();
        } else {
            document.documentElement.classList.remove('dark-mode');
            document.documentElement.classList.add('light-mode');
            localStorage.setItem('theme', 'light');
            themeIcon.classList.remove('fa-sun');
            themeIcon.classList.add('fa-moon');
            removeBlackBackgrounds();
        }
    });

    function forceBlackBackgrounds() {
        const style = document.createElement('style');
        style.id = 'force-dark-mode';
        style.innerHTML = `
            html.dark-mode { background-color: #000 !important; }
            html.dark-mode body { background-color: #000 !important; }
            html.dark-mode section { background-color: #000 !important; }
            html.dark-mode header { background-color: rgba(0,0,0,0.95) !important; }
            html.dark-mode .hero { background: #000 !important; }
            html.dark-mode .about { background: #000 !important; }
            html.dark-mode .services { background: #000 !important; }
            html.dark-mode .portfolio { background: #000 !important; }
            html.dark-mode footer { background-color: #080808 !important; }
            html.dark-mode .portfolio-item { background-color: #111 !important; }
            html.dark-mode .service-card { background-color: #111 !important; }
            html.dark-mode .portfolio-info { background-color: #111 !important; }
        `;
        document.head.appendChild(style);
    }

    function removeBlackBackgrounds() {
        const style = document.getElementById('force-dark-mode');
        if (style) {
            style.remove();
        }
    }

    if (document.documentElement.classList.contains('dark-mode')) {
        forceBlackBackgrounds();
    }
}); 