import os
from pathlib import Path
import csv
import random
import argparse

def is_audio_file(filename):
    """Check if file is an audio file based on extension."""
    audio_extensions = {'.mp3', '.wav', '.flac', '.m4a', '.ogg', '.aac'}
    return Path(filename).suffix.lower() in audio_extensions

def collect_audio_files(genre_path):
    """Collect all audio files in a directory and its subdirectories."""
    audio_files = []
    for root, _, files in os.walk(genre_path):
        for file in files:
            if is_audio_file(file):
                audio_files.append(os.path.join(root, file))
    return audio_files

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Create a dataset of audio files from genre folders.')
    parser.add_argument('--path', type=str, default=None, help='Path to the root directory containing genre folders')
    args = parser.parse_args()
    
    # Get the base directory (use provided path or current directory)
    base_dir = Path(args.path) if args.path else Path.cwd()
    if not base_dir.exists():
        print(f"Error: Directory '{base_dir}' does not exist")
        return
    
    # Dictionary to store genre and corresponding files
    genre_files = {}
    
    # Collect genres (top-level directories)
    for item in base_dir.iterdir():
        if item.is_dir():
            genre = item.name
            files = collect_audio_files(item)
            
            # Sample 25 files if more are available
            if len(files) > 25:
                files = random.sample(files, 25)
            elif len(files) == 0:
                continue
                
            genre_files[genre] = files
    
    # Write results to CSV
    output_file = 'genre_dataset.csv'
    with open(output_file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['path', 'genre'])  # Header
        
        for genre, files in genre_files.items():
            for file_path in files:
                writer.writerow([file_path, genre])
    
    print(f"Dataset created in {output_file}")
    print("Summary of files per genre:")
    for genre, files in genre_files.items():
        print(f"{genre}: {len(files)} files")

if __name__ == "__main__":
    main()
