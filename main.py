import random

import torch
import torchaudio
from torch import nn

import cli
import prefferences
import utils.plotting
from files import SoundFile, CATEGORIES, get_files_per_category
from models import init_sqlite

from dataset import AudioAssets
from network.convolutional import CNNetwork
from network.test import test
from network.train import create_data_loader, BATCH_SIZE, train, LEARNING_RATE, EPOCHS

print('using torch: ' + torch.__version__)
print('using torchaudio: ' + torchaudio.__version__)


if __name__ == '__main__':
    init_sqlite()

    executed_from_cli: bool = False

    if cli.should_reset():
        # Delete everything and Rescan
        executed_from_cli = True

    if cli.should_rescan():
        # Rescan
        executed_from_cli = True

    if cli.should_train():
        executed_from_cli = True

        audio_dataset = AudioAssets("./assets")

        cnn = CNNetwork().to(prefferences.PROCESSING_DEVICE)
        print(cnn)

        # Train the Model
        train(
            model=cnn,
            data_loader=create_data_loader(audio_dataset, BATCH_SIZE),
            loss_function=nn.CrossEntropyLoss(),
            optimizer=torch.optim.Adam(
                cnn.parameters(),
                lr=LEARNING_RATE,
            ),
            device=prefferences.PROCESSING_DEVICE,
            epochs=EPOCHS
        )

        # Save Model
        export_path = cli.model_export_path()
        torch.save(cnn.state_dict(), export_path)
        print(f"Model saved at {export_path}")

    if cli.should_test():
        executed_from_cli = True

        audio_dataset = AudioAssets(cli.validation_path())

        cnn = CNNetwork().to(prefferences.PROCESSING_DEVICE)
        cnn.load_state_dict(torch.load(cli.model_import_path()))

        test(cnn, audio_dataset, CATEGORIES)

    if not executed_from_cli:
        prefferences.force_processing_device_to("cpu")

        # Do random plotting from each category
        for category, files in get_files_per_category():
            rand_index = random.randint(0, len(files) - 1)
            with SoundFile.from_file(files[rand_index]) as sound:
                plot_name = f"{sound.name} {category} - {sound.path}"

                # utils.plotting.plot_waveform(
                #     waveform=sound.samples,
                #     sample_rate=sound.sample_rate,
                #     title=f"{plot_name} Waveform",
                # )

                utils.plotting.plot_spectrogram(
                    sound.mel_spectrogram()[0],
                    title=f"{plot_name} mel spectrogram",
                    ylabel="mel_freq",
                )

                utils.plotting.plot_spectrogram(
                    sound.mfcc_spectrogram()[0],
                    title=f"{plot_name} mfcc spectrogram",
                    ylabel="freq_bin"
                )
