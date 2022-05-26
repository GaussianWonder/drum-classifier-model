from torch.utils.data import DataLoader

BATCH_SIZE = 32
EPOCHS = 100
LEARNING_RATE = 0.001


def create_data_loader(train_data, batch_size):
    train_loader = DataLoader(train_data, batch_size=batch_size)
    return train_loader


def train_single_epoch(model, data_loader, loss_function, optimizer, device):
    loss = None

    for input_data, target_data in data_loader:
        input_data = input_data.to(device)
        target_data = target_data.to(device)

        # calculate loss
        prediction = model(input_data)
        loss = loss_function(prediction, target_data)

        # back propagate error and update weights
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

    print(f"loss: {loss.item()}")


def train(model, data_loader, loss_function, optimizer, device, epochs):
    for i in range(epochs):
        print(f"Epoch {i+1}")
        train_single_epoch(model, data_loader, loss_function, optimizer, device)
        print("---------------------------")
    print("Finished training")

