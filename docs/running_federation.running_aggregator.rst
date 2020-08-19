Running the Aggregator
####################



On the Aggregator
~~~~~~~~~~~~~~~~~


1.	To start the aggregator, run the Python script. Note that we will need to pass in the fully-qualified domain name (FQDN) for the aggregator node address in order to present the correct certificate.

.. code-block:: console

   $ ./venv/bin/python3 ./bin/run_aggregator_from_flplan.py -p keras_cnn_mnist_2.yaml -ccn AGGREGATOR.FULLY.QUALIFIED.DOMAIN.NAME --collaborators_file cols_2.yaml

.. note::

    :code:`--collaborators_file cols_2.yaml` needs to be changed to the names in your collaborator list.
    A good practice is to create a new YAML file for each of your federations. This file is only needed by the aggregator.
    These YAML files can be found in :code:`bin/federations/collaborator_lists/`

At this point, the aggregator is running and waiting
for the collaborators to connect. When all of the collaborators
connect, the aggregator starts training. When the last round of
training is complete, the aggregator stores the final weights in
the protobuf file that was specified in the YAML file
(in this case *keras_cnn_mnist_latest.pbuf*).