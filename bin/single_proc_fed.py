# Copyright (C) 2020 Intel Corporation
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from enum import Enum
import os

from openfl.flplan import create_data_object, create_model_object, create_compression_pipeline, create_aggregator_object_from_flplan, create_collaborator_object_from_flplan


def federate(flplan, 
             resume,
             local_config,
             collaborator_common_names,
             base_dir,
             weights_dir,
             metadata_dir,
             model_device, 
             local_outputs_directory, 
             no_local_outputs):   

    # create the data objects for each collaborator
    data_objects = {collaborator_common_name: create_data_object(flplan, collaborator_common_name, local_config)  for collaborator_common_name in collaborator_common_names}

    # for simulation we create multiple directories under the local_outputs_direcotry (one for each collaborator)
    local_outputs_directories = {name: os.path.join(local_outputs_directory, 'model_outputs_for_' + name) for name in collaborator_common_names}
    for dir_name in local_outputs_directories.values():
        if not os.path.exists(dir_name):
            os.mkdir(dir_name)
    
    # instantiate the model (using the first collaborator dataset for now)
    model = create_model_object(flplan, data_objects[collaborator_common_names[0]], model_device)
    
    # FL collaborators are statefull. Since this single process script utilizes one
    # shared model for all collaborators, model states need to be tracked.
    model_states = {collaborator_common_name: None for collaborator_common_name in collaborator_common_names}

    # create the compressor
    compression_pipeline = create_compression_pipeline(flplan)

    # if we have not already specified minimum_reporting in the plan, set to number of collaborators
    if flplan['aggregator_object_init']['init_kwargs'].get('minimum_reporting') is None:
        flplan['aggregator_object_init']['init_kwargs']['minimum_reporting'] = len(collaborator_common_names)

    # create the aggregator
    aggregator = create_aggregator_object_from_flplan(flplan,
                                                      collaborator_common_names,
                                                      None,
                                                      base_dir,
                                                      weights_dir,
                                                      metadata_dir, 
                                                      resume=resume)

    # create the collaborators
    collaborators = {} 
    for collaborator_common_name in collaborator_common_names:
        collaborators[collaborator_common_name] = \
            create_collaborator_object_from_flplan(flplan,
                                                   collaborator_common_name,
                                                   local_config,
                                                   base_dir,
                                                   weights_dir,
                                                   metadata_dir, 
                                                   local_outputs_directory=local_outputs_directories[collaborator_common_name],
                                                   no_local_outputs=no_local_outputs,
                                                   data_object=data_objects[collaborator_common_name],
                                                   model_object=model,
                                                   compression_pipeline=compression_pipeline,
                                                   network_object=aggregator)

    rounds_to_train = flplan['aggregator_object_init']['init_kwargs']['rounds_to_train']

    # TODO: Enable flat score detection, minimum accept, etc.
    for round in range(rounds_to_train):
        for collaborator_common_name in collaborator_common_names:

            collaborator = collaborators[collaborator_common_name]

            # overwrite the model's data using current insitution
            model.set_data(data_objects[collaborator_common_name])
            
            if round != 0:
                # restore model state from when this collaborator last held the model
                model.set_tensor_dict(model_states[collaborator_common_name], with_opt_vars=True)

            # run the collaborator jobs for this round
            collaborator.run_to_yield_or_quit()

            model_states[collaborator_common_name] = model.get_tensor_dict(with_opt_vars=True)
