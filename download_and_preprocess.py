import os
import requests
import zipfile
import torchaudio
from torchaudio.transforms import MelSpectrogram
import matplotlib.pyplot as plt

# Directory for storing datasets
DATASET_DIR = "dataset/"
PROCESSED_DIR = "processed/"

# Example dataset URLs (GTZAN Genre Dataset)
DATASET_URLS = {
    "gtzan": "http://opihi.cs.uvic.ca/sound/genres.tar.gz",
    # Add more datasets here if needed
}

def download_dataset(dataset_name, url):
    """Download and extract a dataset."""
    dataset_path = os.path.join(DATASET_DIR, f"{dataset_name}.tar.gz")
    extract_path = os.path.join(DATASET_DIR, dataset_name)

    if not os.path.exists(dataset_path):
        print(f"Downloading {dataset_name} dataset...")
        response = requests.get(url, stream=True)
        with open(dataset_path, "wb") as file:
            for chunk in response.iter_content(chunk_size=1024):
                file.write(chunk)
        print(f"Downloaded {dataset_name} dataset.")

    if not os.path.exists(extract_path):
        print(f"Extracting {dataset_name} dataset...")
        with zipfile.ZipFile(dataset_path, "r") as zip_ref:
            zip_ref.extractall(DATASET_DIR)
        print(f"Extracted {dataset_name} dataset.")

def preprocess_audio_to_spectrogram(audio_path, output_dir):
    """Convert audio file to spectrogram and save as an image."""
    waveform, sample_rate = torchaudio.load(audio_path)
    mel_transform = MelSpectrogram(sample_rate=sample_rate)
    spectrogram = mel_transform(waveform)

    # Save the spectrogram as an image
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, os.path.basename(audio_path).replace(".wav", ".png"))
    plt.figure(figsize=(10, 4))
    plt.imshow(spectrogram.log2()[0, :, :].detach().numpy(), cmap="viridis")
    plt.title("Mel Spectrogram")
    plt.colorbar(format="%+2.0f dB")
    plt.savefig(output_file)
    plt.close()
    print(f"Saved spectrogram: {output_file}")

def process_dataset(dataset_name):
    """Download and preprocess a dataset."""
    if dataset_name not in DATASET_URLS:
        raise ValueError(f"No URL defined for dataset: {dataset_name}")

    # Download the dataset
    download_dataset(dataset_name, DATASET_URLS[dataset_name])

    # Preprocess audio files
    dataset_path = os.path.join(DATASET_DIR, dataset_name)
    genres = [d for d in os.listdir(dataset_path) if os.path.isdir(os.path.join(dataset_path, d))]

    for genre in genres:
        genre_path = os.path.join(dataset_path, genre)
        output_dir = os.path.join(PROCESSED_DIR, genre)

        for audio_file in os.listdir(genre_path):
            if audio_file.endswith(".wav"):
                audio_path = os.path.join(genre_path, audio_file)
                preprocess_audio_to_spectrogram(audio_path, output_dir)

if __name__ == "__main__":
    # Example: Process the GTZAN dataset
    process_dataset("gtzan")
