Running on Baremetal
####################

We will show you how to set up |productName| using a simple `MNIST <https://en.wikipedia.org/wiki/MNIST_database>`_
dataset and a `TensorFlow/Keras <https://www.tensorflow.org/>`_
CNN model as an example.

Before you run [links to previous steps here]

On the Aggregator
~~~~~~~~~~~~~~~~~

1.	It is assumed that the federation may be fine-tuning a previously
trained model. For this reason, the pre-trained weights for the model
will be stored within protobuf files on the aggregator and
passed to the collaborators during initialization. As seen in
the YAML file, the protobuf file with the initial weights is
expected to be found in the file keras_cnn_mnist_init.pbuf. For
this example, however, we’ll just create an initial set of
random model weights and putting it into that file by running the command:

.. code-block:: console

   $ ./venv/bin/python3 ./bin/create_initial_weights_file_from_flplan.py -p keras_cnn_mnist_2.yaml -dc local_data_config.yaml --collaborators_file cols_2.yaml

.. note::

    :code:`--collaborators_file cols_2.yaml` needs to be changed to the names in your collaborator list.
    A good practice is to create a new YAML file for each of your federations. This file is only needed by the aggregator.
    These YAML files can be found in :code:`bin/federations/collaborator_lists/`



