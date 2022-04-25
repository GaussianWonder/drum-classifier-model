import glob
from typing import AnyStr

from files.file import File
from files.sound_file import SoundFile

CATEGORIES = [
    'kick',
    'snare',
    'crash',
    'hihat',
]


def category_patterns(category: str):
    return (
        './assets/{category}/**/*.wav'.format(category=category),
        './assets/{category}/**/*.WAV'.format(category=category),
        './assets/{category}/**/*.mp3'.format(category=category),
        './assets/{category}/**/*.MP3'.format(category=category),
        './assets/{category}/**/*.ogg'.format(category=category),
    )


def patterns_to_paths(patterns):
    return [
        path
        for pattern in patterns
        for path in glob.glob(pattern, recursive=True)
    ]


def get_patterns():
    return [
        (category, category_patterns(category))
        for category in CATEGORIES
    ]


def get_paths() -> list[tuple[str, list[str | bytes]]]:
    return [
        (category, patterns_to_paths(patterns))
        for (category, patterns) in get_patterns()
    ]


def get_files_per_category():
    return [
        (category, [File(p) for p in paths])
        for (category, paths) in get_paths()
    ]


def get_files():
    return [
        (category, fl)
        for (category, files) in get_files_per_category()
        for fl in files
    ]


ALL_AUDIO_PATTERN = category_patterns('.')
