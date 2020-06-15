.. # Copyright (C) 2020 Intel Corporation
.. # Licensed subject to the terms of the separately executed evaluation license agreement between Intel Corporation and you.


How to set up Federated Learning on Docker
-------------------------------------------

We will show you how to set up federated learning on Docker
using the simplest MNIST dataset as an example.

Before we start the tutorial, please make sure you have Docker
installed and confugured properly. Here is a easy test to run in order to test some basic functionality:

.. code-block:: console

  $ docker run hello-world
  Hello from Docker!
  This message shows that your installation appears to be working correctly.
  ...
  ...
  ...

Additionally, we need to set up the PKI for our test machines. See docs/tutorial.test_pki.rst for how to set up a PKI among trusted test machines. **Note that PKI tutorial is not for production deployments, as explained in that tutorial**

Federated Training of an MNIST Classifier
-------------------------------------------

Configure The Federation
^^^^^^^^^^^^^^^^^^^^^^^^

(**Every machine needs configured. We recommend creating/editing config files on a single machine,
then copying files to the others, as indicated in the table at the end. Eventually, the Governor
will handle most of this**)

1. Enter the project folder.
Note that "spr_secure_intelligence-trusted_federated_learning"
is the folder name we chose for the local repository.
It can be anything of your choice on your machine.

.. code-block:: console

  $ cd spr_secure_intelligence-trusted_federated_learning

2. Edit the FL plan file to specify the correct addresses for your machines.
Open bin/federations/plans/keras_cnn_mnist_2.yaml:

.. code-block:: console

  $ vi bin/federations/plans/keras_cnn_mnist_2.yaml


Find the keys in the federation config for the address ("agg_addr") and port ("agg_port"):

.. code-block:: console

  ...
  federation:
    fed_id: &fed_id 'fed_0'
    opt_treatment: &opt_treatment 'RESET'
    polling_interval: &polling_interval 4
    rounds_to_train: &rounds_to_train 16
    agg_id: &agg_id 'agg_0'
    agg_addr: &agg_addr "agg.domain.com"   # CHANGE THIS STRING
    agg_port: &agg_port <some_port>        # CHANGE THIS INT
...


Next find the "aggregator" section and the subkey "test_mode_whitelist" and enter the common names used for the certificates  for each collaborator machine you created in the test_pki step. Note that you must only whitelist test machines that you trust, as such machines are able to act as any collaborator id. This is why we call this "test_mode", as this is not proper security in a production setting.

.. code-block:: console

  ...

  aggregator:
    agg_id: *agg_id
    fed_id: *fed_id
    col_ids: *col_ids
    rounds_to_train: *rounds_to_train
    test_mode_whitelist:
      - TEST_MACHINE_NAME   # CHANGE TO THE COMMON NAME USED IN THE COLLABORATOR CERT FOR THIS MACHINE
      - TEST_MACHINE_NAME2  # CHANGE TO THE COMMON NAME USED IN THE COLLABORATOR CERT FOR THIS MACHINE
  ...

4. Copy the modified FL plan to each test machine. When done, each machine should have the same file at bin/federations/plans/keras_cnn_mnist_2.yaml

Start an Aggregator
^^^^^^^^^^^^^^^^^^^^

1. Build the docker images "tfl_agg_<model_name>_<username>:0.1" and 
"tfl_col_<model_name>_<username>:0.1" using project folder Makefile targets.
This uses the project folder "Dockerfile".
We only build them once, unless we change `Dockerfile`.
We pass along the proxy configuration from the host machine
to the docker container, so that your container would be
able to access the Internet from typical corporate networks.
We also create a container user with the same UID so that it is easier
to access the mapped local volume from the docker container.
Note that we include the username to avoid development-time collisions
on shared develpment servers.
We build the collaborator Docker image upon the aggregator image, 
adding necessary dependencies such as the mainstream deep learning 
frameworks. You may modify `./models/<model_name>/Dockerfile` to install
the needed packages.


.. code-block:: console

  $ make build_containers model_name=keras_cnn
    docker build \
    --build-arg BASE_IMAGE=ubuntu:18.04 \
    --build-arg http_proxy \
    --build-arg https_proxy \
    --build-arg socks_proxy \
    --build-arg ftp_proxy \
    --build-arg no_proxy \
    --build-arg UID=11632344 \
    --build-arg GID=2222 \
    --build-arg UNAME=edwardsb \
    -t tfl_agg_keras_cnn_edwardsb:0.1 \
    -f Dockerfile \
    .
    Sending build context to Docker daemon   3.25GB
    Step 1/29 : ARG BASE_IMAGE=ubuntu:18.04
    Step 2/29 : FROM $BASE_IMAGE
     ---> ccc6e87d482b    
       ...
       ...
       ...
       
    Step 29/29 : ENV PATH=/home/${UNAME}/tfl/venv/bin:$PATH
     ---> Running in 5d41487d94f4
    Removing intermediate container 5d41487d94f4
     ---> 1e71e09a4a5a
    Successfully built 1e71e09a4a5a
    Successfully tagged tfl_agg_keras_cnn_edwardsb:0.1
    docker build --build-arg whoami=edwardsb \
    --build-arg use_gpu=false \
    -t tfl_col_cpu_keras_cnn_edwardsb:0.1 \
    -f ./models/tensorflow/keras_cnn/cpu.dockerfile \
    .
    Sending build context to Docker daemon  3.251GB
    Step 1/7 : ARG whoami
    
      ...
      ...
      ...
    
    
    
    Step 7/7 : RUN pip3 install intel-tensorflow==1.14.0;
     ---> Using cache
     ---> 7d1b3ef6fb8c
    Successfully built 7d1b3ef6fb8c
    Successfully tagged tfl_col_cpu_keras_cnn_edwardsb:0.1

2. Run the aggregator container (entering a bash shell inside the container), 
again using the Makefile. Note that we map the local volumes `./bin/federations` to the container

.. code-block:: console

  $ make run_agg_container model_name=keras_cnn
  Aggregator container started. You are in the Docker container.
  Make sure you've defined the initial weights protobuf file before starting the aggregator.
  Run the command: python3 run_aggregator_from_flplan.py -p PLAN_NAME.yaml -ccn AGGREGATOR.FULLY.QUALIFIED.DOMAIN.NAME
  [FL Docker for Aggregator ~/tfl/bin >>


3. In the aggregator container shell, build the initial weights files providing the global model initialization 
that will be sent from the aggregator out to all collaborators.

.. code-block:: console

  $ ./create_initial_weights_file_from_flplan.py -p keras_cnn_mnist_2.yaml -dc docker_data_config.yaml

  ...
  ...
  ...

  created /home/msheller/tfl/bin/federations/weights/keras_cnn_mnist_init.pbuf

4. In the aggregator container shell, run the aggregator, using the following python command, replacing the aggregator FQDN for AGGREGATOR.FULLY.QUALIFIED.DOMAIN.NAME:

.. code-block:: console

  $ python3 run_aggregator_from_flplan.py -p keras_cnn_mnist_2.yaml -ccn AGGREGATOR.FULLY.QUALIFIED.DOMAIN.NAME
  Loaded logging configuration: logging.yaml
  2020-01-15 23:17:18,143 - tfedlrn.aggregator.aggregatorgrpcserver - DEBUG - Starting aggregator.


Start Collaborators
^^^^^^^^^^^^^^^^^^^^

Note: the collaborator machines can be the same as the aggregator machine.

1. (**On each collaborator machine**) Enter the project folder and build the containers as above.

.. code-block:: console

  $ make build_containers model_name=keras_cnn


2. (**On the first collaborator machine**)
Run the first collaborator container (entering a bash shell inside the container) 
using the project folder Makefile. Note that we map the local volumes `./bin/federations` 
to the docker container, and that we set different names for the two 
collaborator containers (hence the argument 'col_name'), though they share the same 
docker image.

.. code-block:: console

  $ make run_col_container model_name=keras_cnn col_name=col_0
  Collaborator col_0 container started. You are in the Docker container
  Run the command: python3 run_collaborator_from_flplan.py -p PLAN_NAME.yaml -ccn TEST_MACHINE_COMMON_NAME -col col_0 -dc docker_data_config.yaml
  [FL Docker for Collaborator col_0 ~/tfl/bin >>

5. In this first collaborator shell, run the collabotor using the following command, replacing TEST_MACHINE_COMMON_NAME with the common name used in the cert for this machine:

.. code-block:: console

  $ python3 run_collaborator_from_flplan.py -p keras_cnn_mnist_2.yaml -ccn TEST_MACHINE_COMMON_NAME -col col_0 -dc docker_data_config.yaml
  

6. (**On the second collaborator machine, which could be a second terminal on the first machine**)
Run the second collaborator container (entering a bash shell inside the container).

.. code-block:: console

  $ make run_col_container model_name=keras_cnn col_name=col_1
  Collaborator col_1 container started. You are in the Docker container
  Run the command: python3 run_collaborator_from_flplan.py -p PLAN_NAME.yaml -ccn TEST_MACHINE_COMMON_NAME -col col_1 -dc docker_data_config.yaml
  [FL Docker for Collaborator col_1 ~/tfl/bin >>

7. In the second collaborator container shell, run the second collaborator, again setting the common name in the cert for this collaborator:

.. code-block:: console

  $ python3 run_collaborator_from_flplan.py -p keras_cnn_mnist_2.yaml -ccn TEST_MACHINE_COMMON_NAME -col col_1 -dc docker_data_config.yaml
  
The federation will train for 16 rounds. When it completes, in the aggregator console, you should see the following:

.. code-block:: console
  2020-06-15 18:04:42,716 - tfedlrn.aggregator.aggregator - INFO - round results for model id/version KerasCNN/15
  2020-06-15 18:04:42,717 - tfedlrn.aggregator.aggregator - INFO -        validation: 0.9570000171661377
  2020-06-15 18:04:42,717 - tfedlrn.aggregator.aggregator - INFO -        loss: 0.08092422783374786
  2020-06-15 18:04:42,718 - tfedlrn.aggregator.aggregator - DEBUG - Start a new round 17.
  2020-06-15 18:04:42,719 - tfedlrn.aggregator.aggregator - DEBUG - aggregator handled UploadLocalMetricsUpdate in time 0.0031032562255859375
  2020-06-15 18:04:42,719 - tfedlrn.aggregator.aggregator - DEBUG - aggregator handled UploadLocalMetricsUpdate in time 0.0032558441162109375
  2020-06-15 18:04:42,720 - tfedlrn.aggregator.aggregator - DEBUG - Receive job request from col_0 and assign with 3
  2020-06-15 18:04:42,721 - tfedlrn.aggregator.aggregator - DEBUG - aggregator handled RequestJob in time 0.0003361701965332031
  2020-06-15 18:04:45,465 - tfedlrn.aggregator.aggregator - DEBUG - Receive job request from col_1 and assign with 3
  2020-06-15 18:04:45,465 - tfedlrn.aggregator.aggregator - DEBUG - aggregator handled RequestJob in time 0.0003685951232910156
  [FL Docker for Aggregator ~/tfl/bin >>


Federated Training of the 2D UNet (Brain Tumor Segmentation)
-----------------------------------------------------------------

This tutorial assumes that you've run the MNIST example above in that less details are provided.


1. Unlike the MNIST toy example, in this example we are allocating data correctly. To make this work,
we create a <Brats Symlinks Dir>, which is has directories of symlinks to the data for each institution
number. Setting this up is out-of-scope for this code at the moment, so we leave this to the reader. In
the end, our directory looks like below. Note that "0-9" allows us to do data-sharing training.

.. code-block:: console

  $ ll <Brats Symlinks Dir>

  ...
    drwxr-xr-x  90 <user> <group> 4.0K Nov 25 22:14 0
    drwxr-xr-x 212 <user> <group>  12K Nov  2 16:38 0-9
    drwxr-xr-x  24 <user> <group> 4.0K Nov 25 22:14 1
    drwxr-xr-x  36 <user> <group> 4.0K Nov 25 22:14 2
    drwxr-xr-x  14 <user> <group> 4.0K Nov 25 22:14 3
    drwxr-xr-x  10 <user> <group> 4.0K Nov 25 22:14 4
    drwxr-xr-x   6 <user> <group> 4.0K Nov 25 22:14 5
    drwxr-xr-x  10 <user> <group> 4.0K Nov 25 22:14 6
    drwxr-xr-x  16 <user> <group> 4.0K Nov 25 22:14 7
    drwxr-xr-x  17 <user> <group> 4.0K Nov 25 22:14 8
    drwxr-xr-x   7 <user> <group> 4.0K Nov 25 22:14 9
  ...


2. (**We start with just a two collaborator example.**)
Edit the FL plan file to specify the correct addresses for your machines.
Open bin/federations/plans/brats17_insts2_3.yaml.

.. code-block:: console

  $ vi bin/federations/plans/tf_2dunet_brats_insts2_3.yaml


Find the keys in the federation config for the address ("agg_addr") and port ("agg_port"):

.. code-block:: console

  ...
  federation:
    fed_id: &fed_id 'fed_0'
    opt_treatment: &opt_treatment 'AGG'
    polling_interval: &polling_interval 4
    rounds_to_train: &rounds_to_train 50
    agg_id: &agg_id 'agg_0'
    agg_addr: &agg_addr "agg.domain.com"   # CHANGE THIS STRING
    agg_port: &agg_port <some_port>        # CHANGE THIS INT
...


Next find the "aggregator" section and the subkey "test_mode_whitelist" and enter the common names used for the certificates  for each collaborator machine you created in the test_pki step. Note that you must only whitelist test machines that you trust, as such machines are able to act as any collaborator id. This is why we call this "test_mode", as this is not proper security in a production setting.

.. code-block:: console

  ...

  aggregator:
    agg_id: *agg_id
    fed_id: *fed_id
    col_ids: *col_ids
    rounds_to_train: *rounds_to_train
    test_mode_whitelist:
      - TEST_MACHINE_NAME   # CHANGE TO THE COMMON NAME USED IN THE COLLABORATOR CERT FOR THIS MACHINE
      - TEST_MACHINE_NAME2  # CHANGE TO THE COMMON NAME USED IN THE COLLABORATOR CERT FOR THIS MACHINE
  ...


3. Edit the docker data config file to refer to the correct username (the name of the account
you are using. Open bin/federations/docker_data_config.yaml and replace the username with your username

.. code-block:: console

  $ vi bin/federations/docker_data_config.yaml

  collaborators:
    col_one_big:
      brats: &brats_data_path '/home/<USERNAME>/tfl/datasets/brats'                # replace with your username
    col_0:
      brats: *brats_data_path   
      mnist_shard: 0
    col_1:
      brats: *brats_data_path
      mnist_shard: 1
  ...


5. Copy the fl plan bin/federations/plans/tf_2dunet_brats_insts2_3.yaml to each machine.

Start an Aggregator
^^^^^^^^^^^^^^^^^^^^

1. Build the docker images "tfl_agg_<model_name>_<username>:0.1" and 
"tfl_col_<model_name>_<username>:0.1" using project folder Makefile targets.
This uses the project folder "Dockerfile".
We only build them once, unless we change `Dockerfile`.
We pass along the proxy configuration from the host machine
to the docker container, so that your container would be
able to access the Internet from typical corporate networks.
We also create a container user with the same UID so that it is easier
to access the mapped local volume from the docker container.
Note that we include the username to avoid development-time collisions
on shared develpment servers.
We build the collaborator Docker image upon the aggregator image, 
adding necessary dependencies such as the mainstream deep learning 
frameworks. You may modify `./models/<model_name>/Dockerfile` to install
the needed packages.


.. code-block:: console

  $ make build_containers model_name=tf_2dunet
 

2. Run the aggregator container (entering a bash shell inside the container), 
again using the Makefile. Note that we map the local volumes `./bin/federations` to the container

.. code-block:: console

  $ make run_agg_container model_name=tf_2dunet dataset=brats

3. In the aggregator container shell, build the initial weights files providing the global model initialization 
that will be sent from the aggregator out to all collaborators.

.. code-block:: console

  $ ./create_initial_weights_file_from_flplan.py -p tf_2dunet_brats_insts2_3.yaml -dc docker_data_config.yaml



4. In the aggregator container shell, run the aggregator, using the following python command, replacing the aggregator FQDN for AGGREGATOR.FULLY.QUALIFIED.DOMAIN.NAME:

.. code-block:: console

  $ python3 run_aggregator_from_flplan.py -p tf_2dunet_brats_insts2_3.yaml -ccn AGGREGATOR.FULLY.QUALIFIED.DOMAIN.NAME
  Loaded logging configuration: logging.yaml
  2020-01-15 23:17:18,143 - tfedlrn.aggregator.aggregatorgrpcserver - DEBUG - Starting aggregator.


Start Collaborators
^^^^^^^^^^^^^^^^^^^^

Note: the collaborator machines can be the same as the aggregator machine.

1. (**On each collaborator machine**) Enter the project folder and build the containers as above.

.. code-block:: console

  $ make build_containers model_name=tf_2dunet


2. (**On the first collaborator machine**)
Run the first collaborator container. Note we are using collaborators 2 and 3.

.. code-block:: console

  $ make run_col_container model_name=tf_2dunet dataset=brats col_name=col_2

5. In this first collaborator shell, run the collabotor using the following command, replacing TEST_MACHINE_COMMON_NAME with the common name used in the cert for this machine:

.. code-block:: console

  $ python3 run_collaborator_from_flplan.py -p tf_2dunet_brats_insts2_3.yaml -ccn TEST_MACHINE_COMMON_NAME -col col_2 -dc docker_data_config.yaml

6. (**On the second collaborator machine, which could be a second terminal on the first machine**)
Run the second collaborator container (entering a bash shell inside the container).

.. code-block:: console

  $ make run_col_container model_name=tf_2dunet dataset=brats col_name=col_3

5. In this first collaborator shell, run the collabotor using the following command, replacing TEST_MACHINE_COMMON_NAME with the common name used in the cert for this machine:

.. code-block:: console

  $ python3 run_collaborator_from_flplan.py -p tf_2dunet_brats_insts2_3.yaml -ccn TEST_MACHINE_COMMON_NAME -col col_3 -dc docker_data_config.yaml


