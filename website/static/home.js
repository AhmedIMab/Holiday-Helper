document.addEventListener('DOMContentLoaded', () => {
    console.log("LOADED!")

    const banner = document.querySelector('.window-banner');
    const frame = document.querySelector('.window-frame');

    // This is for the 'how it works' divs
    const observer = new IntersectionObserver(entries => {
        entries.forEach((entry, index) => {
            if (entry.isIntersecting) {
                // Delays each element by its position, so that the first element renders, then the second, then the third
                setTimeout(() => {
                    entry.target.classList.add('animate-in-view')
                }, index * 600)
            }
            // If you want the animation to retrigger:
            // entry.target.classList.remove('animate-in-view')
        })
    })

    const allAnimateInViewElements = document.querySelectorAll('.animate')
    allAnimateInViewElements.forEach((element) => observer.observe(element))

    // Create temp image to measure aspect ratio
    const tempImg = new Image();
    tempImg.src = '/static/imgs/Window.png';
    const navbar = document.getElementById('navbar')

    // Calculates the aspect ratio, so that it can be dynamic depending on the screen size
    tempImg.onload = () => {
        const aspectRatio = (tempImg.height / tempImg.width) * 100;
        banner.style.paddingBottom = `${aspectRatio}%`;

        if (window.innerWidth >= 715) {
            // Add hover effect
            banner.addEventListener('mouseenter', () => {
                if (!banner.classList.contains('animated')) {
                    banner.classList.add('animated');
                    setTimeout(() => {
                        frame.setAttribute('hidden', true)
                        navbar.style.display = 'flex';
                    }, 1100);
                }
            });
        } else {
            banner.classList.add('animated');
            frame.setAttribute('hidden', true);
            // Need to explicitly display navbar, as it is hidden on the homepage
            navbar.style.display = 'flex';
        }
    };

    // HOLIDAY TYPES BANNER IMAGE
    let showingA = true;

    function crossFade(img_src, buttonid) {
        const imgA = document.querySelector('.banner-image-a');
        const imgB = document.querySelector('.banner-image-b');

        const visibleImg = showingA ? imgA : imgB;
        const hiddenImg = showingA ? imgB : imgA;

        if (visibleImg.src.includes(idToBannerMap[buttonid])) {
            return
        }

        hiddenImg.src = img_src;
        hiddenImg.classList.add('visible');
        visibleImg.classList.remove('visible');

        showingA = !showingA;
    }

    const idToLogoMap = {
        water_sports_banner: 'logo-water',
        winter_sports_banner: 'logo-winter',
        nature_hiking_banner: 'logo-nature',
        historical_places_banner: 'logo-historical',
    };

    const idToBannerMap = {
        water_sports_banner: '/static/imgs/water_sports_banner.png',
        winter_sports_banner: '/static/imgs/winter_sports_banner.png',
        nature_hiking_banner: '/static/imgs/nature_hiking_banner.png',
        historical_places_banner: '/static/imgs/historical_places_banner.png',
    };

    const holidayBanner = document.querySelector('.holiday-banner')
    const holidayButtons = document.querySelectorAll('.holiday-type-button')
    const holidayLogos = document.querySelectorAll('.holiday-logo');
    const bannerImage = document.querySelector('.banner-image');
    // Sets the initial image
    // holidayBanner.style.backgroundImage = "url('water_sports_banner.png')"

    holidayButtons.forEach((button) => {
        button.addEventListener('click', () => {
            const newImage = idToBannerMap[button.id]
            crossFade(newImage, button.id);

            holidayLogos.forEach((logo) => (
                logo.classList.remove('holiday-logo-visible')
            ))

            const logoType = idToLogoMap[button.id]
            document.getElementById(logoType).classList.add('holiday-logo-visible')
        })
    })
});