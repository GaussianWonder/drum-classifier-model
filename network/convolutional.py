from torch import nn

import prefferences
from files import CATEGORIES


def convolutional_block_builder(
        in_channels=1, out_channels=16, conv_kernel=3, conv_stride=1, conv_padding=2,
        m_pool_kernel=2,
) -> nn.Sequential:
    return nn.Sequential(
        nn.Conv2d(
            in_channels=in_channels,
            out_channels=out_channels,
            kernel_size=conv_kernel,
            stride=conv_stride,
            padding=conv_padding,
        ),
        nn.ReLU(),
        nn.MaxPool2d(
            kernel_size=m_pool_kernel,
        ),
    ).to(prefferences.PROCESSING_DEVICE)


class CNNetwork(nn.Module):
    conv1: nn.Sequential
    conv2: nn.Sequential
    conv3: nn.Sequential
    conv4: nn.Sequential

    flatten: nn.Flatten
    linear: nn.Linear
    softmax: nn.Softmax

    def __init__(self):
        super().__init__()

        # First convolutional block in:1 out:16
        self.conv1 = convolutional_block_builder(
            in_channels=1,
            out_channels=16,
        )
        self.conv2 = convolutional_block_builder(
            in_channels=16,
            out_channels=32,
        )
        self.conv3 = convolutional_block_builder(
            in_channels=32,
            out_channels=64,
        )
        self.conv4 = convolutional_block_builder(
            in_channels=64,
            out_channels=128,
        )

        self.flatten = nn.Flatten().to(prefferences.PROCESSING_DEVICE)

        self.linear = nn.Linear(
            # TODO 5 * 4 ? frequency/time resolution ? experiment!
            128 * 5 * 5,
            # TODO put this in the constructor
            len(CATEGORIES)
        ).to(prefferences.PROCESSING_DEVICE)

        self.softmax = nn.Softmax(dim=1).to(prefferences.PROCESSING_DEVICE)

    def forward(self, input_data):
        # Convolution blocks
        x = self.conv1(input_data)
        x = self.conv2(x)
        x = self.conv3(x)
        x = self.conv4(x)

        # Flatten
        x = self.flatten(x)

        logits = self.linear(x)
        predictions = self.softmax(logits)
        return predictions
