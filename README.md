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
