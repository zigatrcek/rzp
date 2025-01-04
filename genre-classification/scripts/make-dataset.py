import os
from pathlib import Path
import csv
import argparse

def is_audio_file(filename):
    """Check if file is an audio file based on extension."""
    audio_extensions = {'.mp3', '.wav', '.flac', '.m4a', '.ogg', '.aac'}
    return Path(filename).suffix.lower() in audio_extensions

def read_csv_paths(csv_file):
    """Read paths from CSV file."""
    keep_files = set()
    with open(csv_file, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            keep_files.add(row['path'])
    return keep_files

def clean_directory(base_dir, keep_files):
    """Remove files not in the keep_files set."""
    removed_count = 0
    for root, _, files in os.walk(base_dir):
        for file in files:
            if is_audio_file(file):
                full_path = os.path.join(root, file)
                if full_path not in keep_files:
                    print(f"Removing: {full_path}")
                    os.remove(full_path)
                    removed_count += 1
    return removed_count

def main():
    parser = argparse.ArgumentParser(description='Clean audio directories based on CSV dataset')
    parser.add_argument('--csv', type=str, required=True, help='Path to the CSV dataset file')
    parser.add_argument('--dir', type=str, required=True, help='Base directory containing genre folders')
    parser.add_argument('--force', action='store_true', help='Skip confirmation prompt')
    args = parser.parse_args()

    base_dir = Path(args.dir)
    if not base_dir.exists():
        print(f"Error: Directory '{base_dir}' does not exist")
        return

    # Read files to keep from CSV
    try:
        keep_files = read_csv_paths(args.csv)
    except FileNotFoundError:
        print(f"Error: CSV file '{args.csv}' not found")
        return

    # Confirmation prompt
    if not args.force:
        print(f"This will delete all audio files in {base_dir} that are not listed in {args.csv}")
        response = input("Are you sure you want to continue? (y/N): ")
        if response.lower() != 'y':
            print("Operation cancelled")
            return

    # Clean directories
    removed_count = clean_directory(base_dir, keep_files)
    print(f"Cleanup complete. Removed {removed_count} files")

if __name__ == "__main__":
    main()
