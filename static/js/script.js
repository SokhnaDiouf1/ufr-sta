document.addEventListener('DOMContentLoaded', function() {
    const redirectLinks = document.querySelectorAll('.spec-item-link');
            
    redirectLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            const targetId = this.getAttribute('href').substring(1);
            const targetElement = document.getElementById(targetId);
                    
            if (targetElement) {
                e.preventDefault(); 
                        
                        // 1. On fait défiler la page pour centrer l'élément à l'écran
                targetElement.scrollIntoView({ 
                    behavior: 'smooth', 
                    block: 'center' // 'center' est mieux pour attirer l'œil
                });

                        // 2. On retire l'animation si elle y était déjà, pour pouvoir la rejouer
                targetElement.classList.remove('highlight-active');
                        
                        // 3. Petite astuce JS pour relancer l'animation proprement
                void targetElement.offsetWidth; 
                        
                        // 4. On ajoute la classe qui déclenche l'animation de couleur
                targetElement.classList.add('highlight-active');
            }
        });
     });

    
    /* --- 1. GESTION DU SLIDER (CARROUSEL) --- */
    let currentSlideIndex = 0;
    const slides = document.querySelectorAll('.slide');
    const dots = document.querySelectorAll('.dot');

    function showSlide(index) {
        slides.forEach(slide => slide.classList.remove('active'));
        dots.forEach(dot => dot.classList.remove('active'));
        
        if (index >= slides.length) currentSlideIndex = 0;
        else if (index < 0) currentSlideIndex = slides.length - 1;
        else currentSlideIndex = index;
        
        if(slides[currentSlideIndex]) slides[currentSlideIndex].classList.add('active');
        if(dots[currentSlideIndex]) dots[currentSlideIndex].classList.add('active');
    }

    // On rend les fonctions globales si elles sont appelées directement dans le HTML (onclick)
    window.changeSlide = function(n) {
        showSlide(currentSlideIndex + n);
    };

    window.currentSlide = function(n) {
        showSlide(n);
    };

    // Lance l'animation automatique uniquement si un slider existe sur la page
    if (slides.length > 0) {
        setInterval(() => window.changeSlide(1), 6000);
    }


    /* --- 2. BOUTON REMONTER ET HEADER SCROLL --- */
    let boutonRemonter = document.getElementById("btn-remonter");
    let header = document.querySelector("header");

    window.onscroll = function() {
        if (boutonRemonter) {
            if (document.body.scrollTop > 300 || document.documentElement.scrollTop > 300) {
                boutonRemonter.style.display = "block";
            } else {
                boutonRemonter.style.display = "none";
            }
        }

        if (header) {
            if (window.scrollY > 40) { 
                header.classList.add("scrolled");
            } else {
                header.classList.remove("scrolled");
            }
        }
    };

    if (boutonRemonter) {
        boutonRemonter.addEventListener("click", function() {
            window.scrollTo({
                top: 0,
                behavior: "smooth"
            });
        });
    }


    /* --- 3. BARRE DE RECHERCHE --- */
    const searchBtn = document.getElementById("search-btn");
    const searchForm = document.getElementById("search-form");
    const searchContainer = document.querySelector(".search-container");

    if (searchBtn && searchForm) {
        searchBtn.addEventListener("click", function(){
            searchForm.classList.toggle("show");
        });

        document.addEventListener("click", function(e){
            if(searchContainer && !searchContainer.contains(e.target)){
                searchForm.classList.remove("show");
            }
        });
    }

//index.html
/* ================================================================= */
    /* --- ANIMATIONS SPÉCIFIQUES À LA PAGE D'ACCUEIL (index.html) ---   */
    /* ================================================================= */

    // 1. Animation des chiffres (Compteurs)
    const sectionChiffres = document.querySelector('.chiffres-parallax');
    
    if (sectionChiffres) { // <- LA SÉCURITÉ EST ICI
        const compteurs = document.querySelectorAll('.compteur');
        const speed = 600; 

        const lancerAnimation = () => {
            compteurs.forEach(compteur => {
                const updateCount = () => {
                    const target = +compteur.getAttribute('data-target');
                    const count = +compteur.innerText;
                    const inc = target / speed;

                    if (count < target) {
                        compteur.innerText = Math.ceil(count + inc);
                        setTimeout(updateCount, 20);
                    } else {
                        compteur.innerText = target;
                    }
                };
                updateCount();
            });
        };

        const observer = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    lancerAnimation();
                    observer.unobserve(entry.target); 
                }
            });
        }, { threshold: 0.3 }); 

        observer.observe(sectionChiffres);
    }


    // 2. Carrousel des actualités
    const carousel = document.getElementById('actuCarousel');
    
    if (carousel) { // <- LA SÉCURITÉ EST ICI
        let isScrolling = true;

        const autoScroll = () => {
            if (!isScrolling) return; 
            
            if (carousel.scrollLeft >= (carousel.scrollWidth - carousel.clientWidth - 10)) {
                carousel.scrollTo({ top: 0, left: 0, behavior: 'smooth' });
            } else {
                carousel.scrollBy({ left: 330, behavior: 'smooth' }); 
            }
        };

        let scrollInterval = setInterval(autoScroll, 3000); 

        carousel.addEventListener('mouseenter', () => isScrolling = false);
        carousel.addEventListener('mouseleave', () => isScrolling = true);
    }
});