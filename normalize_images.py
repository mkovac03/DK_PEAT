import os
import numpy as np
import rasterio
import pandas as pd
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor, as_completed
import config  # Import configuration from config.py


def load_stats_from_csv(csv_path):
    """Load the statistics (mean, std) for each folder and band from the respective CSV."""
    return pd.read_csv(csv_path)


def normalize_image(image, mean, std):
    """Normalize the image to 0 mean and unit variance."""
    return (image - mean) / std


def process_and_save_image(file_path, means, stds, num_bands, normalized_base_folder, original_base_folder):
    """Process and save the normalized image, skipping if the normalized file already exists."""

    # Calculate relative path of file from the original base folder
    relative_path = os.path.relpath(file_path, original_base_folder)

    # Ensure that the relative subfolder structure is maintained inside the normalized folder
    normalized_file_path = os.path.join(normalized_base_folder, relative_path)
    normalized_file_dir = os.path.dirname(normalized_file_path)

    # Ensure the directory exists
    os.makedirs(normalized_file_dir, exist_ok=True)

    # Check if the normalized image already exists
    if os.path.exists(normalized_file_path):
        print(f"Normalized file already exists, skipping: {normalized_file_path}")
        return

    with rasterio.open(file_path) as src:
        profile = src.profile
        profile.update(dtype=rasterio.float32)

        # Normalize each band
        normalized_bands = []
        for band in range(1, num_bands + 1):
            image = src.read(band).astype(np.float32)
            normalized_image = normalize_image(image, means[band - 1], stds[band - 1])
            normalized_bands.append(normalized_image)

        # Write the normalized image back to disk
        with rasterio.open(normalized_file_path, 'w', **profile) as dst:
            for band in range(1, num_bands + 1):
                dst.write(normalized_bands[band - 1], band)


def normalize_folder(folder_path, stats_df):
    """Normalize all .tif files in a folder using the global mean and std for each band."""

    # Create a subfolder for normalized images inside the folder's "normalized" directory
    normalized_base_folder = os.path.join(folder_path, config.normalized_subfolder)
    os.makedirs(normalized_base_folder, exist_ok=True)

    # Get the means and stds for each band
    means = stats_df["mean"].values
    stds = stats_df["std"].values
    num_bands = len(means)

    # Find all .tif files in the folder (not subfolders)
    tif_files = [file for file in os.listdir(folder_path) if file.endswith('.tif')]

    print(f"Normalizing images in folder: {folder_path}")

    with ThreadPoolExecutor() as executor:
        futures = []
        for file in tif_files:
            file_path = os.path.join(folder_path, file)
            futures.append(
                executor.submit(process_and_save_image, file_path, means, stds, num_bands, normalized_base_folder,
                                folder_path))

        for future in tqdm(as_completed(futures), total=len(futures), desc="Normalizing files", unit="file"):
            future.result()


def normalize_images():
    """Main function to normalize images using statistics from CSV files."""
    for folder in config.folders:
        csv_path = f"{folder}{config.csv_suffix}"  # Fixed by adding a separator before config.csv_suffix
        stats_df = load_stats_from_csv(csv_path)
        normalize_folder(folder, stats_df)


# If you want this script to run standalone as well
if __name__ == "__main__":
    normalize_images()
