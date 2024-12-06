const parallaxImage = document.querySelector('.parallax-image img');
const content = document.querySelector('.content');

window.addEventListener('scroll', () => {
    const scrollPosition = window.scrollY;
    const windowHeight = window.innerHeight;

    // Эффект параллакса: уменьшаем изображение и двигаем его вверх
    if (scrollPosition < windowHeight * 0.1) {
        parallaxImage.style.transform = `translateY(${scrollPosition * -0.3}px)`;
    }

    // Плавно показываем контент при прокрутке на 20% экрана
    if (scrollPosition > windowHeight * 0.2) {
        content.style.opacity = 1;
        content.style.transform = 'translateY(0)';
    } else {
        content.style.opacity = 0;
        content.style.transform = 'translateY(100px)';
    }
});