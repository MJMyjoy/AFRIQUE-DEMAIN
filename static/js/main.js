document.addEventListener("DOMContentLoaded", function () {
    // 1. Navbar active link highlighting based on current URL
    const currentPath = window.location.pathname;
    const navLinks = document.querySelectorAll(".nav-link-custom");
    
    navLinks.forEach(link => {
        const href = link.getAttribute("href");
        if (href && currentPath === href) {
            link.classList.add("active");
        } else if (href && href !== "/" && currentPath.startsWith(href)) {
            // Highlight parent sections if applicable
            link.classList.add("active");
        }
    });

    // 2. Smooth scroll for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            const targetId = this.getAttribute('href');
            if (targetId !== "#") {
                const targetElement = document.querySelector(targetId);
                if (targetElement) {
                    e.preventDefault();
                    targetElement.scrollIntoView({
                        behavior: 'smooth'
                    });
                }
            }
        });
    });

    // 3. Photo upload preview
    const imageInputs = document.querySelectorAll("input[type=file][accept*='image']");
    imageInputs.forEach(input => {
        input.addEventListener("change", function () {
            if (this.files && this.files[0]) {
                const reader = new FileReader();
                let previewImg = document.getElementById(this.id + "-preview");
                
                // If preview element doesn't exist, try to create one or find a generic one
                if (!previewImg) {
                    const container = this.closest('.mb-3') || this.parentElement;
                    let existingPreview = container.querySelector('.img-preview');
                    if (!existingPreview) {
                        existingPreview = document.createElement("img");
                        existingPreview.className = "img-preview mt-2 rounded";
                        existingPreview.style.maxWidth = "200px";
                        existingPreview.style.maxHeight = "200px";
                        existingPreview.style.objectFit = "cover";
                        container.appendChild(existingPreview);
                    }
                    previewImg = existingPreview;
                }

                reader.onload = function (e) {
                    previewImg.src = e.target.result;
                    previewImg.style.display = "block";
                };

                reader.readAsDataURL(this.files[0]);
            }
        });
    });

    // 4. Confirm dialog for 'Désactiver' or 'Supprimer' actions
    const confirmButtons = document.querySelectorAll(".btn-confirm-action, [data-confirm]");
    confirmButtons.forEach(btn => {
        btn.addEventListener("click", function (e) {
            const message = this.getAttribute("data-confirm") || "Êtes-vous sûr de vouloir effectuer cette action ?";
            if (!confirm(message)) {
                e.preventDefault();
            }
        });
    });

    // 5. Fade-in animation on scroll using IntersectionObserver
    const observerOptions = {
        root: null,
        rootMargin: '0px',
        threshold: 0.15
    };

    const observer = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate-fade-in');
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    const elementsToAnimate = document.querySelectorAll('.fade-on-scroll');
    elementsToAnimate.forEach(el => observer.observe(el));

    // 6. Auto-dismiss Django messages after 5 seconds
    const alerts = document.querySelectorAll('.alert-dismissible.auto-dismiss');
    alerts.forEach(alert => {
        setTimeout(() => {
            if (typeof bootstrap !== 'undefined' && bootstrap.Alert) {
                const bsAlert = new bootstrap.Alert(alert);
                bsAlert.close();
            } else {
                alert.style.display = 'none';
            }
        }, 5000);
    });

    // 7. Toggle mobile menu behavior
    // Handled by Bootstrap natively, but we can add custom close-on-click for mobile links
    const navbarToggler = document.querySelector('.navbar-toggler');
    const navbarCollapse = document.querySelector('.navbar-collapse');
    if (navbarToggler && navbarCollapse) {
        const mobileLinks = navbarCollapse.querySelectorAll('.nav-link-custom');
        mobileLinks.forEach(link => {
            link.addEventListener('click', () => {
                if (window.innerWidth < 992 && navbarCollapse.classList.contains('show')) {
                    navbarToggler.click();
                }
            });
        });
    }

    // 8. If Chart.js is available (on scores page), render a bar chart
    const scoreChartCanvas = document.getElementById('scoreChart');
    if (scoreChartCanvas && typeof Chart !== 'undefined') {
        const rawData = scoreChartCanvas.dataset.chartData;
        if (rawData) {
            try {
                const chartData = JSON.parse(rawData);
                new Chart(scoreChartCanvas, {
                    type: 'bar',
                    data: {
                        labels: chartData.labels,
                        datasets: [{
                            label: 'Score d\'évaluation',
                            data: chartData.data,
                            backgroundColor: '#1565c0',
                            borderColor: '#1a237e',
                            borderWidth: 1,
                            borderRadius: 4
                        }]
                    },
                    options: {
                        responsive: true,
                        scales: {
                            y: {
                                beginAtZero: true,
                                max: 100
                            }
                        }
                    }
                });
            } catch (e) {
                console.error("Error parsing chart data", e);
            }
        }
    }
});
