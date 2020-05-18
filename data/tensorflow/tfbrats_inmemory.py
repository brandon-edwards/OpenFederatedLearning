# Copyright (C) 2020 Intel Corporation
# Licensed subject to the terms of the separately executed evaluation license agreement between Intel Corporation and you.

from data.tensorflow.tffldata_inmemory import TensorFlowFLDataInMemory





class TensorFlowBratsInMemory(TensorFlowFLDataInMemory):

    def __init__(self, data_path, batch_size, percent_train=0.8, pre_split_shuffle=True, **kwargs):
        raise NotImplementedError("Medical data loading and processing code not implemented")
        super().__init__(batch_size)
        
        # X_train, y_train, X_val, y_val = 
        self.X_train = X_train
        self.y_train = y_train
        self.X_val = X_val
        self.y_val = y_val
