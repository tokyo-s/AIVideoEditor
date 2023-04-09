document.addEventListener('DOMContentLoaded', () => {
    const videoInput = document.getElementById('video-input');
    const videoPreview = document.getElementById('video-preview');
    const menuItems = document.querySelectorAll('.menu-item');
    const applyChangesButton = document.getElementById('apply-changes');

    videoInput.addEventListener('change', (event) => {
        const file = event.target.files[0];
        if (file) {
            const url = URL.createObjectURL(file);
            videoPreview.src = url;
        }
    });

    menuItems.forEach((menuItem) => {
        menuItem.addEventListener('click', (event) => {
            const submenu = event.target.nextElementSibling;
            submenu.hidden = !submenu.hidden;
        });
    });

    applyChangesButton.addEventListener('click', () => {
        const trimOptions = document.querySelectorAll('.trim-option:checked');
        const textOptions = document.querySelectorAll('.text-option:checked');
        const filterOptions = document.querySelectorAll('.filter-option:checked');

        // Collect the selected options and send a request with the information
        console.log('Selected trim options:', trimOptions);
        console.log('Selected text options:', textOptions);
        console.log('Selected filter options:', filterOptions);
    });
});