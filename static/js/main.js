const form = document.querySelector('#upload-form');
const fileInput = document.querySelector('#file-input');
const resultContainer = document.querySelector('#result-container');
const predictedClass = document.querySelector('#predicted-class');
const score = document.querySelector('#score');

form.addEventListener('submit', async (event) => {
    event.preventDefault();

    const formData = new FormData();
    formData.append('file', fileInput.files[0]);

    try {
        const response = await fetch('/predict', {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        predictedClass.textContent = `Predicted class: ${data.predicted_class}`;
        score.textContent = `Score: ${data.score}`;
        resultContainer.classList.remove('hidden');
    } catch (error) {
        console.error(error);
    }
});
