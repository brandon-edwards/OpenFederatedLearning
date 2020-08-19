.. # Copyright (C) 2020 Intel Corporation
.. # Licensed subject to the terms of the separately executed evaluation license agreement between Intel Corporation and you.


Configuring the Collaborator
####################

We will show you how to set up |productName| using a simple `MNIST <https://en.wikipedia.org/wiki/MNIST_database>`_
dataset and a `TensorFlow/Keras <https://www.tensorflow.org/>`_
CNN model as an example.

Before you run [links to previous steps here]




On the Collaborator
~~~~~~~~~~~~~~~~~~~

1.	Make sure that you followed the steps in :ref:`Configure the Federation <install_certs>` and have copied the keys and certificates onto the federation nodes.

2.	Copy the plan file (e.g. *keras_cnn_mnist_2.yaml*) from the aggregator
over to the collaborator to the plan subdirectory (**bin/federations/plans**)

3.	Build the virtual environment using the command:

.. code-block:: console

   $ make install


