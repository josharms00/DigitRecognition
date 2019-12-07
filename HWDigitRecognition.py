from nn import NeuralNetwork
import numpy as np
import matplotlib.pyplot as plt
import pickle

# initialize labels
l = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

# initialize network topology
digit = NeuralNetwork(784, [12, 12], 10, l)

def train():

    # initialize target array
    targets = np.asarray([
               [[1],  [0], [0], [0], [0], [0], [0], [0], [0], [0]], 
               [[0],  [1], [0], [0], [0], [0], [0], [0], [0], [0]],
               [[0],  [0], [1], [0], [0], [0], [0], [0], [0], [0]],
               [[0],  [0], [0], [1], [0], [0], [0], [0], [0], [0]],
               [[0],  [0], [0], [0], [1], [0], [0], [0], [0], [0]],
               [[0],  [0], [0], [0], [0], [1], [0], [0], [0], [0]],
               [[0],  [0], [0], [0], [0], [0], [1], [0], [0], [0]],
               [[0],  [0], [0], [0], [0], [0], [0], [1], [0], [0]],
               [[0],  [0], [0], [0], [0], [0], [0], [0], [1], [0]],
               [[0],  [0], [0], [0], [0], [0], [0], [0], [0], [1]] ])

    # iterate through all test batches
    for x in range(0, 999):
        with open("pickled/pickled_mnist" + str(x) + ".plk", "br") as fh:
            data = pickle.load(fh)
            train_imgs = data[0]
            train_labels = data[1]

            # iterate through all training cases
            for i in  range(0, len(train_imgs)):
                digit.train(train_imgs[i].reshape(784, 1), targets[int(train_labels[i][0])])
            train_imgs = []
            train_labels = []

    digit.store_weights_and_biases()

# function to test network with test dataset
def test():
    # load weights and biases from previous training
    digit.load_weights_and_biases()

    inp = ''
    while (1):
        # choose batch number to test from 
        inp = input("Choose a number from 0 - 165: ")

        # stop testing when user requests
        if inp == 'exit':
            break
        
        # open pickled test batch
        with open("pickled/pickled_mnist" + str(inp) + ".plk", "br") as fh:
                data = pickle.load(fh)
                test_imgs = data[0]

                # choose specific test case
                inp2 = int(input("Now choose a number from 0 - 60: "))

                # let the network guess
                print('Guess is: ', digit.guess(test_imgs[inp2].reshape(784, 1)))

                # display test digit
                img = test_imgs[inp2].reshape((28,28))
                plt.imshow(img, cmap="Greys")
                plt.show()

def calculate_accuracy(itr):
    # load weights and biases into matrix
    digit.load_weights_and_biases()

    # initialize variables
    correct = 0
    total = 0

    # iterate as many times as requested
    for i in range(0, itr):
        # pick a random test batch
        r = np.random.randint(0, 165)
        with open("pickled/pickled_mnist" + str(r) + ".plk", "br") as fh:
                    data = pickle.load(fh)
                    test_imgs = data[0]
                    test_labels = data[1]
                    
                    # pick a random test case
                    rand = np.random.randint(0, 59)

                    # let the network guess
                    g = digit.guess(test_imgs[rand].reshape(784, 1))
                    
                    # if the guess matches the label increment the correct
                    if g == int(test_labels[rand]):
                        correct += 1
                    
                    total += 1

    acc = correct / total

    print('Accuracy of network = ', np.round(acc*100, 2), '%')



# take csv file and pickle into multiple batches
def pickle_csv():
    train = [] 
    test = []
    row = 0
    last = 0
    batch = 0
    for line in open("mnist_test.csv"):
        test.append(np.fromstring(line, sep=","))
        if row == (60 + last):
            last = row
            fac = 0.99 / 255
            train_imgs = np.asfarray(train) 
            train_labels = np.asfarray(train)

            test_imgs = np.asfarray(test)
            test_labels = np.asfarray(test)

            test_imgs = test_imgs[: , 1:] * fac + 0.01
            test_labels = test_labels[: , :1]
            with open("pickled_test/pickled_mnist" + str(batch) + ".plk", "bw") as fh:
                data = (test_imgs, test_labels)
                pickle.dump(data, fh)
            batch += 1
            test = []
        row += 1



def main():
    #test()
    train()
    #calculate_accuracy(2000)
    #pickle_csv()

if __name__ == '__main__':
    main()