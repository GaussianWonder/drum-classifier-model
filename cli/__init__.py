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


cli_parser.add_argument(
    '--test',
    action='store',
    required=False,
    default='',
    dest='import_model',
    help="test a trained model which was previously exported at a given path",
)


cli_parser.add_argument(
    '--assets',
    action='store',
    required=False,
    default='./assets',
    dest='assets_path',
    help="the path to the assets folder to train the model",
)


cli_parser.add_argument(
    '--validation',
    action='store',
    required=False,
    default='./test_assets',
    dest='validation_assets_path',
    help="the path to the assets to test the trained model",
)


ARG_OPTS = cli_parser.parse_args()
print('Args:', ARG_OPTS)


def should_rescan() -> bool:
    return ARG_OPTS.rescan_assets


def should_reset() -> bool:
    return ARG_OPTS.reprocess_assets


def should_train() -> bool:
    return ARG_OPTS.export_model is not None and ARG_OPTS.export_model != ''


def should_test() -> bool:
    return ARG_OPTS.import_model is not None and ARG_OPTS.import_model != ''


def model_export_path() -> str | None:
    if should_train():
        return ARG_OPTS.export_model
    return None


def model_import_path() -> str | None:
    if should_test():
        return ARG_OPTS.import_model
    return None


def assets_path() -> str:
    return ARG_OPTS.assets_path


def validation_path() -> str:
    return ARG_OPTS.validation_assets_path


print('Validating', should_test())
print('Training', should_train())
