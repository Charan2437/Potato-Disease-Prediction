import React, { useState } from 'react';
import axios from 'axios';

function App() {
  const [file, setFile] = useState(null);
  const [prediction, setPrediction] = useState(null);

  const onFileChange = event => {
    setFile(event.target.files[0]);
  };

  const onFormSubmit = event => {
    event.preventDefault();

    const formData = new FormData();
    formData.append('file', file);

    axios.post('http://localhost:8000/predict', formData)
      .then(response => {
        setPrediction(response.data);
      })
      .catch(error => {
        console.error(error);
      });
  };

  return (
    <div>
      <form onSubmit={onFormSubmit}>
        <input type="file" onChange={onFileChange} />
        <button type="submit">Predict</button>
      </form>
      {prediction && (
        <div>
          <p>Predicted Class: {prediction.class}</p>
          <p>Confidence: {prediction.confidence}</p>
        </div>
      )}
    </div>
  );
}

export default App;