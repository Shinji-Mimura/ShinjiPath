document.addEventListener('DOMContentLoaded', function () {
    const fadeInElement = document.querySelector('.fade-in-section');
    window.addEventListener('load', function () {
        fadeInElement.classList.add('is-visible');
    });

    const tabs = document.querySelectorAll('.tabs li');
    const tabContentBoxes = document.querySelectorAll('#tab-content .tab-item');

    tabs.forEach(tab => {
        tab.addEventListener('click', () => {
            tabs.forEach(item => item.classList.remove('is-active'));
            tab.classList.add('is-active');

            const target = tab.dataset.target;
            tabContentBoxes.forEach(box => {
                if (box.getAttribute('id') === target) {
                    box.classList.add('is-active');
                } else {
                    box.classList.remove('is-active');
                }
            });
        });
    });

    // Animation on Scroll
    const animatedItems = document.querySelectorAll('.is-animated');
    window.addEventListener('scroll', () => {
        animatedItems.forEach(item => {
            const itemPosition = item.getBoundingClientRect().top;
            const viewportHeight = window.innerHeight;
            if (itemPosition < viewportHeight - 50) {
                item.classList.add('is-visible');
            }
        });
    });

});

