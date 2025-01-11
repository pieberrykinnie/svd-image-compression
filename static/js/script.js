const form = document.querySelector('form');
const output = document.querySelector('#comparison');

form.addEventListener('submit', (e) => {
    e.preventDefault();
    const formData = new FormData(form);

    fetch('/upload', {
        method: 'POST',
        body: formData
    })
    .then(response => response.text())
    .then(data => {
        const img = document.createElement('img');
        img.src = data;
        output.appendChild(img);
    })
    .catch(error => console.error('Error:', error));
});