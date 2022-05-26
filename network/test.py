import torch


def predict(model, input_data, target, class_mapping):
    model.eval()
    with torch.no_grad():
        predictions = model(input_data)
        # Tensor (1, CATEGORIES) -> [ [0.1, 0.01, ..., 0.6] ]
        predicted_index = predictions[0].argmax(0)
        predicted = class_mapping[predicted_index]
        expected = class_mapping[target]
    return predicted, expected


def test(model, dataset, class_mapping):
    for input_data, target_data in dataset:
        input_data.unsqueeze_(0)

        predicted, expected = predict(model, input_data, target_data, class_mapping)

        print(f"Predicted {predicted}, expected: {expected}")
