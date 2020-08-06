# Copyright (C) 2020 Intel Corporation
# Licensed subject to the terms of the separately executed evaluation license agreement between Intel Corporation and you.


class FLData(object):

    def __init__(self, data_path, **kwargs):
        """Instantiate the data object

        Args:
            data_path: The filepath to the dataset
            **kwargs: Additional parameters to pass to method

        Returns:
            None
        """
        pass

    def get_feature_shape(self):
        """Gets the shape of an example feature array

        Returns:
            tuple: shape of an example feature array
        """
        raise NotImplementedError

    def get_train_loader(self):
        """
        Get training data loader

        Returns:
            loader object (class defined by inheritor)
        """
        raise NotImplementedError

    def get_val_loader(self):
        """Get validation data loader

        Returns:
            loader object (class defined by inheritor)
        """
        raise NotImplementedError

    def get_inference_loader(self):
        """
        Get inferencing data loader 

        Returns
        -------
        loader object (class defined by inheritor)
        """
        return NotImplementedError

    def get_training_data_size(self):
        """Get total number of training samples

        Returns:
            int: number of training samples
        """
        raise NotImplementedError

    def get_validation_data_size(self):
        """Get total number of validation samples

        Returns:
            int: number of validation samples
        """
        raise NotImplementedError
