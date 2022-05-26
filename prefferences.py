import torch
from torchaudio.transforms import MelSpectrogram, Resample, MFCC


def most_performant_device():
    if torch.cuda.is_available():
        print("GPU available")
        return "cuda"
    else:
        print("GPU is not available, using CPU instead")
        return "cpu"


PROCESSING_DEVICE = most_performant_device()


def force_processing_device_to(device: str):
    global PROCESSING_DEVICE
    PROCESSING_DEVICE = device


# SAMPLE_RATE: int = 44100
# N_FFT: int = 1024
# HOP_LENGTH: int = N_FFT // 2
# N_MELS: int = 64
# N_MFCC: int = 64
SAMPLE_RATE: int = 44100
N_FFT: int = 1024
HOP_LENGTH: int = N_FFT // 2
N_MELS: int = 256
N_MFCC: int = 256


def mel_spec_transform() -> MelSpectrogram:
    return MelSpectrogram(
        sample_rate=SAMPLE_RATE,
        n_fft=N_FFT,
        hop_length=HOP_LENGTH,
        n_mels=N_MELS,
    ).to(PROCESSING_DEVICE)


def mfcc_spec_transform() -> MFCC:
    return MFCC(
        sample_rate=SAMPLE_RATE,
        n_mfcc=N_MFCC,
        melkwargs={
          'n_fft': N_FFT,
          'n_mels': N_MELS,
          'hop_length': HOP_LENGTH,
          'mel_scale': 'htk',
        }
    ).to(PROCESSING_DEVICE)


# duration in seconds
MAX_DURATION: float = 0.7
MAX_SAMPLE_COUNT: int = int(MAX_DURATION * SAMPLE_RATE)


def resample_if_applicable(samples, sample_rate):
    if sample_rate != SAMPLE_RATE:
        resample = Resample(
            sample_rate,
            SAMPLE_RATE,
        ).to(PROCESSING_DEVICE)
        samples = resample(samples)
        return resample(samples), SAMPLE_RATE
    return samples, sample_rate


def mono_if_stereo(samples):
    if samples.shape[0] == 1:
        return samples
    return torch.mean(samples, dim=0, keepdim=True)


def adjust_to_duration(samples):
    signal_len = samples.shape[1]
    # Cut if necessary
    if signal_len > MAX_SAMPLE_COUNT:
        return samples[:, :MAX_SAMPLE_COUNT]
    if signal_len < MAX_SAMPLE_COUNT:
        extra_samples = MAX_SAMPLE_COUNT - signal_len
        return torch.nn.functional.pad(samples, (0, extra_samples))
    return samples


def uniform_transformation(samples, sample_rate):
    r_samples, r_sr = resample_if_applicable(samples, sample_rate)
    m_samples = mono_if_stereo(r_samples)
    u_samples = adjust_to_duration(m_samples)
    return u_samples, r_sr
