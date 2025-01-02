# imports
import torch
import compute.computeBase
from compute.loging import printInfo


class neuralNetworkModel(torch.nn.Module):
    """
    Class for neural network model
    """
    def __init__(self, **kwargs):
        super(neuralNetworkModel, self).__init__()

        # default and overwrite
        inputDim = 4
        hiddenDim = 3
        outputDim = 1 # should stay at 1

        # Read from dict
        self.__dict__.update(kwargs)

        # Layer Sequence
        # self.torchSeq = torch.nn.Sequential()

        # Layer 1
        self.layer_1 = torch.nn.Linear(inputDim, hiddenDim)
        torch.nn.init.kaiming_uniform_(self.layer_1.weight, nonlinearity='relu')
        # self.torchSeq.add(self.layer_1)

        # Layer 2
        self.layer_2 = torch.nn.Linear(hiddenDim, outputDim)
        # self.torchSeq.add(self.layer_2)

    def forward(self, x):
        x = torch.nn.functional.relu(self.layer_1(x))
        x = torch.nn.functional.relu(self.layer_2(x))
        return x


class NeuralNetwork(compute.computeBase.computeBase):
    def __init__(self, **kwargs):
        super(NeuralNetwork, self).__init__()
        printInfo("Initializing NeuralNetwork")

        self.model = neuralNetworkModel()
        print(self.model)

        # Config parameters
        self.learningRate = 0.1
        self.numEpochs = 1000

        # Read from dict and update
        self.__dict__.update(kwargs)

        self.torchDevice = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
        # self.model.to(self.torchDevice)
        print(f"Using: {self.torchDevice}")


    def calculate(self, outputFolder):
        printInfo("Calculating NeuralNetwork")

        torchX = torch.tensor(self.dataSource.X_test.values, dtype=torch.float32)
        torchY = torch.tensor(self.dataSource.y_test.values, dtype=torch.int8)

        lossFunc = torch.nn.BCELoss()
        optimizer = torch.optim.Adam(self.model.parameters(), lr=0.001)

        for epoch in range(self.numEpochs):
            for torchX, torchY in zip(torchX, torchY):
                optimizer.zero_grad()

                pred = self.model(torchX)
                loss = lossFunc(pred, torchY)
                loss.backward()
                optimizer.step()

        printInfo("Training Finished!")




    def test(self):
        print("Testing...")