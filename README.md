# Smart Study Companion 

A lightweight, terminal-based Python tool designed to help students and professionals optimize their breaks. By entering a city name, the script checks real-time weather conditions and air quality metrics to recommend whether it's a great time for an outdoor walk or if staying inside is the healthier option.

##  Features
* **Global Geocoding:** Type any major city, and the tool dynamically resolves its latitude and longitude.
* **Real-time Weather Metrics:** Fetches live temperature, "feels like" temperature, humidity, and precipitation data using the Open-Meteo API.
* **Air Quality Check:** Evaluates live US AQI (Air Quality Index) parameters.
* **Smart Decision Logic:** Instantly analyzes parameters against strict comfort thresholds (Rain, Temperature boundaries, and Pollution).
* **Robust Error Handling:** Designed with defensive coding to handle API timeouts, empty inputs, or missing data points gracefully.

##  How It Works
The application works in three sequential steps:
1. **Geocoding:** Converts your text input (e.g., "Paris") into geographical coordinates.
2. **Data Fetching:** Dispatches parallel data queries to Open-Meteo's Weather and Air Quality forecast engines.
3. **Condition Analysis:** Compares conditions against baseline safety comfort zones:
   * **Precipitation:** $> 0\text{ mm}$ triggers an indoor recommendation.
   * **Temperature:** Must be between $10^\circ\text{C}$ and $32^\circ\text{C}$.
   * **Air Quality Index:** Must be $\le 100$ AQI.

##  Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/YOUR_USERNAME/weather-aqi-companion.git](https://github.com/aksdhama0067/weather-aqi-companion.git)
   cd aksdhama0067
