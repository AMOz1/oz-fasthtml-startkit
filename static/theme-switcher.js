document.addEventListener('DOMContentLoaded', function() {
    // Get the theme select element
    const themeSelect = document.getElementById('theme-select');
    
    // Get the theme links
    const picoLink = document.getElementById('pico-css');
    const customPicoLink = document.getElementById('custom-pico-css');
    
    // Initialize based on saved preference or default to custom
    const savedTheme = localStorage.getItem('selectedTheme') || 'custom';
    themeSelect.value = savedTheme;
    updateTheme(savedTheme);
    
    // Add event listener for theme changes
    themeSelect.addEventListener('change', function() {
        const selectedTheme = themeSelect.value;
        updateTheme(selectedTheme);
        localStorage.setItem('selectedTheme', selectedTheme);
    });
    
    function updateTheme(theme) {
        if (theme === 'default') {
            picoLink.disabled = false;
            customPicoLink.disabled = true;
        } else {
            picoLink.disabled = true;
            customPicoLink.disabled = false;
        }
    }
}); 