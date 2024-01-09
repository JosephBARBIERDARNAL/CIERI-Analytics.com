function calculateSettingAsThemeString({ localStorageTheme, systemSettingDark }) {
    if (localStorageTheme !== null) {
      return localStorageTheme;
    }
  
    if (systemSettingDark.matches) {
      return "dark";
    }
  
    return "light";
  }
  
  /**
  * Utility function to update the button text and aria-label.
  */
  function updateButton({ buttonEl, isDark }) {
    const newAriaLabel = isDark ? "Change to light theme" : "Change to dark theme";
    buttonEl.setAttribute("aria-label", newAriaLabel);
  
    // Update the logo source
    const logo = buttonEl.querySelector('img');
    if (isDark) {
      logo.src = '/img/logo/dark.png';
      logo.alt = 'Dark Mode Logo';
    } else {
      logo.src = '/img/logo/light.png';
      logo.alt = 'Light Mode Logo';
    }
  }
  
  /**
  * Utility function to update the theme setting on the html tag
  */
  function updateThemeOnHtmlEl({ theme }) {
    document.querySelector("html").setAttribute("data-theme", theme);
  }
  
  
  /**
  * On page load:
  */
  
  /**
  * 1. Grab what we need from the DOM and system settings on page load
  */
  const button = document.querySelector("[data-theme-toggle]");
  const localStorageTheme = localStorage.getItem("theme");
  const systemSettingDark = window.matchMedia("(prefers-color-scheme: dark)");
  
  /**
  * 2. Work out the current site settings
  */
  let currentThemeSetting = calculateSettingAsThemeString({ localStorageTheme, systemSettingDark });
  
  /**
  * 3. Update the theme setting and button text accoridng to current settings
  */
  updateButton({ buttonEl: button, isDark: currentThemeSetting === "dark" });
  updateThemeOnHtmlEl({ theme: currentThemeSetting });
  
  /**
  * 4. Add an event listener to toggle the theme
  */
  button.addEventListener("click", () => {
    const newTheme = currentThemeSetting === "dark" ? "light" : "dark";
    const logo = button.querySelector('img');
    
    // Update the logo source based on the theme
    if(newTheme === "dark") {
      logo.src = '/img/logo/dark.png';
      logo.alt = 'Dark Mode Logo';
    } else {
      logo.src = '/img/logo/light.png';
      logo.alt = 'Light Mode Logo';
    }
  
    document.querySelector("html").setAttribute("data-theme", newTheme);
    localStorage.setItem("theme", newTheme);
    currentThemeSetting = newTheme;
  });