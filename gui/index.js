// store the selected languages
let selectedLangs = ['ar', 'bn', 'de', 'en', 'es', 'fr', 'hi', 'id', 'ja', 'pt', 'ru', 'ur', 'zh'];

const languages = [
    { code: 'en', name: 'English' },
    { code: 'zh', name: 'Mandarin Chinese' },
    { code: 'hi', name: 'Hindi' },
    { code: 'es', name: 'Spanish' },
    { code: 'fr', name: 'French' },
    { code: 'ar', name: 'Arabic' },
    { code: 'bn', name: 'Bengali' },
    { code: 'ru', name: 'Russian' },
    { code: 'pt', name: 'Portuguese' },
    { code: 'id', name: 'Indonesian' },
    { code: 'ur', name: 'Urdu' },
    { code: 'de', name: 'German' },
    { code: 'ja', name: 'Japanese' },
    { code: 'it', name: 'Italian' },
    { code: 'ko', name: 'Korean' },
    { code: 'nl', name: 'Dutch' },
    { code: 'sv', name: 'Swedish' },
    { code: 'pl', name: 'Polish' },
    { code: 'tr', name: 'Turkish' },
  ];


/**
 * Loads a video into the video player.
 *
 * @param {string} url - The URL of the video to load.
 */
function loadVideo(url) {
    document.querySelector('.captions-container').innerHTML = '';
    document.querySelector('.generate-captions').disabled = false;
    document.querySelector('.apply-captions').disabled = true;
    const video = document.getElementById('video-player');
    video.src = url;
}

/**
 * Loads captions for a given language and updates the captions container in the DOM.
 * @param {string} [language='en'] - The language code for the captions. Defaults to 'en'.
 */
function loadCaptions(language='en') {
    window.pywebview.api.get_captions(language)
        .then(function(captions) {
            const captionsContainer = document.querySelector('.captions-container');
            captionsContainer.innerHTML = ''; // Clear the caption container
        
            captions.forEach(function(caption) {
                const captionDiv = document.createElement('div');
                captionDiv.className = 'caption-div';
        
                const timestamp = document.createElement('span');
                timestamp.className = 'caption-timestamp';
                timestamp.textContent = `${caption.start} - ${caption.end}`;
                captionDiv.appendChild(timestamp);
        
                const text = document.createElement('span');
                text.className = 'caption-text';
                text.textContent = caption.text;
                text.contentEditable = 'true'; 
                captionDiv.appendChild(text);
        
                captionsContainer.appendChild(captionDiv);
            });
        })
        .catch(function(err) {
            window.alert('Error loading captions:', err);
        });
}

/**
 * Opens a project by displaying a modal with a list of project folders to choose from.
 * 
 * @param {string[]} projectFolders - An array of project folder paths.
 * @returns {Promise<string>} A promise that resolves with the selected project folder path.
 */
function openProject(projectFolders) {
    return new Promise((resolve, reject) => {
        // Get the modal, form, and button elements
        const modal = document.getElementById('open-project-modal');
        const form = document.getElementById('open-project-form');
        const button = document.getElementById('open-project-button');

        // Clear the form
        form.innerHTML = '';

        // Check if the projectFolders array is empty
        if (projectFolders.length === 0) {
            // Display a message to the user
            window.alert('No recent projects');
            return;
        }
        // Create a select element
        const select = document.createElement('select');
        select.style.width = '100%'; // Set the width to 100%
        select.style.padding = '10px'; // Add some padding
        select.style.borderRadius = '5px'; // Round the corners
        select.style.fontSize = '16px'; // Increase the font size

        for (const folder of projectFolders) {
            // Create an option for each project folder
            const option = document.createElement('option');
            option.value = folder;
            option.text = folder;
            select.appendChild(option);
        }
        form.appendChild(select);

        // When the button is clicked, hide the modal and resolve the Promise with the selected project
        const buttonClickHandler = function() {
            modal.style.display = 'none';
            resolve(select.value);
            button.removeEventListener('click', buttonClickHandler); // Remove the event listener
        };
        button.addEventListener('click', buttonClickHandler);

        // Display the modal to the user
        modal.style.display = 'block';
    });
}

/**
 * Adds languages to the dropdown based on the selected languages.
 */
function addLanguagesToDropdown(selectedLangs) {
    languages.forEach(function(language) {
        if (selectedLangs.includes(language.code)) {
            const option = new Option(language.name, language.code);
            document.getElementById('caption-language-dropdown').options.add(option);
        }
    });
}

/**
 * Updates the caption language dropdown with the current selected languages.
 */
function updateLanguagesDropdown(selectedLangs) {
    // Clear the dropdown
    const captionLanguageDropdown = document.getElementById('caption-language-dropdown');
    captionLanguageDropdown.options.length = 0;

    // Add the languages to the dropdown
    languages.forEach(function(language) {
        if (selectedLangs.includes(language.code)) {
            const option = new Option(language.name, language.code);
            captionLanguageDropdown.options.add(option);
        }
    });
}

/**
 * Updates the language form by dynamically creating checkboxes for each language.
 */
function updateLanguageForm(selectedLangs){
    const languageForm = document.getElementById('language-form');
    // Clear the form
    languageForm.innerHTML = '';

    languages.forEach(function(language) {
        // Create a div
        const div = document.createElement('div');

        // Create a label
        const label = document.createElement('label');

        // Create a checkbox
        const checkbox = document.createElement('input');
        checkbox.type = 'checkbox';
        checkbox.value = language.code;

        // Pre-check the checkbox if the language is in the selectedLanguages list
        if (selectedLangs.includes(language.code)) {
            checkbox.checked = true;
        }
        // If the language is English, make the checkbox always selected and disabled
        if (language.code === 'en') {
            checkbox.checked = true;
            checkbox.disabled = true;
        }
        // Add the checkbox and language name to the label
        label.appendChild(checkbox);
        label.appendChild(document.createTextNode(` ${language.name}`));

        // Add the label to the div
        div.appendChild(label);

        // Add the div to the form
        languageForm.appendChild(div);
    });
}

/**
 * Loads a project with the specified destination languages, captions type, and captions generation status.
 *
 * @param {Array} destLanguages - An array of destination languages.
 * @param {string} captionsType - The type of captions.
 * @param {boolean} areCaptionsGenerated - Indicates whether captions are generated or not.
 * @returns {void}
 */
function loadProject(destLanguages, captionsType, areCaptionsGenerated) {
    selectedLangs = destLanguages;
    if (areCaptionsGenerated) {
        document.querySelector('.generate-captions').disabled = true;
        document.querySelector('.apply-captions').disabled = false;
        document.getElementById('srt').disabled = true;
        document.getElementById('vtt').disabled = true;
    }
    const radio = document.querySelector(`input[name="captionFormat"][value="${captionsType}"]`);
    if (radio) {
        radio.checked = true;
    }
    try {
        updateLanguagesDropdown(selectedLangs);
        updateLanguageForm(selectedLangs);
        addLanguagesToDropdown(selectedLangs);
    } catch (error) {
        window.alert('Error updating languages:', error);
    }
}

/**
 * Retrieves the selected caption type from the radio buttons.
 * @returns {string} The value of the selected caption type.
 */
function getSelectedCaptionType() {
    const radios = document.getElementsByName('captionFormat');

    const selectedRadio = Array.from(radios).find(radio => radio.checked);

    // Return the value of the selected radio button, or 'srt' if no option is selected
    return selectedRadio ? selectedRadio.value : 'srt';
}

// Call updateDropdown when the DOM is loaded
updateLanguagesDropdown(selectedLangs);

// Add an event listener to the checkbox
document.getElementById('is-english-checkbox').addEventListener('change', function() {
    if (this.checked) {
        // If the checkbox is checked, hide the other language label and set the language input's value to "English"
        document.getElementById('language-label').style.display = 'none';
        document.getElementById('language-input').value = 'en';
    } else {
        // If the checkbox is not checked, show the other language label and clear the language input's value
        document.getElementById('language-label').style.display = 'block';
        document.getElementById('language-input').value = '';
    }
});

// Add an event listener to the button
document.getElementById('select-languages-button').addEventListener('click', function() {
    // Show the modal
    document.getElementById('language-modal').style.display = 'block';
});

// Add an event listener to the button
document.getElementById('save-languages-button').addEventListener('click', function() {
    // Hide the modal
    document.getElementById('language-modal').style.display = 'none';
    // Clear the selectedLangs list
    selectedLangs = [];

    // Get all the checkboxes
    const checkboxes = document.getElementById('language-form').querySelectorAll('input[type=checkbox]');

    // Loop through the checkboxes
    checkboxes.forEach(function(checkbox) {
        // If the checkbox is checked, add its value to the selectedLangs list
        if (checkbox.checked) {
            selectedLangs.push(checkbox.value);
        }
    });
     // Update the dropdown
     updateLanguagesDropdown(selectedLangs);
     document.querySelector('.generate-captions').disabled = false;
    document.querySelector('.apply-captions').disabled = false;
});


languages.forEach(function(language) {
    // Create a div
    const div = document.createElement('div');

    // Create a label
    const label = document.createElement('label');

    // Create a checkbox
    const checkbox = document.createElement('input');
    checkbox.type = 'checkbox';
    checkbox.value = language.code;

    // Pre-check the checkbox if the language is in the selectedLanguages list
    if (selectedLangs.includes(language.code)) {
        checkbox.checked = true;
    }
    // If the language is English, make the checkbox always selected and disabled
    if (language.code === 'en') {
        checkbox.checked = true;
        checkbox.disabled = true;
    }
    // Add the checkbox and language name to the label
    label.appendChild(checkbox);
    label.appendChild(document.createTextNode(` ${language.name}`));

    // Add the label to the div
    div.appendChild(label);

    // Add the div to the form
    document.getElementById('language-form').appendChild(div);
});

document.querySelector('.generate-captions').addEventListener('click', function() {
    
    const languageInput = document.getElementById('language-input');
    if (document.getElementById('is-english-checkbox').checked) {
        languageInput.value = 'en';
    }
    const sourceLang = languageInput.value;
    document.querySelector('.generate-captions').disabled = true;
    
    window.pywebview.api.generate_captions(sourceLang, selectedLangs,getSelectedCaptionType())
        .then(function() {
            loadCaptions(document.getElementById('caption-language-dropdown').value);
            document.querySelector('.generate-captions').disabled = true;
            document.getElementById('srt').disabled = true;
            document.getElementById('vtt').disabled = true;             
            document.querySelector('.apply-captions').disabled = false;
            addLanguagesToDropdown(selectedLangs);
        })
        .catch(function(error) {
            window.alert('Soemthing went wrong:', error);
            document.querySelector('.generate-captions').disabled = false;
            document.getElementById('srt').disabled = false;
            document.getElementById('vtt').disabled = false;
        });
});

document.querySelector('.apply-captions').addEventListener('click', function() {
    
    window.pywebview.api.add_captions(selectedLangs)
        .then(function() {
            document.querySelector('.apply-captions').disabled = true;
            document.querySelector('.generate-captions').disabled = true;
        })
        .catch(function(error) {
            window.alert('Error adding captions:', error);
        });
});


// Add an event listener to the dropdown
document.getElementById('caption-language-dropdown').addEventListener('change', function() {
    const selectedLanguage = this.value;

    // Load the captions for the selected language
    loadCaptions(selectedLanguage);
});

// Add an event listener to the button
document.getElementById('save-changes-btn').addEventListener('click', function() {
    // Get all the caption divs
    const captionDivs = document.querySelectorAll('.caption-div');

    // Gather the caption data
    const captions = Array.from(captionDivs).map(function(captionDiv) {
        const timestamp = captionDiv.querySelector('.caption-timestamp').textContent;
        const text = captionDiv.querySelector('.caption-text').textContent;

        // Split the timestamp into start and end
        const [start, end] = timestamp.split(' - ');

        return { start, end, text };
    });

    // Get the currently selected language
    const selectedLanguage = document.getElementById('caption-language-dropdown').value;

    // Call the API function to save the captions
    if (captions.length > 0 && selectedLanguage) {
        window.pywebview.api.save_captions(captions, selectedLanguage)
            .catch(error => window.alert('Error saving captions:', error));
    }

    document.querySelector('.apply-captions').disabled = false;
});