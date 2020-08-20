.. # Copyright (C) 2020 Intel Corporation
.. # Licensed under the Apache License, Version 2.0 (the "License");
.. # you may not use this file except in compliance with the License.
.. # You may obtain a copy of the License at
.. #
.. #     http://www.apache.org/licenses/LICENSE-2.0
.. #
.. # Unless required by applicable law or agreed to in writing, software
.. # distributed under the License is distributed on an "AS IS" BASIS,
.. # WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
.. # See the License for the specific language governing permissions and
.. # limitations under the License.

Running a Federation Simulation (no network, single process)
-------------------------------------------

When exploring the convergence properties of federated learning for a particular use-case, it is helpful to run several federations in parallel, each of which runs the aggregator and collaborators (round-robin) in a single process avoiding the need for network communication. We describe here how to run one of these simulations.

Note that much of the code used for simulation (ex. collaborator and aggregator objects) is the
same as for the multiprocess solution with grpc. Since the collaborator calls the aggregator object 
methods via the grpc channel object, simulation is performed by simply replacing the channel object
provided to each collaborator with the aggregator object.

Simulations are run from an flplan, and in fact the same flplan that is used for a multi-process federation can be used.  

**Note**: Simulations utilize a single model, with each new collaborator taking control of the model when it is their turn in the round-robin. It is therefore critical that the model, 'set_tensor_dict' method completely overwrites all substantive model state in order that state does not leak from the collabotor who previously held the model.

The steps for running a simulation
----------------------------------


1. Go through the steps for project :ref:`installation_and_setup`  with the following in mind. --WORKING HERE---In this case, we require make install_openfl and make install_openfl_tensorflow. The tensorflow piece is required, as we will have the aggregator create the initial weights using the model code. The aggregator does not require this otherwise,and indeed the creation of initial weights can be done on a collaborator machine and copied to the aggregator (who needs it to start the federation) if you wish. Though the collaborator list we use here is already provided in the repository (and is already compatible with the flplan and local_data_config default file), you will also need to make sure you create a copy of the network config as part of this setup and enter in the appropriate FQDN for this machine that is running the aggregator. Finally the PKI creation step can be skipped as we will not be using the network here.

2. Now follow the stps for :ref:`creating_initial_weights` from the flplan.

3. Kick off the simulation using the flplan and the appropriate (make sure that the collaborators listed in your list are provided in included in the local data config --WORKKING HERE TOO--.

.. code-block:: console

  $ ../venv/bin/python run_simulation_from_flplan.py -p <flpan filename> -c <collaborators list filename>



4. --WOKING HREE--You'll find the output from the aggregator in bin/logs/aggregator.log. Grep this file to see results (one example below). You can check the progress as the simulation runs, if desired.

.. code-block:: console

  $ pwd                                                                                                                                                                                                                            msheller@spr-gpu01
    /home/<user>/git/openfl/bin
  $ grep -A 2 "round results" logs/aggregator.log
    2020-03-30 13:45:33,404 - openfl.aggregator.aggregator - INFO - round results for model id/version KerasCNN/1
    2020-03-30 13:45:33,404 - openfl.aggregator.aggregator - INFO -        validation: 0.4465000107884407
    2020-03-30 13:45:33,404 - openfl.aggregator.aggregator - INFO -        loss: 1.0632034242153168
    --
    2020-03-30 13:45:35,127 - openfl.aggregator.aggregator - INFO - round results for model id/version KerasCNN/2
    2020-03-30 13:45:35,127 - openfl.aggregator.aggregator - INFO -        validation: 0.8630000054836273
    2020-03-30 13:45:35,127 - openfl.aggregator.aggregator - INFO -        loss: 0.41314733028411865
    --

Note that aggregator.log is always appended to, so will include results from previous runs.

5. Edit the plan to train for more rounds, etc.



