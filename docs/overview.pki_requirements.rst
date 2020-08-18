.. # Copyright (C) 2020 Intel Corporation
.. # Licensed subject to the terms of the separately executed evaluation license agreement between Intel Corporation and you.

*****************************************
PKI Requirements
*****************************************

By default, |productName| uses `TLS <https://en.wikipedia.org/wiki/Transport_Layer_Security>`_ encryption for the network connections.

TODO: MIKE BEALE PLEASE ADD DISCLAIMER HERE!!!

Collaborator-to-Aggregator TLS
##############################

For the TLS connection between the collaborators and the aggregator, each node (aggregator/collaborator) in the federation requires:
- A cert_chain.crt file that holds the certificate/public key for the trusted signer.
- A .crt file that holds the public key and common name for the node, signed by the trusted signer.
- A .key file that holds the private key that goes with the .crt file.

Additionally, aggregator node certificates should be server certificates, while collaborator node certificates should be client certificates.

.. note::

   The common name (CN) of the aggregator certificate must either be the FQDN of the aggregator or the IP address.

.. note::

   The common name (CN) of the collaborator certificate must match the name used by the collaborator. The aggregator has a list of approved common names and will reject connections from collaborators whose cert CNs are not in that list.


Single Collaborator Cert Common Name Mode for testing
#####################################################

|productName| provides a convenience option called "Single Collaborator Cert Common Name" (SCN) mode that allows developers/testers to re-use the same collaborator certificate for each collaborator.
**This should only be use in fully trusted test environments on the same trusted network, and should never be used if any nodes are not under direct control of the tester/developer!**
Normally, the aggregator checks the cert to ensure that the collaborator name matches the common name in the certificate.
This mode allows a collaborator node to masquerade as any collaborator by instead instructing the aggregator to check that the common name in the cert matches a specific name given to it when launched.
Therefore, the collaborator process can claim any name it wishes, so long as it presents a certificate with that specific common name.
This is especially useful for a test environment where collaborator nodes may run on different machines at different times.
(Note that in SCN mode, the collaborator name must be in the approved list. The collaborator name just doesn't have to match the CN in the cert is uses).

To enable SCN mode, pass -scn <common name> to **each** process in the federation.

.. note::

   Nodes that have been launched with different SCN settings will refuse to connect.

Disabling TLS
#############

Finally, it is possible to disable TLS entirely. **Do this at your own risk**. In the <TODO: link network configuration section> section, you will see a "disable_tls" configuration option. 

.. note::

   Some IT departments configure networks to drop unencrypted RPC traffic like gRPC. In such cases, disabling TLS could prevent the nodes from connecting.
