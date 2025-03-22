# imports
import torch
import compute.computeBase
import matplotlib.pyplot as plt
from compute.helper.loging import printInfo


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
        super().__init__()
        self.l1 = torch.nn.Linear(4, 64)  # Input layer to 64 neurons
        self.act1 = torch.nn.ReLU()       # ReLU activation function
        self.l2 = torch.nn.Linear(64, 16) # 64 neurons to 16 neurons
        self.drop = torch.nn.Dropout(0.2) # Dropout for regularization
        self.act2 = torch.nn.ReLU()       # Another ReLU
        self.l3 = torch.nn.Linear(16, 3)  # Output layer to 3 neurons (classes)


    def forward(self, x):
        x = self.l1(x)
        x = self.act1(x)
        x = self.l2(x)
        x = self.drop(x)
        x = self.act2(x)
        x = self.l3(x)
        return x


class NeuralNetwork(compute.computeBase.computeBase):
    def __init__(self, **kwargs):
        super(NeuralNetwork, self).__init__()
        printInfo("Initializing NeuralNetwork")

        self.model = neuralNetworkModel()
        print(self.model)

        # Config parameters
        self.learningRate = 0.002
        self.numEpochs = 400

        # Read from dict and update
        self.__dict__.update(kwargs)

        self.torchDevice = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
        # self.model.to(self.torchDevice)
        print(f"Using: {self.torchDevice}")


    def calculate(self, outputFolder):
        printInfo("Calculating NeuralNetwork")

        # self.model = neuralNetworkModel()

        self.torchTrX = torch.tensor(self.dataSource.x_train.values, dtype=torch.float32)
        self.torchTrY = torch.tensor(self.dataSource.y_train.values, dtype=torch.long)

        # Move to GPU or CPU
        self.model.to(self.torchDevice)
        self.torchTrX = self.torchTrX.to(self.torchDevice)
        self.torchTrY = self.torchTrY.to(self.torchDevice)


        loss_arr = []
        loss_fn = torch.nn.CrossEntropyLoss()
        optimizer = torch.optim.Adam(self.model.parameters(), lr=self.learningRate)

        for epoch in range(self.numEpochs):
            ypred = self.model(self.torchTrX)
            loss = loss_fn(ypred, self.torchTrY)
            loss_arr.append(loss.item())
            loss.backward()
            optimizer.step()
            optimizer.zero_grad()

        printInfo("Training Finished!")

        plt.plot(loss_arr)
        plt.show()


        printInfo("Training Finished!")





    def test(self):
        printInfo("Testing NeuralNetwork")

        self.torchTestX = torch.tensor(self.dataSource.x_test.values, dtype=torch.float32)
        self.torchTestX.to(self.torchDevice)

        self.torchPredY = self.model(self.torchTestX)

        testY = torch.argmax(self.torchPredY, dim=1)

        #