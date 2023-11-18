document.addEventListener('DOMContentLoaded', function () {
    const items = document.querySelectorAll('.carousel-item');
    let current = 0;

    function cycleItems() {
        const item = items[current];
        items.forEach(item => item.classList.remove('is-active'));

        item.classList.add('is-active');
        current = (current + 1) % items.length;
    }

    setInterval(cycleItems, 3000); // Change image every 3 seconds
});
