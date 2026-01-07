# 🌦️ Python Weather Data Analysis & Forecasting

![Python](https://img.shields.io/badge/Python-3.x-blue)
![Meteostat](https://img.shields.io/badge/API-Meteostat-green)
![Status](https://img.shields.io/badge/Status-Active-success)
![License](https://img.shields.io/badge/License-MIT-yellow)

A Python-based weather data analysis and visualization project that retrieves historical weather data using the Meteostat API.  
The application supports multiple South African cities, customizable date ranges, flood risk indicators, statistical analysis, and time-series forecasting.

---

## 📌 Project Overview

This project is an interactive command-line application that enables users to analyze historical weather data for selected locations in South Africa.  
Users can choose the city, date range, indicators, data source, and visualization types, making the analysis flexible and user-driven.

The project is suitable for:
- Academic assignments
- Portfolio demonstrations
- Data analysis and visualization practice

---

## ✨ Key Features

- 📍 Multi-city support  
  - Cape Town  
  - Johannesburg  
  - Durban  
  - Pretoria  
  - Port Elizabeth  

- 📆 Custom start and end date selection  
- 🌡️ Weather indicators:
  - Average temperature
  - Minimum temperature
  - Precipitation
  - Wind speed
  - Atmospheric pressure

- 🌧️ Flood risk classification based on precipitation levels  
- 📊 Visualization options:
  - Line graphs (time series)
  - Bar charts (statistical summaries)
  - Pie charts (indicator contribution)
  - Correlation heatmaps
  - Monthly Top 5 histograms

- 🔮 ARIMA-based forecasting  
- 🧪 Indicator comparison mode  
- 💾 Data export and reload support:
  - CSV
  - Excel
  - JSON
  - XML
  - SQLite database

---

## 🛠️ Technologies Used

- Python
- Pandas
- Matplotlib
- Seaborn
- Meteostat API
- SQLite
- Statsmodels (ARIMA)

---

## 📦 Installation

Make sure Python 3.x is installed, then install the required libraries:

```bash
pip install meteostat pandas matplotlib seaborn statsmodels openpyxl lxml
▶️ How to Run the Project
Clone the repository and run the script:

bash
Copy code
python weather.py
During execution, the program will guide you through:

Selecting a city

Entering a start and end date

Choosing a data source (cloud or saved file)

Selecting weather indicators

Selecting visualization types

Optional forecasting

Optional indicator comparison

📊 Data Analysis & Visualizations
Based on the user’s selections, the application dynamically generates:

📈 Time-series line graphs for selected indicators

🔥 Correlation heatmaps showing relationships between indicators

📊 Statistical summary bar charts

🧮 Monthly Top 5 histograms based on average values

🌧️ Flood risk analysis derived from precipitation data

All visualizations are generated programmatically using Matplotlib and Seaborn.

🌧️ Flood Risk Indicator
Flood risk is calculated using daily precipitation values and classified as follows:

Level	Description
1	Low Risk
2	Moderate Risk
3	High Risk

This provides a simplified assessment of rainfall-related flood potential.

🔮 Forecasting
The project uses an ARIMA (AutoRegressive Integrated Moving Average) model to forecast selected weather indicators.

Forecasting capabilities include:

Short-term future predictions

Visual comparison between historical and forecasted values

User-selected indicators for forecasting

This functionality is intended for analytical and educational use.

🧪 Indicator Comparison Mode
Users can compare two selected indicators on a single graph to:

Observe trends over time

Identify possible relationships

Support exploratory data analysis

📁 Data Storage Formats
Weather data can be saved and reloaded in the following formats:

CSV

Excel

JSON

XML

SQLite database

This allows repeated analysis without re-downloading data from the API.

📌 Use Cases
Academic projects and assignments

Weather trend exploration

Data visualization practice

Portfolio project for internships and graduate roles

🔧 Future Enhancements
Interactive web dashboard (Streamlit or Dash)

Machine learning-based forecasting models

Automated extreme weather alerts

Expanded South African city coverage

Performance optimizations and caching

👤 Author
Sange Mgqamqo
ICT Applications Development Graduate
📍 South Africa
📧 sange7806@gmail.com
