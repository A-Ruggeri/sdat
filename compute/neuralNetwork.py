# imports
import torch
from compute.loging import printInfo

class neuralNetworkModel(torch.nn.Module):
    def __init__(self, **kwargs):
        super(NeuralNetwork, self).__init__()

        # default and overwrite
        input_dim = 1
        hidden_dim = 1
        output_dim = 1

        # Read from dict
        self.__dict__.update(kwargs)

        # Layer 1
        self.layer_1 = torch.nn.Linear(input_dim, hidden_dim)
        torch.nn.init.kaiming_uniform_(self.layer_1.weight, nonlinearity='relu')

        # Layer 2
        self.layer_2 = torch.nn.Linear(hidden_dim, output_dim)

    def forward(self, x):
        x = torch.nn.functional.relu(self.layer_1(x))
        x = torch.nn.functional.relu(self.layer_2(x))


class NeuralNetwork:
    def __init__(self, **kwargs):
        print("Initializing NeuralNetwork...")

        self.model = neuralNetworkModel()
        print(self.model)

        self.learningRate = 0.1
        self.numEpochs = 1000

        # Read from dict
        self.__dict__.update(kwargs)

        self.torchDevice = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
        printInfo(f"Using: {self.torchDevice}")


    def calculate(self):
        printInfo("Calculating NeuralNetwork:")

        torchX = torch.tensor(self.X_train, dtype=torch.float32)
        torchY = torch.tensor(self.Y_train, dtype=torch.int8).reshape(-1,1)

        optimizer = torch.optim.Adam(self.model.parameters(), lr=0.001)

        for epoch in range(self.numEpochs):
            for torchX, torchY in zip(torchX, torchY):
                optimizer.zero_grad()
                pred = self.model(torchX)
                loss = torch.nn.BCELoss(pred, torchY.unsqueeze(-1))
                loss_values.append(loss.item())
                loss.backward()
                optimizer.step()

        printInfo("Training Finished!")




    def test(self):
        print("Testing...")