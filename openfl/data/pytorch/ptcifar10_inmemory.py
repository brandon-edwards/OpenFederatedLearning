# Copyright (C) 2020 Intel Corporation
# Licensed subject to the terms of the separately executed evaluation license agreement between Intel Corporation and you.

import numpy as np
# FIXME: we should remove the keras dependency since it is only really for file downloading
#import tensorflow.keras as keras

from openfl.data.pytorch.ptfldata_inmemory import PyTorchFLDataInMemory
import torchvision

def _load_raw_datashards(shard_num, nb_collaborators):
    """Load the raw CIFAR10 dataset from the web
  
    origin_link = 'https://www.cs.toronto.edu/~kriz/cifar-10-python.tar.gz' 
    hash_value = 'c58f30108f718f92721af3b95e74349a' 
    path = get_file('cifar10.tar.gz', origin=origin_link, file_hash=hash_value)
  
    Args:
        shard_num (int): The index of the dataset shard
        nb_collaborators (int): The number of collaborators in the federation
  
    Returns:
        Two tuples (images, labels) for the training and validation datasets for this shard 
  
    """ 
    train_obj = torchvision.datasets.CIFAR10('~/.CIFAR10', train=True, download=True)  
    test_obj = torchvision.datasets.CIFAR10('~/.CIFAR10', train=False, download=True)  
    x_train = train_obj.data
    y_train = np.asarray(train_obj.targets)
    x_test = test_obj.data
    y_test = np.asarray(test_obj.targets)
    # fix the label dimension to be (N,)
    y_train = y_train.reshape(-1)
    y_test = y_test.reshape(-1) 
  
    # create the shards
    X_train_shards = x_train[shard_num::nb_collaborators]
    y_train_shards = y_train[shard_num::nb_collaborators]
  
    X_test_shards = x_test[shard_num::nb_collaborators]
    y_test_shards  = y_test[shard_num::nb_collaborators]
    return (X_train_shards, y_train_shards), (X_test_shards, y_test_shards)

def load_cifar10_shard(shard_num, nb_collaborators, categorical=True, channels_last=False, **kwargs):
    """Load the CIFAR10 dataset.
  
    Args: 
        shard_num (int): The index of the dataset shard
        nb_collaborators (int): The number of collaborators in the federation
        categorical (bool): True = return the categorical labels as one-hot encoded (Default = True) 
        channels_last (bool): True = input images are channels first (Default = False) 
        **kwargs: Variable parameters to pass to function 
  
    Returns:     
        list: The input shape.  
        int: The number of classes    
        numpy.ndarray: The training data       
        numpy.ndarray: The training labels     
        numpy.ndarray: The validation data     
        numpy.ndarray: The validation labels   
    """ 
    img_rows, img_cols, img_channel = 32, 32, 3
    num_classes = 10   
  
    (X_train, y_train), (X_test, y_test) = _load_raw_datashards(shard_num, nb_collaborators)
  
    if channels_last:  
        X_train = X_train.reshape(X_train.shape[0], img_rows, img_cols, img_channel)        
        X_test = X_test.reshape(X_test.shape[0], img_rows, img_cols, img_channel)  
        input_shape = (img_rows, img_cols, img_channel)       
    else:        
        X_train = X_train.reshape(X_train.shape[0], img_channel, img_rows, img_cols)        
        X_test = X_test.reshape(X_test.shape[0], img_channel, img_rows, img_cols)  
        input_shape = (img_channel, img_rows, img_cols)       
  
    X_train = X_train.astype('float32')        
    X_test = X_test.astype('float32') 
    X_train /= 255     
    X_test /= 255
  
    if categorical:    
        def to_categorical(x, num_classes):
            """one-hot encodes an array"""
            return np.eye(num_classes, dtype='uint8')[x]
        # convert class vectors to binary class matrices      
        y_train = to_categorical(y_train, num_classes)  
        y_test = to_categorical(y_test, num_classes)    
  
    return input_shape, num_classes, X_train, y_train, X_test, y_test  

class PyTorchCIFAR10InMemory(PyTorchFLDataInMemory):
    """PyTorch data loader for CIFAR10 dataset
    """

    def __init__(self, data_path, batch_size, **kwargs):
        """Instantiate the data object

        Args:
   data_path: file path for the data
   batch_size (int): batch size for the data loader
   **kwargs: Additional parameters to pass to function
        """
        super().__init__(batch_size, **kwargs)

        _, num_classes, X_train, y_train, X_val, y_val = load_cifar10_shard(shard_num=data_path, **kwargs)

        self.training_data_size = len(X_train)
        self.validation_data_size = len(X_val)
        self.num_classes = num_classes
        self.train_loader = self.create_loader(X=X_train, y=y_train, shuffle=True)
        self.val_loader = self.create_loader(X=X_val, y=y_val, shuffle=False)
