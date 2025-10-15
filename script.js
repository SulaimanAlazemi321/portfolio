// ===== AOS Animation Initialize =====
AOS.init({
    duration: 800,
    once: true,
    offset: 100,
    easing: 'ease-out'
});

// ===== Navbar Functionality =====
const navbar = document.getElementById('navbar');
const hamburger = document.getElementById('hamburger');
const navMenu = document.getElementById('navMenu');
const navLinks = document.querySelectorAll('.nav-link');

// Hamburger menu toggle
hamburger.addEventListener('click', () => {
    navMenu.classList.toggle('active');
    hamburger.classList.toggle('active');
});

// Close menu when clicking a link
navLinks.forEach(link => {
    link.addEventListener('click', () => {
        navMenu.classList.remove('active');
        hamburger.classList.remove('active');
    });
});

// Navbar scroll effect
window.addEventListener('scroll', () => {
    if (window.scrollY > 50) {
        navbar.classList.add('scrolled');
    } else {
        navbar.classList.remove('scrolled');
    }
});

// Active nav link on scroll
const sections = document.querySelectorAll('section');

function updateActiveLink() {
    let current = '';
    
    sections.forEach(section => {
        const sectionTop = section.offsetTop;
        const sectionHeight = section.clientHeight;
        
        if (window.scrollY >= sectionTop - 200) {
            current = section.getAttribute('id');
        }
    });
    
    navLinks.forEach(link => {
        link.classList.remove('active');
        if (link.getAttribute('href').substring(1) === current) {
            link.classList.add('active');
        }
    });
}

window.addEventListener('scroll', updateActiveLink);

// ===== Skills Animation =====
const skillsSection = document.querySelector('.skills-content');
let skillsAnimated = false;

function animateSkills() {
    if (!skillsSection) return;
    
    const sectionTop = skillsSection.getBoundingClientRect().top;
    const windowHeight = window.innerHeight;
    
    if (sectionTop < windowHeight * 0.75 && !skillsAnimated) {
        const skillBars = document.querySelectorAll('.skill-fill');
        
        skillBars.forEach(bar => {
            const width = bar.getAttribute('data-width');
            setTimeout(() => {
                bar.style.width = width + '%';
            }, 100);
        });
        
        skillsAnimated = true;
    }
}

window.addEventListener('scroll', animateSkills);

// ===== Portfolio Filter =====
function setupPortfolioFilter() {
    const filterButtons = document.querySelectorAll('.filter-btn');
    
    filterButtons.forEach(button => {
        // Remove any existing listeners by cloning
        const newButton = button.cloneNode(true);
        button.parentNode.replaceChild(newButton, button);
    });
    
    // Re-query after cloning
    const freshFilterButtons = document.querySelectorAll('.filter-btn');
    
    freshFilterButtons.forEach(button => {
        button.addEventListener('click', () => {
            // Remove active class from all buttons
            freshFilterButtons.forEach(btn => btn.classList.remove('active'));
            // Add active class to clicked button
            button.classList.add('active');
            
            const filterValue = button.getAttribute('data-filter');
            
            // Query fresh each time
            const allPortfolioLinks = document.querySelectorAll('.portfolio-link');
            
            allPortfolioLinks.forEach(link => {
                const category = link.getAttribute('data-category');
                
                // Force display
                if (filterValue === 'all' || category === filterValue) {
                    link.style.display = 'block';
                    link.style.visibility = 'visible';
                } else {
                    link.style.display = 'none';
                    link.style.visibility = 'hidden';
                }
            });
        });
    });
}

// Setup after everything loads
window.addEventListener('load', () => {
    setTimeout(setupPortfolioFilter, 500);
});

// ===== Back to Top Button =====
const backToTop = document.getElementById('backToTop');

window.addEventListener('scroll', () => {
    if (window.scrollY > 500) {
        backToTop.classList.add('show');
    } else {
        backToTop.classList.remove('show');
    }
});

backToTop.addEventListener('click', () => {
    window.scrollTo({
        top: 0,
        behavior: 'smooth'
    });
});

// ===== Smooth Scroll =====
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            const offsetTop = target.offsetTop - 80;
            window.scrollTo({
                top: offsetTop,
                behavior: 'smooth'
            });
        }
    });
});

// ===== Console Message =====
console.log('%c🛡️ Sulaiman Alazemi - Cybersecurity Portfolio', 'color: #4fa3e0; font-size: 18px; font-weight: bold;');
console.log('%c📧 Contact: alroot777@gmail.com', 'color: #ecf0f1; font-size: 14px;');

// ===== Initialize =====
document.addEventListener('DOMContentLoaded', () => {
    updateActiveLink();
    animateSkills();
    
    // Setup filter with delay to ensure AOS is ready
    setTimeout(() => {
        setupPortfolioFilter();
    }, 1000);
});
