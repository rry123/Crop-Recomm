import React, { useState } from "react";
import config from "./config"; // Import API key from config.ts
import './App.css';

const App: React.FC = () => {
  const [features, setFeatures] = useState({
    Nitrogen: "",
    Phosphorus: "",
    Pottassium: "",
    PH: "",
    Rainfall: "",
  });

  const [location, setLocation] = useState("");
  const [temperature, setTemperature] = useState<number | null>(null);
  const [humidity, setHumidity] = useState<number | null>(null);
  const [prediction, setPrediction] = useState<string | null>(null);

  // Fetch weather data based on location
  const fetchWeather = async () => {
    try {
      if (!location) {
        alert("Please enter a location.");
        return;
      }

      const response = await fetch(
        `https://api.openweathermap.org/data/2.5/weather?q=${location}&appid=${config.WEATHER_API_KEY}&units=metric`
      );

      if (!response.ok) throw new Error("Failed to fetch weather data");

      const data = await response.json();
      setTemperature(data.main.temp);
      setHumidity(data.main.humidity);
    } catch (error) {
      console.error("Error fetching weather data:", error);
      alert("Failed to fetch weather data. Check the location.");
    }
  };

  // Handle input changes for other features
  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFeatures({
      ...features,
      [e.target.name]: e.target.value,
    });
  };

  // Handle Prediction Request
  const handlePredict = async () => {
    try {
      if (temperature === null || humidity === null) {
        alert("Please fetch weather data first.");
        return;
      }

      const response = await fetch("https://crop-recomm.onrender.com/predict", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          feature1: parseFloat(features.Nitrogen),
          feature2: parseFloat(features.Phosphorus),
          feature3: parseFloat(features.Pottassium),
          feature4: temperature, // Fetched from API
          feature5: humidity, // Fetched from API
          feature6: parseFloat(features.PH),
          feature7: parseFloat(features.Rainfall),
        }),
      });

      if (!response.ok) throw new Error("Error predicting crop");

      const data = await response.json();
      setPrediction(data.prediction);
    } catch (error) {
      setPrediction("Error predicting crop");
    }
  };

  return (
    <div className="app-container">
      <h1>Crop Prediction</h1>

      <div className="input-container">
        <label className="label">Enter Location:</label>
        <input
          type="text"
          value={location}
          onChange={(e) => setLocation(e.target.value)}
          className="input"
        />
      </div> 


      <div className="f-button">
        <button onClick={fetchWeather} className="button">
          Fetch Weather
        </button>
      </div>

      {temperature !== null && humidity !== null && (
        <div className="weather-info">
          <p>🌡 Temperature: {temperature} °C</p>
          <p>💧 Humidity: {humidity} %</p>
        </div>
      )}

      <div className="features-container">
        {Object.keys(features).map((key, index) => (
          <div key={index} className="feature-input">
            <label className="label">{key}:</label>
            <input
              type="number"
              name={key}
              value={features[key as keyof typeof features]}
              onChange={handleChange}
              className="input"
            />
          </div>
        ))}
        <button onClick={handlePredict} className="button">
          Predict
        </button>
      </div>

      {prediction && <h2 className="prediction-result">Predicted Crop: {prediction}</h2>}
    </div>
  );
};

export default App;
