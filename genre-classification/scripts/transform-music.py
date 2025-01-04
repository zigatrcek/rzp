from pydub import AudioSegment
import os
from pathlib import Path
import glob

def trim_audio(input_path, output_path, duration=24000):  # duration in milliseconds
    # Load the audio file
    audio = AudioSegment.from_file(input_path)
    
    # Calculate the middle point and extract 24 seconds
    total_duration = len(audio)
    if total_duration <= duration:
        trimmed_audio = audio
    else:
        midpoint = total_duration // 2
        start_time = midpoint - (duration // 2)
        end_time = start_time + duration
        trimmed_audio = audio[start_time:end_time]
    
    # Create output directory if it doesn't exist
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Export the trimmed audio
    trimmed_audio.export(output_path, format=os.path.splitext(output_path)[1][1:])

def process_directory(input_dir):
    # Common audio file extensions
    audio_extensions = ('.mp3', '.wav', '.ogg', '.m4a', '.flac', '.aac')
    
    # Create output directory path by appending "-trimmed"
    input_path = Path(input_dir)
    output_path = input_path.parent / f"{input_path.name}-trimmed"
    
    # Find all audio files recursively
    for ext in audio_extensions:
        for audio_file in input_path.rglob(f'*{ext}'):
            # Calculate relative path to maintain directory structure
            relative_path = audio_file.relative_to(input_path)
            output_file = output_path / relative_path
            
            print(f"Processing: {audio_file}")
            try:
                trim_audio(str(audio_file), str(output_file))
                print(f"Created trimmed version: {output_file}")
            except Exception as e:
                print(f"Error processing {audio_file}: {str(e)}")

if __name__ == "__main__":
    input_directory = "/mnt/g/glasba/rzp/Beatport Trance TOP 100 Tracks August 2023"
    process_directory(input_directory)
