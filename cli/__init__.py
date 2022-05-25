import argparse

cli_parser = argparse.ArgumentParser(
    description="CLI options for VisualizeSound",
)

cli_parser.add_argument(
    '--rescan-assets',
    action='store_true',
    required=False,
    default=False,
    dest='rescan_assets',
    help="rescan assets and process new files",
)

cli_parser.add_argument(
    '--reprocess-assets',
    action='store_true',
    required=False,
    default=False,
    dest='reprocess_assets',
    help="delete cache and rescan, thus reprocessing all assets"
)


def get_args():
    return cli_parser.parse_args()

