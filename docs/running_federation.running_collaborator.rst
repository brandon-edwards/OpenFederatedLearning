.. # Copyright (C) 2020 Intel Corporation
.. # Licensed subject to the terms of the separately executed evaluation license agreement between Intel Corporation and you.


Running the Collaborator
####################

We will show you how to set up |productName| using a simple `MNIST <https://en.wikipedia.org/wiki/MNIST_database>`_
dataset and a `TensorFlow/Keras <https://www.tensorflow.org/>`_
CNN model as an example.

Before you run [links to previous steps here]

1.	Now run the collaborator col_1 using the Python script. Again,
you will need to pass in the fully qualified domain name in
order to present the correct certificate.

.. code-block:: console

   $ ./venv/bin/python3 ./bin/run_collaborator_from_flplan.py -p keras_cnn_mnist_2.yaml -col col_1 -ccn COLLABORATOR.FULLY.QUALIFIED.DOMAIN.NAME

2.	Repeat this for each collaborator in the federation. Once all
collaborators have joined, the aggregator will start and you
will see log messages describing the progress of the federated training.