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
    for col in expected_columns:
        if col not in df.columns:
            raise ValueError(f"Required column '{col}' is missing in the dataset.")

    # FILTER DATA FOR VALID LATITUDE AND LONGITUDE
    df_filtered = df[(df['Latitude'] >= lat_min) & (df['Latitude'] <= lat_max) &
                     (df['Longitude'] >= lon_min) & (df['Longitude'] <= lon_max)]

    # LOAD MAP IMAGE
    map_img = plt.imread(map_image_path)

    # CREATE SCATTER PLOTS
    fig, ax = plt.subplots(figsize=(10, 12))
    ax.imshow(map_img, extent=[lon_min, lon_max, lat_min, lat_max], aspect='auto')

    # PLOTTING SENSORS
    if 'SensorType' in df_filtered.columns:
        sensor_types = df_filtered['SensorType'].unique()
        colors = plt.cm.get_cmap('tab10', len(sensor_types))
        for i, sensor_type in enumerate(sensor_types):
            subset = df_filtered[df_filtered['SensorType'] == sensor_type]
            size = 15 if sensor_type == 'Flower Power' else 100  # Customize as needed
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
