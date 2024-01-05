#IMPORT NECESSARY LIBRARIES 
import pandas as pd
import matplotlib.pyplot as plt

# FILE PATH TO CSV AND MAP IMAGE
csv_file_path = '/Volumes/ExtraStorage /Python2/Archive/GrowLocations.csv'  
map_image_path = '/Volumes/ExtraStorage /Python2/Archive/map7.png'     

# BOUNDING BOX FOR THE UK
lon_min, lon_max = -10.592, 1.6848
lat_min, lat_max = 50.681, 57.985

try:
    # LOAD CSV FILE INTO DATAFRAME
    df = pd.read_csv(csv_file_path)

    # VERIFY AND CORRECT COLUMNS
    expected_columns = ['Latitude', 'Longitude', 'SensorType']
    if not all(col in df.columns for col in expected_columns):
        raise ValueError("Required columns are missing in the dataset.")

    # CONVERT COLUMNS TO CORRECT DATA TYPES
    df['Latitude'] = pd.to_numeric(df['Latitude'], errors='coerce')
    df['Longitude'] = pd.to_numeric(df['Longitude'], errors='coerce')

    # CHECK FOR NaN VALUES IN COLUMNS
    if df[['Latitude', 'Longitude']].isnull().values.any():
        raise ValueError("Latitude or Longitude contains invalid values.")

    # CORRECT THE COLUMNS 
    if df['Latitude'].min() < lat_min or df['Latitude'].max() > lat_max:
        df.rename(columns={'Latitude': 'temp', 'Longitude': 'Latitude'}, inplace=True)
        df.rename(columns={'temp': 'Longitude'}, inplace=True)

    # FILTER DATA FOR VALID LATITUDE AND LONGITUDE WITHIN UK RANGE 
    df_filtered = df[(df['Latitude'] >= lat_min) & (df['Latitude'] <= lat_max) &
                     (df['Longitude'] >= lon_min) & (df['Longitude'] <= lon_max)]

    # LOAD MAP IMAGE
    map_img = plt.imread(map_image_path)

    # PLOT SENSOR LOCATIONS
    fig, ax = plt.subplots(figsize=(10, 12))
    ax.imshow(map_img, extent=[lon_min, lon_max, lat_min, lat_max], aspect='auto')

    # PLOT SENSORS WITH DIFFERENT COLOURS FOR WACH SENSOR TYPE 
    if 'SensorType' in df_filtered.columns:
        sensor_types = df_filtered['SensorType'].unique()
        colors = plt.cm.get_cmap('tab10', len(sensor_types))
        for i, sensor_type in enumerate(sensor_types):
            subset = df_filtered[df_filtered['SensorType'] == sensor_type]
            size = 15 if sensor_type == 'Flower Power' else 100  
            ax.scatter(subset['Longitude'], subset['Latitude'], color=colors(i), label=sensor_type, s=size)
        ax.legend()

    # CUSTOMIZE APPEARANCE
    ax.set_title('Sensor Locations in the UK', fontsize=16)
    ax.axis('off')

    plt.show()

except FileNotFoundError:
    print(f"Error: File not found. Please check the file path for '{csv_file_path}' and '{map_image_path}'.")
except pd.errors.EmptyDataError:
    print("Error: The provided CSV file is empty.")
except ValueError as ve:
    print(f"Data Validation Error: {ve}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")


