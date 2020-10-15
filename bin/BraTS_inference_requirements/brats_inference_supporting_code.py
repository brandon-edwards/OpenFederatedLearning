import numpy as np
import os
import sys

import SimpleITK as sitk

from torch.utils.data.dataset import Dataset
from torch.utils.data import DataLoader

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

from IPython.display import HTML



### MODEL CODE

# Model Class Mixin 
# Modification of openfl.models.flmodel at: https://github.com/IntelLabs/OpenFederatedLearning
# Note much has been removed in order to focus solely on demonstrating inference


"""
Mixin class for FL models. No default implementation.
Each framework will likely have its own baseclass implementation (e.g. TensorflowFLModelBase) that uses this mixin.
You may copy use this file or the appropriate framework-specific base-class to port your own models.
"""


class FLModel(object):
    """Federated Learning Model Base Class
    """

    def __init__(self, data,**kwargs):
        """Intializer
        Args:
            data: The data object
            **kwargs: Additional parameters to pass to the function
        """

        self.data = data



    def load_native(self, filepath, **kwargs):
        """Loads model state from a filepath in ML-framework "native" format, e.g. PyTorch pickled models. May load from multiple files. Other filepaths may be derived from the passed filepath, or they may be in the kwargs.
        Args:
            filepath (string): Path to frame-work specific file to load. For frameworks that use multiple files, this string must be used to derive the other filepaths.
            kwargs           : For future-proofing 
        Returns:
            None
        """
        raise NotImplementedError

    def run_inference_and_store_results(self, **kwargs):
        """Runs inference over the inference_loader in the data object, then calls the data object to store the results.
        Args:
            kwargs: For write_outputs method of self.data
        
        Returns:
            List of outputs from the data.write_output calls
        """
        
        # what comes out of the model object? generally numpy arrays
        # what metadata is specific to the batch? for example, simpleITK image objects of input and filenames

        # loop over inference data (each sample here is a single patient volume)
        for sample in self.data.get_inference_loader():
            features = sample["features"]
            metadata = sample["metadata"]
            
            output = self.infer_volume(features)
            self.data.write_output(output, metadata, **kwargs)
    
    def infer_volume(self, X):
        """Runs inference on a batch and returns the output of the model.
        Args:
            X: Input for batch
        Returns:
            Model output for batch
        """
        raise NotImplementedError



# Model Wrapper Code 
# Modification of openfl.models.flmodel at: https://github.com/IntelLabs/OpenFederatedLearning


class InferenceOnlyFLModelWrapper(FLModel):
    """Model class wrapper for Federated Learning to enable model inference using
    OpenFederatedLearning run inference scripts.
    """

    def __init__(self, base_model, **kwargs):
        """Initializer

        Args:
            base_model: model class satisfying the requirements provided at the start of this notebook
            **kwargs: Additional parameters,  passed to both the FLModel and base_model constructors
        """

        super(InferenceOnlyFLModelWrapper, self).__init__(**kwargs)

        self.base_model = base_model

        self.infer_volume = self.base_model.infer_volume


# Dummy Model

class DummyModel(object):
    
    def __init__(self, channels_first):
        """
        Instantiates a properly configured model object, including population
        of all model weights from a model serialization file.

        Args: channels_first (int): Whether or not the input channels are expected before
        or after the physical dimensions of the volume.

        Returns:
            An instance of the model class object.
        """       
        self.channels_first = channels_first
      
    def infer_volume(self, X):
        """
        Simulate model inference on a volume of data.

        Args:
            X (numpy array): Input volume to perform inference on, containing channels for
                             all scan modalities required for the model task. 
                             Document here any expectations on the shape of inputs.

        Returns:
            (numpy array): Model output for the input volume.
                           Document here how the output shape can be infered from the input shape.
        """           
        # produce a simulated output by averaging over the input channels,
        # then binarizing using a 0.5 threshold
        print("Dummy model input shape is: ", X.shape)
        
        # cast X to a numpy array
        X = X.numpy()
        
        if self.channels_first:
            channel_axis = 1
        else:
            channel_axis=-1
        
        # artificially produce a simulated output having the correct shape
        out = np.mean(X, axis=channel_axis)
        
        # artificially limit the output to binary
        out[out<0.5] = 0
        out[out>=0.5] = 1
        
        print("Dummy model output shape is: ", out.shape)
        
        return out
    




###########################################################################

### Data Code

# Dataset Code
# Modification of Algorithms.fets.data.pytorch.brainmage_utils 
# at: https://github.com/FETS-AI/Algorithms

# Allows for zero padding in order to enable enforcement of input dimension 
# divisibility requirements. There is a dependency between this zero-padding 
# and how outputs are cropped (see write_outputs method in cell below). This loader
# iterates over single samples only (rather than batches).

# Some utility functions

def check_for_file_or_gzip_file(path, extensions=['.gz']):
    return find_file_or_with_extension(path, extensions) is not None


def find_file_or_with_extension(path, extensions=['.gz']):
    if os.path.exists(path):
        return path

    for ext in extensions:
        if os.path.exists(path + ext):
            return path + ext
    return None


class TumorSegmentationDataset(Dataset):
    def __init__(self, 
                 dir_paths, 
                 feature_modes, 
                 channels_first,
                 outputs_only=False,
                 output_tag='',
                 divisibility_factor=1):
        self.dir_paths = dir_paths
        self.feature_modes = feature_modes
        # put channels corresponding to scanning modalities before physical dimensions
        self.channels_first = channels_first
        self.outputs_only = outputs_only
        self.output_tag = output_tag
        self.divisibility_factor = divisibility_factor

    def __len__(self):
        return len(self.dir_paths)

    def zero_pad(self, array):
        # zero pads in order to obtain a new array which is properly divisible in all dimensions except first
        current_shape = array.shape
        new_shape = list(current_shape)
        for idx in range(1,len(current_shape)):
            remainder = new_shape[idx] % self.divisibility_factor
            if remainder != 0: 
                new_shape[idx] += self.divisibility_factor - remainder
        zero_padded_array = np.zeros(shape=new_shape)
        slices = [slice(0,dim) for dim in current_shape]
        zero_padded_array[tuple(slices)] = array
        return zero_padded_array       
    
    def __getitem__(self, index):

        # get directory path and base of filename
        dir_path = self.dir_paths[index]
        fname = os.path.basename(dir_path) # base of filename matches last dirname

        # dataset solely for producing output images   
        if self.outputs_only:
            fpath = os.path.join(dir_path, fname + '_' + self.output_tag + '.nii.gz')
            if fpath is None:
                raise RuntimeError("Data sample directory missing a required image mode.")
            mode_image = sitk.ReadImage(fpath)
            mode_array = sitk.GetArrayFromImage(mode_image)
            sample = mode_array 
        else:
            feature_stack =  []
            for mode in self.feature_modes:
                fpath = find_file_or_with_extension(os.path.join(dir_path, fname + mode))
                if fpath is None:
                    raise RuntimeError("Data sample directory missing a required image mode.")
                mode_image = sitk.ReadImage(fpath)
                mode_array = sitk.GetArrayFromImage(mode_image)

                # normalize the features for this mode
                mode_array = (mode_array - np.mean(mode_array)) / np.std(mode_array)

                feature_stack.append(mode_array)
                
            if self.channels_first:
                stack_position = 0
            else:
                stack_position = -1
            feature_array = np.stack(feature_stack, axis=stack_position)
            metadata = {"dir_path": dir_path, 
                        "original_x_dim": list(mode_array.shape)[0], 
                        "original_y_dim": list(mode_array.shape)[1], 
                        "original_z_dim": list(mode_array.shape)[2]}

            feature_array = self.zero_pad(feature_array)
            sample = {'features': feature_array, 'metadata':  metadata}
        
        return sample

# Data Loader Code
# Modification of Algorithms.fets.data.pytorch.ptbrainmagedata at: https://github.com/FETS-AI/Algorithms


def get_inference_dir_paths(data_path, feature_modes):
     inference_dir_paths = [os.path.join(data_path,dir_name) for dir_name in os.listdir(data_path)]
     inference_dir_paths = remove_incomplete_data_paths(dir_paths = inference_dir_paths, 
                                                        feature_modes=feature_modes)
     return inference_dir_paths


def remove_incomplete_data_paths(dir_paths, feature_modes, label_tags=[]):
    filtered_dir_paths = []
    for path in dir_paths:
        dir_name = os.path.basename(path)
        # check to that all features are present
        all_modes_present = True
        for mode in feature_modes:
            fpath = os.path.join(path, dir_name + mode)
            if not check_for_file_or_gzip_file(fpath):
                all_modes_present = False
                break
        if all_modes_present:
            have_needed_labels = False
            for label_tag in label_tags:
                fpath = os.path.join(path, dir_name + label_tag)
                if check_for_file_or_gzip_file(fpath):
                    have_needed_labels = True
                    break
            if label_tags == []:
                have_needed_labels = True
        
        if all_modes_present and have_needed_labels:
            filtered_dir_paths.append(path)
        else:
            print("Excluding data directory: {}, as not all required files present.".format(dir_name))
    return filtered_dir_paths


class PyTorchBrainMaGeData(object):

    def __init__(self, 
                 feature_modes,
                 channels_first,
                 data_path,
                 outputs_only=False, 
                 output_tag='',
                 shuffle_samples=True,
                 divisibility_factor=1,
                 **kwargs):
        
        self.shuffle_samples = shuffle_samples
        self.feature_modes = ["_" + mode + ".nii" for mode in feature_modes]
        # put channels corresponding to scanning modalities before physical dimensions
        self.channels_first = channels_first 
        self.n_channels = len(feature_modes)
        self.outputs_only = outputs_only
        self.output_tag = output_tag
        # For loading inference data, to ensure proper dimensions using zero padding
        self.divisibility_factor = divisibility_factor

        self.inference_dir_paths = get_inference_dir_paths(data_path=data_path, 
                                                           feature_modes=self.feature_modes)

        self.inference_loader = self.create_loader()
        
    def create_loader(self):
        # This loader iterates over single samples, not batches! 
        
        dir_paths = self.inference_dir_paths
        
        if len(dir_paths) == 0:
            return []
        else:
            dataset = TumorSegmentationDataset(dir_paths = dir_paths,
                                               feature_modes = self.feature_modes,
                                               channels_first=self.channels_first,
                                               outputs_only=self.outputs_only, 
                                               output_tag=self.output_tag,
                                               divisibility_factor=self.divisibility_factor)
            return DataLoader(dataset,shuffle=self.shuffle_samples)
        
    def get_inference_loader(self):
        return self.inference_loader
    
    def write_output(self, output, metadata, output_file_tag="test_output"):
        # write output to a file in image format for inference on a single volume
            
        dir_path = metadata["dir_path"][0]
        base_fname = os.path.basename(dir_path)
        fpath = os.path.join(dir_path, base_fname + "_" + output_file_tag + ".nii.gz")
        
        # remove single dimensional axis corresponding to output channel (if it exists)
        # assuming only one channel for output here
        output = np.squeeze(output)
                  
        # recovering from the metadata what the oringal input shape was
        original_input_shape = []
        original_input_shape.append(metadata["original_x_dim"].numpy()[0])
        original_input_shape.append(metadata["original_y_dim"].numpy()[0])
        original_input_shape.append(metadata["original_z_dim"].numpy()[0])
        slices = [slice(0,original_input_shape[n]) for n in range(3)]

        # now crop to original shape (dependency here on how original zero padding was done)
        output = output[tuple(slices)]

        # convert array to SimpleITK image
        image = sitk.GetImageFromArray(output)

        
        # get header info from an input image
        input_image_fpath = os.path.join(dir_path, base_fname + self.feature_modes[0])
        input_image_fpath = find_file_or_with_extension(input_image_fpath)
        input_image= sitk.ReadImage(input_image_fpath)
        image.CopyInformation(input_image)

        print("Writing inference NIfTI image of shape {} to {}".format(output.shape, fpath))
        sitk.WriteImage(image, fpath)
            

####################################################################

### Code to Test Inference Workload

# Run Inference Code 
# Modification of bin/run_inference_from_flplan at: https://github.com/IntelLabs/OpenFederatedLearning

def test_inference(wrapped_model, **kwargs):
    """Runs the inference and store model method.
    Args:
        wrapped_model: Model wrapped in order to access data and expose infernce interface
    """


    # run inference
    wrapped_model.run_inference_and_store_results(**kwargs)


####################################################################

### Code to Visualize Inputs next to corresponding outputs

def look_at_brains(input_data, output_data, channels_first, idx, mode):
    
    # select a single output, and an image mode to use when imaging inputs
    if channels_first:
        slices = (mode, slice(None), slice(None), slice(None))
    else:
        slices = (slice(None), slice(None), slice(None), mode)
        
    imgs = input_data.inference_loader.dataset[idx]['features'][slices]
    msks=output_data.inference_loader.dataset[idx]
    
    fig, ax = plt.subplots()

    plt.subplot(1, 2, 1)
    img = plt.imshow(imgs[0].reshape(240, 240), animated=True)
    plt.subplot(1, 2, 2)
    msk = plt.imshow(msks[0].reshape(240, 240), animated=True)

    def update(frame):
        img.set_array(imgs[frame].reshape(240, 240))
        msk.set_array(msks[frame].reshape(240, 240))
        return img, msk 

    ani = FuncAnimation(fig, update, frames=np.arange(imgs.shape[0]), blit=True, interval=30)
    

    return HTML(ani.to_html5_video())




