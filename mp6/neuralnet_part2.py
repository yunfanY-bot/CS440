# neuralnet.py
# ---------------
# Licensing Information:  You are free to use or extend this projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to the University of Illinois at Urbana-Champaign
#
# Created by Justin Lizama (jlizama2@illinois.edu) on 10/29/2019
# Modified by Mahir Morshed for the spring 2021 semester
# Modified by Joao Marques (jmc12) for the fall 2021 semester 

"""
This is the main entry point for MP3. You should only modify code
within this file and neuralnet_part1.py,neuralnet_leaderboard -- the unrevised staff files will be used for all other
files and classes when code is run, so be careful to not modify anything else.
"""

import numpy as np

import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from utils import get_dataset_from_arrays
from torch.utils.data import DataLoader


class NeuralNet(nn.Module):
    def __init__(self, lrate, loss_fn, in_size, out_size):
        """
        Initializes the layers of your neural network.

        @param lrate: learning rate for the model
        @param loss_fn: A loss function defined as follows:
            @param yhat - an (N,out_size) Tensor
            @param y - an (N,) Tensor
            @return l(x,y) an () Tensor that is the mean loss
        @param in_size: input dimension
        @param out_size: output dimension
        """

        super(NeuralNet, self).__init__()
        self.loss_fn = loss_fn

        self.cnn = nn.Sequential(nn.Conv2d(3, 35, kernel_size=3), nn.LeakyReLU(), nn.MaxPool2d(2, 2))
        self.cnn1 = nn.Sequential(nn.Conv2d(35, 30, kernel_size=3), nn.LeakyReLU(), nn.MaxPool2d(2))
        self.fc1 = nn.Sequential(nn.Linear(1080, 108), nn.LeakyReLU())
        self.fc2 = nn.Sequential(nn.Linear(108, 108), nn.LeakyReLU())
        self.fc3 = nn.Linear(108, out_size)

        self.lrate = lrate
        self.optims = optim.Adagrad(self.parameters(), lr=self.lrate, weight_decay=0.0018)

    def forward(self, x):
        """Performs a forward pass through your neural net (evaluates f(x)).

        @param x: an (N, in_size) Tensor
        @return y: an (N, out_size) Tensor of output from the network
        """

        x = x.view(-1, 3, 32, 32)
        x = self.cnn(x)
        x = self.cnn1(x)
        x = torch.flatten(x, 1)  # flatten all dimensions except the batch dimension
        x = self.fc1(x)
        x = self.fc2(x)
        x = self.fc3(x)
        return x

    def step(self, x, y):
        """
        Performs one gradient step through a batch of data x with labels y.

        @param x: an (N, in_size) Tensor
        @param y: an (N,) Tensor
        @return L: total empirical risk (mean of losses) for this batch as a float (scalar)

        This code was taken from example from tutorial
        """

        self.optims.zero_grad()
        lossFunction = self.loss_fn(self.forward(x), y)
        lossFunction.backward()
        self.optims.step()
        return lossFunction.item()


def fit(train_set, train_labels, dev_set, epochs, batch_size=100):
    """ Make NeuralNet object 'net' and use net.step() to train a neural net
    and net(x) to evaluate the neural net.

    @param train_set: an (N, in_size) Tensor
    @param train_labels: an (N,) Tensor
    @param dev_set: an (M,) Tensor
    @param epochs: an int, the number of epochs of training
    @param batch_size: size of each batch to train on. (default 100)

    This method _must_ work for arbitrary M and N.

    The model's performance could be sensitive to the choice of learning rate.
    We recommend trying different values in case your first choice does not seem to work well.

    @return losses: list of total loss at the beginning and after each epoch.
            Ensure that len(losses) == epochs.
    @return yhats: an (M,) NumPy array of binary labels for dev_set
    @return net: a NeuralNet object
    """

    train_mean = train_set.mean()
    train_std = train_set.std()
    train = (train_set - train_mean) / train_std

    dev_mean = dev_set.mean()
    dev_std = dev_set.std()
    dev = (dev_set - dev_mean) / dev_std

    loss_fn = nn.CrossEntropyLoss()
    lrate = 0.00425
    net = NeuralNet(lrate, loss_fn, len(train_set[0]), 4)
    losses = []
    batch_n = len(train_set) // batch_size

    count = 0
    for j in range(epochs):
        for i in range(batch_n):
            labels = train_labels[i * batch_size:(i + 1) * batch_size]
            trains = train[i * batch_size:(i + 1) * batch_size]
            steps = net.step(trains, labels)
            losses.append(steps)

    network = net.forward(dev).detach().numpy()
    yhats = np.argmax(network, axis=1)
    return losses, yhats, net