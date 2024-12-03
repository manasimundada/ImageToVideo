// Function to handle music selection
document.getElementById('music-input').addEventListener('change', function(event) {
    const selectedFiles = event.target.files;
    if (selectedFiles.length > 0) {
        const fileName = selectedFiles[0].name;
        document.getElementById('music-file-info').innerText = `Selected file: ${fileName}`;
    } else {
        document.getElementById('music-file-info').innerText = 'Select Music File';
    }
});

// Function to add input fields for image durations based on the number of files selected
document.getElementById('music-input').addEventListener('change', function(event) {
    const numFiles = event.target.files.length;
    const durationInputs = document.getElementById('duration-inputs');
    durationInputs.innerHTML = ''; // Clear existing inputs

    for (let i = 0; i < numFiles; i++) {
        const input = document.createElement('input');
        input.type = 'number';
        input.placeholder = 'Duration';
        input.min = '1';
        durationInputs.appendChild(input);
    }
});
// Function to handle file upload
document.getElementById('multiple-uploader').addEventListener('change', function(event) {
    const numFiles = event.target.files.length;
    const durationInputs = document.getElementById('duration-inputs');
    durationInputs.innerHTML = ''; // Clear existing inputs

    for (let i = 0; i < numFiles; i++) {
        const input = document.createElement('input');
        input.type = 'number';
        input.placeholder = 'Duration';
        input.min = '1';
        durationInputs.appendChild(input);
    }
});


// Function to handle applying transition effect
document.getElementById('transition-select').addEventListener('change', function(event) {
    const selectedTransition = event.target.value;
    console.log('Selected transition:', selectedTransition);
});

document.getElementById('upload-button').addEventListener('click', function() {
    // Redirect to the /upload route
    window.location.href = '/upload';
  });  
