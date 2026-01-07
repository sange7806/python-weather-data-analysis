from meteostat import Point, Daily
from datetime import datetime, date
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sqlite3
import os
from statsmodels.tsa.arima.model import ARIMA

pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)
sns.set(style="whitegrid")
colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b']

# ============================================================
#                   SELECT CITY
# ============================================================
cities = {
    "1": {"name": "Cape Town", "coords": (-33.9249, 18.4241)},
    "2": {"name": "Johannesburg", "coords": (-26.2041, 28.0473)},
    "3": {"name": "Durban", "coords": (-29.8587, 31.0218)},
    "4": {"name": "Pretoria", "coords": (-25.7479, 28.2293)},
    "5": {"name": "Port Elizabeth", "coords": (-33.9613, 25.6122)}
}

print("Select a city to view weather data:")
for key, city in cities.items():
    print(f"{key} = {city['name']}")
city_choice = input("Enter number: ").strip()
if city_choice not in cities:
    raise ValueError("Invalid city choice")

location_name = cities[city_choice]["name"]
lat, lon = cities[city_choice]["coords"]
location = Point(lat, lon)

# ============================================================
#                SPECIFY DATE RANGE
# ============================================================
print("\nEnter the period for data analysis (YYYY-MM-DD format)")
start_input = input("Start date (e.g., 2023-01-01): ").strip()
end_input = input("End date (e.g., 2023-12-31): ").strip()

try:
    start = datetime.strptime(start_input, "%Y-%m-%d")
    end = datetime.strptime(end_input, "%Y-%m-%d")
    if start > end:
        raise ValueError("Start date must be before end date")
except Exception as e:
    raise ValueError(f"Invalid date input: {e}")

# Limit end date to today to avoid future data errors
today = date.today()
if end.date() > today:
    print(f"End date {end.date()} is in the future. Adjusting to today ({today}).")
    end = datetime(today.year, today.month, today.day)

# ============================================================
#                  DOWNLOAD WEATHER DATA
# ============================================================
data_weather = Daily(location, start, end).fetch().reset_index()

if data_weather.empty:
    raise ValueError(f"No weather data available for {location_name} from {start.date()} to {end.date()}.")

# ============================================================
#                  PREPARE DATAFRAME
# ============================================================
columns_weather = [{
    'date': row.get('time'),
    'temperature': row.get('tavg'),
    'min_temperature': row.get('tmin'),
    'precipitation': row.get('prcp'),
    'wind_speed': row.get('wspd'),
    'pressure': row.get('pres')
} for _, row in data_weather.iterrows()]

df_weather = pd.DataFrame(columns_weather)

# ============================================================
#                FLOOD RISK INDICATOR
# ============================================================
def calculate_flood_risk(row):
    if pd.isna(row['precipitation']):
        return 0
    if row['precipitation'] < 5:
        return 1
    elif row['precipitation'] < 20:
        return 2
    else:
        return 3

df_weather['flood_risk'] = df_weather.apply(calculate_flood_risk, axis=1)

# ============================================================
#                    SAVE DATA
# ============================================================
os.makedirs("weather_data", exist_ok=True)

df_weather.to_csv(f"weather_data/{location_name}_weather.csv", index=False)
df_weather.to_excel(f"weather_data/{location_name}_weather.xlsx", index=False)
df_weather.to_json(f"weather_data/{location_name}_weather.json", orient='records', date_format='iso')
df_weather.to_xml(f"weather_data/{location_name}_weather.xml", index=False)

conn = sqlite3.connect(f"weather_data/{location_name}_weather.db")
df_weather.to_sql("weather", conn, if_exists="replace", index=False)
conn.close()

# Load saved versions
dataframe_csv = pd.read_csv(f"weather_data/{location_name}_weather.csv")
dataframe_excel = pd.read_excel(f"weather_data/{location_name}_weather.xlsx")
dataframe_json = pd.read_json(f"weather_data/{location_name}_weather.json")
dataframe_xml = pd.read_xml(f"weather_data/{location_name}_weather.xml")
conn = sqlite3.connect(f"weather_data/{location_name}_weather.db")
dataframe_sql = pd.read_sql("SELECT * FROM weather", conn)
conn.close()

dataframes = [df_weather, dataframe_csv, dataframe_excel, dataframe_json, dataframe_xml, dataframe_sql]

# ============================================================
#              USER CHOOSES DATA SOURCE
# ============================================================
print("\nChoose data source to analyze:")
print("0 = CLOUD\n1 = CSV\n2 = EXCEL\n3 = JSON\n4 = XML\n5 = SQL")
file_choice = int(input("Enter number (0-5): "))
active_dataframe = dataframes[file_choice]
active_dataframe['date'] = pd.to_datetime(active_dataframe['date'])

# ============================================================
#                  INDICATOR SELECTION
# ============================================================
print("\nChoose indicator(s) to analyze:")
print("1 = Average Temperature\n2 = Minimum Temperature\n3 = Precipitation\n4 = Wind Speed\n5 = Pressure\n6 = Flood Risk")

indicator_map = {
    "1": "temperature",
    "2": "min_temperature",
    "3": "precipitation",
    "4": "wind_speed",
    "5": "pressure",
    "6": "flood_risk"
}

indicator_input = input("Enter numbers separated by commas (e.g. 1,3,6): ")
selected_indicators = [indicator_map[i.strip()] for i in indicator_input.split(",") if i.strip() in indicator_map]

active_dataframe = active_dataframe[['date'] + selected_indicators].copy()
active_dataframe.fillna(active_dataframe.mean(numeric_only=True), inplace=True)

# ============================================================
#                  GRAPH SELECTION
# ============================================================
print("\nChoose which graphs to view (separate by commas):")
print("1 = Line Graph (Time Series)\n2 = Bar Graph (Statistical Summary)\n3 = Pie Chart (Average Contributions)\n4 = Heatmap (Correlation Matrix)\n5 = Monthly Top 5 Histogram")
graph_input = input("Enter numbers separated by commas: ")
graph_choices = [int(x.strip()) for x in graph_input.split(",")]

# ============================================================
#                  HEATMAP
# ============================================================
if 4 in graph_choices:
    corr = active_dataframe[selected_indicators].corr()
    print("\nCorrelation Matrix:")
    print(corr)
    sns.heatmap(corr, annot=True, cmap='coolwarm')
    plt.title(f"Correlation Matrix – {location_name}")
    plt.show()

# ============================================================
#                  PIE CHART
# ============================================================
if 3 in graph_choices and len(selected_indicators) > 1:
    means = active_dataframe[selected_indicators].mean()
    plt.figure(figsize=(7,7))
    plt.pie(means, labels=means.index, autopct='%1.1f%%', startangle=90)
    plt.title(f"Average Contribution of Selected Indicators – {location_name}")
    plt.axis('equal')
    plt.show()

# ============================================================
#                  LINE OR BAR GRAPH
# ============================================================
if 1 in graph_choices or 2 in graph_choices:
    plt.figure(figsize=(12,6))
    if 1 in graph_choices:
        for i, col in enumerate(selected_indicators):
            plt.plot(active_dataframe['date'], active_dataframe[col], label=col.capitalize(), color=colors[i % len(colors)], marker='o')
        plt.title(f"Weather Indicators Over Time – {location_name}")
        plt.xlabel("Date")
        plt.ylabel("Values")
        plt.xticks(rotation=45)
        plt.grid(True, linestyle='--', alpha=0.6)
        plt.legend()
        plt.tight_layout()
        plt.show()

    if 2 in graph_choices:
        stats = active_dataframe[selected_indicators].describe().T
        stats.rename(columns={'50%': 'median'}, inplace=True)
        stats[['mean','median','max']].plot(kind='bar', figsize=(10,5))
        plt.title(f"Statistical Summary – {location_name}")
        plt.ylabel("Values")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

# ============================================================
#                  MONTHLY TOP 5 HISTOGRAM
# ============================================================
if 5 in graph_choices:
    active_dataframe['month'] = active_dataframe['date'].dt.to_period('M').astype(str)
    monthly_avg = active_dataframe.groupby('month')[selected_indicators].mean()
    top5_months = monthly_avg.sort_values(by=selected_indicators[0], ascending=False).head(5)
    plt.figure(figsize=(10,6))
    top5_months.plot(kind='bar', color=colors[:len(selected_indicators)])
    plt.title(f"Top 5 Months by Average {selected_indicators[0].capitalize()} – {location_name}")
    plt.xlabel("Month")
    plt.ylabel("Average Value")
    plt.xticks(rotation=45)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()

# ============================================================
#                  FORECASTING
# ============================================================
forecast_choice = input("\nDo you want to forecast an indicator? (y/n): ").lower()
if forecast_choice == 'y':
    print("\nSelect indicator to forecast:")
    for i, ind in enumerate(selected_indicators):
        print(f"{i+1} = {ind.capitalize()}")
    f_choice = int(input("Enter number: "))
    f_indicator = selected_indicators[f_choice-1]
    series = active_dataframe.set_index('date')[f_indicator].dropna()
    model = ARIMA(series, order=(5,1,0))
    fit_model = model.fit()
    forecast = fit_model.forecast(10)
    forecast_dates = pd.date_range(series.index[-1] + pd.Timedelta(days=1), periods=10)
    plt.figure(figsize=(12,6))
    plt.plot(series.index, series, label="Historical", marker='o')
    plt.plot(forecast_dates, forecast, label="Forecast", linestyle='--', color='red', marker='x')
    plt.title(f"Forecast for {f_indicator.capitalize()} – {location_name}")
    plt.xlabel("Date")
    plt.ylabel("Value")
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.tight_layout()
    plt.show()

# ============================================================
#                  INDICATOR COMPARISON
# ============================================================
compare_choice = input("\nDo you want to compare two indicators? (y/n): ").lower()
if compare_choice == 'y':
    print("\nSelect two indicators to compare:")
    for i, ind in enumerate(selected_indicators):
        print(f"{i+1} = {ind.capitalize()}")
    i1, i2 = [selected_indicators[int(x)-1] for x in input("Enter two numbers separated by comma: ").split(',')]
    plt.figure(figsize=(12,6))
    plt.plot(active_dataframe['date'], active_dataframe[i1], label=i1.capitalize(), marker='o')
    plt.plot(active_dataframe['date'], active_dataframe[i2], label=i2.capitalize(), marker='x')
    plt.title(f"Comparison: {i1.capitalize()} vs {i2.capitalize()} – {location_name}")
    plt.xlabel("Date")
    plt.ylabel("Values")
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.tight_layout()
    plt.show()
