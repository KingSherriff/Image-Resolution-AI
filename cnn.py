import tensorflow as tf
import numpy as np
import functools
import operator

def model():
    mnist = tf.keras.datasets.fashion_mnist
    (training_images, training_labels), (test_images, test_labels) = mnist.load_data()
    training_images=training_images / 255.0
    test_images=test_images / 255.0
    model = tf.keras.models.Sequential([
      tf.keras.layers.Flatten(),
      tf.keras.layers.Dense(128, activation=tf.nn.relu),
      tf.keras.layers.Dense(10, activation=tf.nn.softmax)
    ])
    model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
    model.fit(training_images, training_labels, epochs=5)
    
    test_loss = model.evaluate(test_images, test_labels)
    return model

#def weights():
#    fullModel = model()
#    weightsList = []
#    for layer in fullModel.layers:
#        #print(layer.weights)
#        weightsList.append(layer.weights)
#    return weightsList

def weights():
    fullModel = model()
    return fullModel.get_weights()

def organizeWeights():
    result = np.concatenate([x.ravel() for x in weights()])
    return result

#def organizeWeights():
#    weightsList = weights()
#    result = []
#    for item in weightsList:
#        for element in item:
#            result.append(element)
#    return result

#def newOrganizeWeights():
#    result = []
#    weightsList = weights()

def flattenList(inputList):
    result = np.concatenate([x.ravel() for x in inputList])
    return result

#def flattenList(inputList):
#    if len(inputList) == 0:
#        return inputList
#    if isinstance(inputList[0], np.ndarray) or isinstance(inputList[0], list):
#        return flattenList(inputList[0]) + flattenList(inputList[1:])
#    return inputList[:1] + flattenList(inputList[1:])

#def flattenList(inputList):
#    result = []
#    for element in inputList:
#        print(element)
#        print(type(element))
#        if isinstance(element, np.float32) or isinstance(element, np.float64):
#            print("float")
#            result.append(element)
#        elif isinstance(element, np.ndarray):
#            print("ndarray")
#            for item in flattenList(element):
#                result.append(item)
#    return result
