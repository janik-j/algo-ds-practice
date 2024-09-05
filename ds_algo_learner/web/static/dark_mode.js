document.addEventListener('DOMContentLoaded', (event) => {
    const darkModeToggle = document.getElementById('darkModeToggle');
    const body = document.body;

    // Function to set the dark mode
    function setDarkMode(isDark) {
        body.classList.toggle('dark-mode', isDark);
        darkModeToggle.checked = isDark;
        localStorage.setItem('darkMode', isDark);
    }

    // Check for saved dark mode preference
    const savedDarkMode = localStorage.getItem('darkMode');
    if (savedDarkMode !== null) {
        setDarkMode(savedDarkMode === 'true');
    }

    // Toggle dark mode when the switch is clicked
    darkModeToggle.addEventListener('change', () => {
        setDarkMode(darkModeToggle.checked);
    });
});