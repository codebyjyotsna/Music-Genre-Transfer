import torchaudio
from torchaudio.transforms import MelSpectrogram, InverseMelScale

def audio_to_spectrogram(audio_path):
    waveform, sample_rate = torchaudio.load(audio_path)
    mel_transform = MelSpectrogram(sample_rate)
    spectrogram = mel_transform(waveform)
    return spectrogram

def spectrogram_to_audio(spectrogram, output_path):
    inverse_transform = InverseMelScale(n_stft=spectrogram.size(-2))
    audio = inverse_transform(spectrogram)
    torchaudio.save(output_path, audio, sample_rate=22050)

# Example Usage
if __name__ == "__main__":
    spectrogram = audio_to_spectrogram("input_song.mp3")
    print("Spectrogram Shape:", spectrogram.shape)
    spectrogram_to_audio(spectrogram, "reconstructed_song.wav")
