Here’s an updated version of the `README.md` file, reflecting the changes where the `calculate_stats.py` script now skips processing if the CSV file already exists:

---

# Image Normalization Workflow

This project contains three main Python scripts for calculating the global mean and standard deviation of satellite image bands, and for normalizing the images based on those statistics. The process is separated into the following steps:

1. **Calculate Global Statistics**: The `calculate_stats.py` script calculates the mean and standard deviation for each band across all images in a set of folders and saves the statistics in a separate CSV file for each folder. If the CSV file already exists, the folder is skipped.
2. **Normalize Images**: The `normalize_images.py` script normalizes the images using the calculated statistics from each folder's CSV file.
3. **Run Both Scripts Sequentially**: The `main.py` script runs the two scripts (`calculate_stats.py` and `normalize_images.py`) in sequence to streamline the workflow.

### Table of Contents

- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
  - [Step 1: Calculate Global Statistics](#step-1-calculate-global-statistics)
  - [Step 2: Normalize Images](#step-2-normalize-images)
  - [Step 3: Running Both Steps Sequentially](#step-3-running-both-steps-sequentially)
- [Folder Structure](#folder-structure)
- [Notes](#notes)

---

## Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/mkovac03/DK_PEAT.git
   cd DK_PEAT
   ```

2. **Install the required dependencies**:

   Ensure you have Python 3.7 or later installed. Install the dependencies using `pip`:

   ```bash
   pip install -r requirements.txt
   ```

   The following Python packages are required:
   
   - `numpy`
   - `pandas`
   - `rasterio`
   - `tqdm`
   - `concurrent.futures` (part of the Python standard library)

---

## Configuration

The project uses a configuration file (`config.py`) to define folder paths and other settings. This file contains the following configurable parameters:

```python
# config.py

# List of folder paths to process
folders = [
    "/path/to/folder1",
    "/path/to/folder2",
    "/path/to/folder3"
]

# Name of the subfolder where normalized images will be saved
normalized_subfolder = "normalized"

# Define the suffix for the CSV files that will store global statistics for each folder
csv_suffix = "_stats.csv"
```

### Parameters:

- **folders**: A list of folder paths where your `.tif` image files are stored. The paths should be either absolute or relative to the script’s location.
- **normalized_subfolder**: The subfolder where normalized images will be saved. This folder will be created inside each image folder.
- **csv_suffix**: The suffix for the CSV file that will be created for each folder to store the global mean and standard deviation for each band.

---

## Usage

The process is divided into three steps:

### Step 1: Calculate Global Statistics

The `calculate_stats.py` script calculates the global mean and standard deviation for each band in the `.tif` files within the specified folder and saves the results to a CSV file. If the CSV file already exists, the script skips processing for that folder.

To calculate the statistics, run the following command:

```bash
python calculate_stats.py
```

This script will:

- Read the folder paths from `config.py`.
- Calculate the mean and standard deviation for each band in all `.tif` files in each folder.
- Save the statistics (folder path, band, mean, and std) to a CSV file with the name `folder_path_stats.csv`.
- **Skip processing** for folders where the CSV file already exists.

### Step 2: Normalize Images

The `normalize_images.py` script normalizes the images based on the global statistics saved in the CSV file.

To normalize the images, run the following command:

```bash
python normalize_images.py
```

This script will:

- Read the folder paths and the saved statistics from each folder's CSV file (e.g., `folder1_stats.csv`).
- Normalize each `.tif` image using the corresponding mean and standard deviation for each band.
- Save the normalized images in a subfolder (`normalized`) within the original folder.

### Step 3: Running Both Steps Sequentially

The `main.py` script combines both steps into a single workflow by running the `calculate_stats.py` script first and then the `normalize_images.py` script in sequence.

To run both scripts sequentially, use:

```bash
python main.py
```

This will:

- First calculate global statistics for each folder (skipping folders where the CSV file already exists).
- Then normalize the images based on the calculated statistics.

---

## Folder Structure

Here’s an example of what your folder structure should look like:

```
├── calculate_stats.py
├── normalize_images.py
├── main.py
├── config.py
├── /media/lkm413/storage3/DK_PEAT/images/
│   ├── Planet/DK/clipped_images/
│   │   ├── image1.tif
│   │   ├── image2.tif
│   │   ├── clipped_images_stats.csv    # Generated by calculate_stats.py
│   │   └── normalized/                 # Normalized images will be saved here
│   ├── S1/
│   │   ├── image1.tif
│   │   ├── image2.tif
│   │   ├── S1_stats.csv                # Generated by calculate_stats.py
│   │   └── normalized/                 # Normalized images will be saved here
│   └── S2/
│       ├── image1.tif
│       ├── image2.tif
│       ├── S2_stats.csv                # Generated by calculate_stats.py
│       └── normalized/                 # Normalized images will be saved here
```

- Each folder contains `.tif` files directly in the folder (no subfolders are processed).
- The `*_stats.csv` files store the global mean and standard deviation for each band.
- Normalized images are stored in the `normalized` subfolder created by the scripts.

---

## Notes

- **Skipping Processed Folders**: The `calculate_stats.py` script checks for the existence of the CSV file for each folder. If it exists, it skips processing for that folder, ensuring that no redundant calculations are made.
- **No Subfolder Processing**: Only `.tif` files directly inside the specified folders are processed. Subdirectories are ignored.
- **Folder Permissions**: Ensure you have appropriate read/write permissions for the folders where images are stored and where results will be saved.
- **Parallel Processing**: The scripts use multithreading to speed up the computation and normalization of large datasets.

---

