import os
import numpy as np
import rasterio
import pandas as pd
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed
import config  # Import configuration from config.py


def compute_global_mean_std(folder_path):
    """Compute the global mean and standard deviation for each band in the .tif files."""

    # Find all .tif files in the current folder (not subfolders)
    tif_files = [file for file in os.listdir(folder_path) if file.endswith('.tif')]

    # If no .tif files are found, skip processing
    if not tif_files:
        print(f"No .tif files found in folder: {folder_path}")
        return None, None, None

    # Open the first file to determine the number of bands
    with rasterio.open(os.path.join(folder_path, tif_files[0])) as src:
        num_bands = src.count

    # Initialize total sum, sum of squares, and pixel count for each band
    total_sum = np.zeros(num_bands)
    total_sum_sq = np.zeros(num_bands)
    total_pixels = np.zeros(num_bands)

    print(f"Calculating global mean and standard deviation for folder: {folder_path}")

    def process_file(file_path):
        with rasterio.open(file_path) as src:
            sums = np.zeros(num_bands)
            sums_sq = np.zeros(num_bands)
            pixels = np.zeros(num_bands)
            for band in range(1, num_bands + 1):
                image = src.read(band).astype(np.float32)
                sums[band - 1] = np.sum(image)
                sums_sq[band - 1] = np.sum(image ** 2)
                pixels[band - 1] = image.size
            return sums, sums_sq, pixels

    # Use a ThreadPool to process files in parallel
    with ThreadPoolExecutor() as executor:
        futures = {executor.submit(process_file, os.path.join(folder_path, file)): file for file in tif_files}
        for future in tqdm(as_completed(futures), total=len(futures), desc="Processing files", unit="file"):
            sum_image, sum_image_sq, size = future.result()
            total_sum += sum_image
            total_sum_sq += sum_image_sq
            total_pixels += size

    # Calculate mean and standard deviation for each band
    mean = total_sum / total_pixels
    std = np.sqrt((total_sum_sq / total_pixels) - (mean ** 2))

    print(f"Finished calculating means and stds for folder: {folder_path}\n")

    return mean, std, num_bands


def save_stats_to_csv(folder_path, mean, std, num_bands):
    """Save the global statistics (mean, std) to a CSV file for each folder."""
    # Create a DataFrame to hold the statistics
    data = []
    for band in range(1, num_bands + 1):
        data.append([folder_path, band, mean[band - 1], std[band - 1]])

    df = pd.DataFrame(data, columns=["folder_path", "band", "mean", "std"])

    # Define the CSV file path for the folder
    csv_path = f"{folder_path}{config.csv_suffix}"

    # Save the CSV file
    df.to_csv(csv_path, index=False)
    print(f"Saved statistics for folder: {folder_path} to {csv_path}")


# Calculate statistics for each folder and save to separate CSVs
for folder in config.folders:
    mean, std, num_bands = compute_global_mean_std(folder)
    if mean is not None:
        save_stats_to_csv(folder, mean, std, num_bands)
