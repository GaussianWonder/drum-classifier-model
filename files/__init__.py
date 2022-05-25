import glob
import os

from files.file import File
from files.sound_file import SoundFile


# Asset Categories are equivalent to MSL in SoundFileModels
def get_asset_categories(asset_path: str) -> list[str]:
    categories = []
    for f_name in os.listdir(asset_path):
        maybeDir = os.path.join(asset_path, f_name)
        if os.path.isdir(maybeDir):
            categories.append(f_name)
    return categories
# CATEGORIES = [
#     'kick',
#     'snare',
#     'crash',
#     'hihat',
# ]


CATEGORIES = get_asset_categories('./assets')
TEST_CATEGORIES = get_asset_categories('./test_assets')

if not CATEGORIES.sort() == TEST_CATEGORIES.sort():
    print("Categories in asset and test folder are not identical!")


def category_patterns(category: str, asset_path: str = './assets'):
    return (
        '{assets}/{category}/**/*.wav'.format(category=category, assets=asset_path),
        '{assets}/{category}/**/*.WAV'.format(category=category, assets=asset_path),
        '{assets}/{category}/**/*.mp3'.format(category=category, assets=asset_path),
        '{assets}/{category}/**/*.MP3'.format(category=category, assets=asset_path),
        '{assets}/{category}/**/*.ogg'.format(category=category, assets=asset_path),
    )


def patterns_to_paths(patterns):
    return [
        path
        for pattern in patterns
        for path in glob.glob(pattern, recursive=True)
    ]


def get_patterns(asset_path: str = './assets'):
    return [
        (category, category_patterns(category, asset_path))
        for category in CATEGORIES
    ]


def get_paths(asset_path: str = './assets') -> list[tuple[str, list[str | bytes]]]:
    return [
        (category, patterns_to_paths(patterns))
        for (category, patterns) in get_patterns(asset_path)
    ]


def get_files_per_category(asset_path: str = './assets'):
    return [
        (category, [File(p) for p in paths])
        for (category, paths) in get_paths(asset_path)
    ]


def get_files(asset_path: str = './assets'):
    return [
        (category, fl)
        for (category, files) in get_files_per_category(asset_path)
        for fl in files
    ]


def get_test_files():
    return get_files('./test_assets')


ALL_AUDIO_PATTERN = category_patterns('.')

# # 99
# print(len(get_test_files()))
# # 973
# print(len(get_files()))

# def rename_until_valid(file_name: str) -> str:
#     is_valid: bool = False
#     os.path.isfile(file_name)
#     os.path.dirname(file_name)
#     new_file: str = file_name
#     while not is_valid:
#         if not os.path.exists(file_name):
#             is_valid = True
