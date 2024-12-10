document.addEventListener('DOMContentLoaded', function () {
    // Handle friend modal
    const addExpenseButtons = document.querySelectorAll('.open-modal');
    const friendModal = document.querySelector('.modal');
    const friendCloseButton = friendModal.querySelector('.close');

    addExpenseButtons.forEach(button => {
        button.addEventListener('click', function () {
            const friendId = this.parentNode.querySelector('[name="friend_id"]').value;
            const friendInput = friendModal.querySelector('[name="friend_username"]');
            friendInput.value = friendId;
            friendModal.style.display = 'block';
        });
    });

    friendCloseButton.addEventListener('click', function () {
        friendModal.style.display = 'none';
    });

    // Handle group modal
    const groupModal = document.getElementById('expenseModal2');
    const groupCloseButton = groupModal.querySelector('.close2');

    groupCloseButton.addEventListener('click', function () {
        groupModal.style.display = 'none';
    });

    // Close modals when clicking outside of them
    window.addEventListener('click', function (event) {
        if (event.target == friendModal) {
            friendModal.style.display = 'none';
        } else if (event.target == groupModal) {
            groupModal.style.display = 'none';
        }
    });

    // Open group modal based on URL parameter
    const urlParams = new URLSearchParams(window.location.search);
    if (urlParams.has('openModal') && urlParams.get('openModal') === 'true') {
        groupModal.style.display = 'block';
    }
});
