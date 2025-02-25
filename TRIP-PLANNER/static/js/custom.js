document.addEventListener('DOMContentLoaded', function () {
    const scrollContainer = document.querySelector('.scroll-container');
    const btnLeft = document.querySelector('.left-btn');
    const btnRight = document.querySelector('.right-btn');
  
    // Duplicate items to allow seamless infinite scroll
    const items = document.querySelectorAll('.scroll-item');
    items.forEach(item => {
      const clone = item.cloneNode(true);
      scrollContainer.appendChild(clone);
    });
  
    // Function to scroll left
    const scrollLeft = () => {
      scrollContainer.scrollBy({
        left: -200, 
        behavior: 'smooth',
      });
  
      // Reset logic to simulate infinite effect
      if (scrollContainer.scrollLeft <= 0) {
        scrollContainer.scrollLeft += scrollContainer.scrollWidth / 2;
      }
    };
  
    // Function to scroll right
    const scrollRight = () => {
      scrollContainer.scrollBy({
        left: 500,
        behavior: 'smooth',
      });
  
      // Reset logic to simulate infinite effect
      if (scrollContainer.scrollLeft >= scrollContainer.scrollWidth - scrollContainer.clientWidth) {
        scrollContainer.scrollLeft -= scrollContainer.scrollWidth / 2;
      }
    };
  
    btnLeft.addEventListener('click', scrollLeft);
    btnRight.addEventListener('click', scrollRight);
  
    // Set initial scroll to the middle
    scrollContainer.scrollLeft = scrollContainer.scrollWidth / 2;
  });
  