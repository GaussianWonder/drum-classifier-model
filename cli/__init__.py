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


cli_parser.add_argument(
    '--train',
    action='store',
    required=False,
    default='',
    dest='export_model',
    help="train the model and export it to the desired path",
)


def get_args():
    return cli_parser.parse_args()


def should_rescan(opts: argparse.Namespace) -> bool:
    return opts.rescan_assets


def should_reset(opts: argparse.Namespace) -> bool:
    return opts.reprocess_assets


def should_train(opts: argparse.Namespace) -> bool:
    return opts.export_model is not None and opts.export_model != ''


def model_export_path(opts: argparse.Namespace) -> str:
    return opts.export_model
