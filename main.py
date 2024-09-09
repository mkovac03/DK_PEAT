# main.py

# Import the main functions from both scripts
from calculate_stats import calculate_stats
from normalize_images import normalize_images


def main():
    # Run the two scripts in sequence
    print("Starting calculation of global statistics...")
    calculate_stats()

    print("Global statistics calculated. Now starting normalization of images...")
    normalize_images()
    print("Image normalization complete.")


if __name__ == "__main__":
    main()
