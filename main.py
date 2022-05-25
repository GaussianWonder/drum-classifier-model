import librosa
import torch
import torchaudio
from torch import nn

import matplotlib.pyplot as plt

import cli
import prefferences
from files import get_test_files, SoundFile, CATEGORIES
from models import init_sqlite

from dataset import AudioAssets
from network.convolutional import CNNetwork
from network.train import create_data_loader, BATCH_SIZE, train, LEARNING_RATE, EPOCHS

opts = cli.get_args()

print('using torch: ' + torch.__version__)
print('using torchaudio: ' + torchaudio.__version__)


def plot_spectrogram(spec, title=None, ylabel='freq_bin', aspect='auto', xmax=None):
    fig, axs = plt.subplots(1, 1)
    axs.set_title(title or 'Spectrogram (db)')
    axs.set_ylabel(ylabel)
    axs.set_xlabel('frame')
    im = axs.imshow(librosa.power_to_db(spec), origin='lower', aspect=aspect)
    if xmax:
        axs.set_xlim((0, xmax))
    fig.colorbar(im, ax=axs)
    plt.show(block=False)


def predict(model, input_data, target, class_mapping):
    model.eval()
    with torch.no_grad():
        predictions = model(input_data)
        # Tensor (1, CATEGORIES) -> [ [0.1, 0.01, ..., 0.6] ]
        predicted_index = predictions[0].argmax(0)
        predicted = class_mapping[predicted_index]
        expected = class_mapping[target]
    return predicted, expected


if __name__ == '__main__':
    executed_from_cli: bool = False

    init_sqlite()

    if cli.should_reset(opts):
        # Delete everything and Rescan
        executed_from_cli = True

    if cli.should_rescan(opts):
        # Rescan
        executed_from_cli = True

    if cli.should_train(opts):
        executed_from_cli = True

        audioDataset = AudioAssets("./assets")

        cnn = CNNetwork().to(prefferences.PROCESSING_DEVICE)
        print(cnn)

        # Train model
        train(
            model=cnn,
            data_loader=create_data_loader(audioDataset, BATCH_SIZE),
            loss_function=nn.CrossEntropyLoss(),
            optimizer=torch.optim.Adam(
                cnn.parameters(),
                lr=LEARNING_RATE,
            ),
            device=prefferences.PROCESSING_DEVICE,
            epochs=EPOCHS
        )

        # Save Model
        export_path = cli.model_export_path(opts)
        torch.save(cnn.state_dict(), export_path)
        print(f"Model saved at {export_path}")

    if not executed_from_cli:
        audioDataset = AudioAssets("./test_assets")
        cnn = CNNetwork().to(prefferences.PROCESSING_DEVICE)
        cnn.load_state_dict(torch.load("classifier.pth"))

        for input_data, target in audioDataset:
            input_data.unsqueeze_(0)

            predicted, expected = predict(cnn, input_data, target, CATEGORIES)

            print(f"Predicted {predicted}, expected: {expected}")
