# Copyright (C) 2020 Intel Corporation
# Licensed subject to the terms of the separately executed evaluation license agreement between Intel Corporation and you.

from setuptools import setup

setup(name='openfl.pytorch',
      version='0.0.0',
      packages=['openfl.models.pytorch', 
                'openfl.models.pytorch.pt_2dunet', 
                'openfl.models.pytorch.pt_cnn',
                'openfl.models.pytorch.pt_resnet',
                'openfl.data.pytorch',
                'fets',
                'fets.models',
                'fets.models.pytorch',
                'fets.models.pytorch.pt_3dresunet',
                'fets.models.pytorch.brainmage',
                'fets.data',
                'fets.data.pytorch',
                ],
      exclude =['openfl',
                'openfl.aggregator',
                'openfl.collaborator',
                'openfl.tensor_transformation_pipelines',
                'openfl.proto',
                'openfl.comms.grpc',
                'openfl.models',
                'openfl.models.dummy', 
                'openfl.data', 
                'openfl.data.dummy',
                'openfl.models.tensorflow', 
                'openfl.models.tensorflow.keras_cnn', 
                'openfl.models.tensorflow.keras_resnet', 
                'openfl.models.tensorflow.tf_2dunet',
                'openfl.data.tensorflow',
                ],
      install_requires=['torch==1.6.0', 'openfl']
)
