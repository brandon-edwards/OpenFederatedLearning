# Copyright (C) 2020 Intel Corporation
# Licensed subject to the terms of the separately executed evaluation license agreement between Intel Corporation and you.

from setuptools import setup

setup(name='tfedlrn',
      version='0.0.0',
      packages=['tfedlrn',
                'tfedlrn.aggregator',
                'tfedlrn.collaborator',
                'tfedlrn.tensor_transformation_pipelines',
                'tfedlrn.proto',
                'tfedlrn.comms.grpc',
                'models',
                'models.dummy', 
                'models.pytorch', 
                'models.pytorch.pt_2dunet', 
                'models.pytorch.pt_cnn',
                'models.pytorch.pt_resnet',
                'models.tensorflow', 
                'models.tensorflow.keras_cnn', 
                'models.tensorflow.keras_resnet', 
                'models.tensorflow.tf_2dunet',
                'data', 
                'data.dummy',
                'data.pytorch', 
                'data.tensorflow',
                'fets',
                'fets.models',
                'fets.models.pytorch',
                'fets.models.pytorch.pt_3dresunet',
                'fets.models.pytorch.pt_3dresunet_ss',
                'fets.models.pytorch.brainmage',
                'fets.data',
                'fets.data.pytorch'],
      install_requires=['tensorflow==1.14.0', 'torch==1.2.0', 'protobuf', 'pyyaml', 'grpcio', 'tqdm', 'coloredlogs', 'nibabel', 'sklearn', 'SimpleITK', 'pandas']
)
