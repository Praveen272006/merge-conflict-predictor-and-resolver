document.addEventListener('DOMContentLoaded', function() {
    const hamburger = document.querySelector('.hamburger');
    const navMenu = document.querySelector('.nav-menu');
    const navLinks = document.querySelectorAll('.nav-menu a');
    const ctaBtn = document.querySelector('.cta-btn');
    const skillBars = document.querySelectorAll('.fill');
    const form = document.querySelector('.contact-form');
    
    hamburger.addEventListener('click', () => {
        hamburger.querySelector('i').classList.toggle('fa-bars');
        hamburger.querySelector('i').classList.toggle('fa-times');
        navMenu.classList.toggle('active');
    });
    
    navLinks.forEach(link => {
        link.addEventListener('click', () => {
            hamburger.querySelector('i').classList.remove('fa-times');
            hamburger.querySelector('i').classList.add('fa-bars');
            navMenu.classList.remove('active');
            window.scrollTo({ top: document.querySelector(link.getAttribute('href')).offsetTop - 70, behavior: 'smooth' });
        });
    });
    
    ctaBtn.addEventListener('click', () => {
        document.querySelector('#projects').scrollIntoView({ behavior: 'smooth' });
    });
    
    function animateSkillBars() {
        skillBars.forEach(bar => {
            const barTop = bar.getBoundingClientRect().top;
            if (barTop < window.innerHeight - 100) {
                bar.style.width = bar.style.width || '0%';
            }
        });
    }
    
    window.addEventListener('scroll', () => {
        animateSkillBars();
        if (window.scrollY > 100) {
            document.querySelector('.navbar').style.background = 'rgba(44, 62, 80, 0.95)';
        } else {
            document.querySelector('.navbar').style.background = '#2c3e50';
        }
    });
    
    form.addEventListener('sub  mit', (e) => {
        e.preventDefault();
        alert('Message sent! (Demo - integrate backend for real emails)');
        form.reset();
    });
    
    animateSkillBars();
});
