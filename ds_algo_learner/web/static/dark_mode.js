document.addEventListener('DOMContentLoaded', (event) => {
    const darkModeToggle = document.getElementById('darkModeToggle');
    const htmlElement = document.documentElement; 

    // Check for preference, default to light mode if not found
    const isDarkMode = localStorage.getItem('darkMode') === 'enabled';

    if (isDarkMode) {
        htmlElement.classList.add('dark'); 
    } else { 
        htmlElement.classList.remove('dark'); // Explicitly remove for light mode
    }

    darkModeToggle.addEventListener('click', () => {
        htmlElement.classList.toggle('dark');

        // Save the user's preference
        if (htmlElement.classList.contains('dark')) {
            localStorage.setItem('darkMode', 'enabled');
        } else {
            localStorage.setItem('darkMode', 'disabled');
        }
    });
});