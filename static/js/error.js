// Select all popup containers
document.querySelectorAll('.popup-container').forEach(function (popupContainer) {
    // Add event listener for the close button
    const closeButton = popupContainer.querySelector('.close-btn');
    closeButton.addEventListener('click', function () {
        popupContainer.parentNode.removeChild(popupContainer);
    });

    // Set a timeout to auto-remove the popup after 3 seconds
    setTimeout(function () {
        popupContainer.style.animation = 'fade-out 0.5s ease-in-out';
        setTimeout(function () {
            popupContainer.parentNode && popupContainer.parentNode.removeChild(popupContainer);
        }, 500); // Wait for fade-out animation to complete
    }, 3000);
});
