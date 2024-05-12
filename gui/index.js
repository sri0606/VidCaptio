function loadVideo(url) {
    var video = document.getElementById('video-player');
    video.src = url;
}

var sourceLang = document.getElementById('source-lang');
var destLang = document.getElementById('dest-lang');

var languages = [
  { code: 'en', name: 'English' },
  { code: 'es', name: 'Spanish' },
  { code: 'fr', name: 'French' },
  // Add more languages as needed
];

languages.forEach(function(language) {
    var option = new Option(language.name, language.code);
  
    // Add to source language dropdown
    sourceLang.options.add(option);
  
    // Add to destination language dropdown
    var destOption = option.cloneNode(true);
    if (language.code === 'en') {
      destOption.selected = true;
    }
    destLang.options.add(destOption);
  });

document.getElementById('dest-lang').addEventListener('change', function() {
    var selectedLangs = Array.from(this.selectedOptions).map(function(option) {
        return option.text;
    });

    document.getElementById('selected-langs').textContent = 'Selected languages: ' + selectedLangs.join(', ');
});

document.querySelector('.generate-captions').addEventListener('click', function() {
    var sourceLang = document.getElementById('source-lang').value;
    var destLangs = Array.from(document.getElementById('dest-lang').selectedOptions).map(function(option) {
        return option.value;
    });


    window.pywebview.api.generate_captions(sourceLang, destLangs).then(function(captions) {
        var captionsContainer = document.querySelector('.captions-container');
        captionsContainer.innerHTML = ''; // Clear the caption container
    
        captions.forEach(function(caption) {
            var captionDiv = document.createElement('div');
            captionDiv.className = 'caption-div';
    
            var timestamp = document.createElement('p');
            timestamp.className = 'caption-timestamp';
            timestamp.textContent = caption.start + ' - ' + caption.end;
            captionDiv.appendChild(timestamp);
    
            var text = document.createElement('p');
            text.className = 'caption-text';
            text.textContent = caption.text;
            text.contentEditable = 'true'; 
            captionDiv.appendChild(text);
    
            captionsContainer.appendChild(captionDiv);
        });
    });
});