import glob

from files.file import File

AUDIO_PATTERNS = (
    './assets/**/*.wav',
    './assets/**/*.WAV',
    './assets/**/*.mp3',
    './assets/**/*.ogg',
)

KICK_PATTERN = './assets/kick/**/*.wav'
SNARE_PATTERN = './assets/snare/**/*.wav'
CRASH_PATTERN = './assets/crash/**/*.wav'
HIHAT_PATTERN = './assets/hihat/**/*.wav'

AUDIO_PATHS = []

for pattern in AUDIO_PATTERNS:
    AUDIO_PATHS.extend(glob.glob(pattern, recursive=True))

KICKS = glob.glob(KICK_PATTERN, recursive=True)
SNARES = glob.glob(SNARE_PATTERN, recursive=True)
CRASHES = glob.glob(CRASH_PATTERN, recursive=True)
HIHATS = glob.glob(HIHAT_PATTERN, recursive=True)

FILES = {
    "kicks": [File(p) for p in KICKS],
    "snares": [File(p) for p in SNARES],
    "crashes": [File(p) for p in CRASHES],
    "hihats": [File(p) for p in HIHATS],
    "all": [File(p) for p in AUDIO_PATHS],
}
