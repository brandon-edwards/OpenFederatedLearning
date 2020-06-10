.. # Copyright (C) 2020 Intel Corporation
.. # Licensed subject to the terms of the separately executed evaluation license agreement between Intel Corporation and you.

**All provided PKI scripts are provided as-is with no guarantees. Use at your own risk**

How to create a test PKI
-------------------------------------------

For testing, we have provided helpful scripts in bin/federation/pki to set up a root ca, signing cert, server cert for the aggregator and client certs for the collaborators.

We will be creating a collaborator key and cert for each **machine** we will use for testing, rather than for each collaborator. This allows us to easily run multiple collaborators on a single test machine, and easily change which test machines run which collaborators.

**NOTE**: By default, OFL requires a cert for each collaborator. However, an aggregator can be run in a test mode that allows you to whitelist machines and run any collaborator on any whitelisted machine. **In test mode, you must trust each of these machines! This is not proper security for real federations!**

Create the root-ca and signing cert
^^^^^^^^^^^^^^^^^^^^^^^^

1. To prepare, make sure you have openssl installed. (Tested with OpenSSL 1.1.1b)

2. Enter the project folder and then the pki folder

.. code-block:: console

  $ cd spr_secure_intelligence-trusted_federated_learning
  $ cd bin/federations/pki

3. Run the ca setup script and sign the root cert and signing cert when prompted:

.. code-block:: console

  $ bash setup_ca.sh
  -----                                                                                                                                                                                                                                                                   [0/177]
  Using configuration from config/root-ca.conf
  Check that the request matches the signature
  Signature ok
  Certificate Details:
          Serial Number: 1 (0x1)
          Validity
              Not Before: May 22 17:46:00 2020 GMT
              Not After : May 22 17:46:00 2021 GMT
          Subject:
              domainComponent           = org
              domainComponent           = simple
              organizationName          = Simple Inc
              organizationalUnitName    = Simple Root CA
              commonName                = Simple Root CA
          X509v3 extensions:
              X509v3 Key Usage: critical
                  Certificate Sign, CRL Sign
              X509v3 Basic Constraints: critical
                  CA:TRUE
              X509v3 Subject Key Identifier:
                  C8:65:3F:45:75:55:F0:66:25:D3:78:F8:70:55:ED:D3:3A:32:58:E4
              X509v3 Authority Key Identifier:
                  keyid:C8:65:3F:45:75:55:F0:66:25:D3:78:F8:70:55:ED:D3:3A:32:58:E4

  Certificate is to be certified until May 22 17:46:00 2021 GMT (365 days)
  Sign the certificate? [y/n]:y


  1 out of 1 certificate requests certified, commit? [y/n]y
  Write out database with 1 new entries
  Data Base Updated
  Generating a RSA private key
  ...................................................................................................+++++
  ......................................+++++
  writing new private key to 'ca/signing-ca/private/signing-ca.key'
  -----
  Using configuration from config/root-ca.conf
  Check that the request matches the signature
  Signature ok
  Certificate Details:
          Serial Number: 2 (0x2)
          Validity
              Not Before: May 22 17:46:16 2020 GMT
              Not After : May 22 17:46:16 2021 GMT
          Subject:
              domainComponent           = org
              domainComponent           = simple
              organizationName          = Simple Inc
              organizationalUnitName    = Simple Signing CA
              commonName                = Simple Signing CA
          X509v3 extensions:
              X509v3 Key Usage: critical
                  Certificate Sign, CRL Sign
              X509v3 Basic Constraints: critical
                  CA:TRUE, pathlen:0
              X509v3 Subject Key Identifier:
                  FE:86:D8:25:97:B3:C5:A3:3D:8C:5C:2A:7D:99:84:25:19:DE:0C:A4
              X509v3 Authority Key Identifier:
                  keyid:C8:65:3F:45:75:55:F0:66:25:D3:78:F8:70:55:ED:D3:3A:32:58:E4

  Certificate is to be certified until May 22 17:46:16 2021 GMT (365 days)
  Sign the certificate? [y/n]:y


  1 out of 1 certificate requests certified, commit? [y/n]y
  Write out database with 1 new entries
  Data Base Updated
  (base) ------

3. Run the aggregator cert script, replacing AGGREGATOR.FULLY.QUALIFIED.DOMAIN.NAME with the actual FQDN for the aggregator machine. You may optionally include the IP address for the aggregator, replacing [IP_ADDRESS]

.. code-block:: console

  $ bash create-aggregator.sh AGGREGATOR.FULLY.QUALIFIED.DOMAIN.NAME
  Valid FQDN
  No IP specified. IP address will not be included in subject alt name.
  Creating debug client key pair with following settings: CN=AGGREGATOR.FULLY.QUALIFIED.DOMAIN.NAME SAN=DNS:AGGREGATOR.FULLY.QUALIFIED.DOMAIN.NAME
  Generating a RSA private key
  ..............+++++
  ..................+++++
  writing new private key to 'agg_AGGREGATOR.FULLY.QUALIFIED.DOMAIN.NAME.key'
  -----
  Using configuration from config/signing-ca.conf
  Check that the request matches the signature
  Signature ok
  Certificate Details:
          Serial Number: 2 (0x2)
          Validity
              Not Before: Jun 10 22:39:03 2020 GMT
              Not After : Jun 10 22:39:03 2021 GMT
          Subject:
              commonName                = AGGREGATOR.FULLY.QUALIFIED.DOMAIN.NAME
          X509v3 extensions:
              X509v3 Basic Constraints:
                  CA:FALSE
              X509v3 Authority Key Identifier:
                  keyid:9F:B0:5A:5C:17:7B:67:44:5B:E6:6C:B8:F7:9E:17:D7:54:18:13:27

              X509v3 Key Usage: critical
                  Digital Signature, Key Encipherment
              X509v3 Extended Key Usage:
                  TLS Web Server Authentication
              X509v3 Subject Key Identifier:
                  72:FD:FB:70:54:32:40:D6:5D:30:B4:7E:05:C3:F3:C6:75:4D:89:5C
              X509v3 Subject Alternative Name:
                  DNS:AGGREGATOR.FULLY.QUALIFIED.DOMAIN.NAME
  Certificate is to be certified until Jun 10 22:39:03 2021 GMT (365 days)

  Write out database with 1 new entries
  Data Base Updated
  
4. **For each test machine you want to run collaborators on**, we create a collaborator cert, replacing TEST.MACHINE.NAME with the actual test machine name. This does not have to be the FQDN:


.. code-block:: console

  $ bash create-collaborator.sh TEST.MACHINE.NAME
  Note: collaborator CN is not a valid FQDN and will not be added to the DNS entry of the subject alternative names
  Creating collaborator key pair with following settings: CN=TEST_MACHINE_NAME SAN=DNS:TEST_MACHINE_NAME
  Generating a RSA private key
  ...............................................................................................................+++++
  ..............................+++++
  writing new private key to 'col_TEST_MACHINE_NAME.key'
  -----
  Using configuration from config/signing-ca.conf
  Check that the request matches the signature
  Signature ok
  Certificate Details:
          Serial Number: 3 (0x3)
          Validity
              Not Before: Jun 10 22:40:41 2020 GMT
              Not After : Jun 10 22:40:41 2021 GMT
          Subject:
              commonName                = TEST_MACHINE_NAME
          X509v3 extensions:
              X509v3 Basic Constraints:
                  CA:FALSE
              X509v3 Authority Key Identifier:
                  keyid:9F:B0:5A:5C:17:7B:67:44:5B:E6:6C:B8:F7:9E:17:D7:54:18:13:27

              X509v3 Key Usage: critical
                  Digital Signature, Key Encipherment
              X509v3 Extended Key Usage:
                  TLS Web Client Authentication
              X509v3 Subject Key Identifier:
                  8C:81:F5:1B:5B:85:F5:24:C0:2D:E8:38:CE:D7:63:3A:BF:D3:06:3C
              X509v3 Subject Alternative Name:
                  DNS:TEST_MACHINE_NAME
  Certificate is to be certified until Jun 10 22:40:41 2021 GMT (365 days)

  Write out database with 1 new entries
  Data Base Updated

5. Once you have the certificates created, you need to move the certs to the correct machines and ensure each machine has the cert_chain.crt needed to verify cert signatures. For example, on a test machine named TEST_MACHINE that you want to be able to run as a collaborator, you should have:
  * bin/federations/pki/cert_chain.crt
  * bin/federations/pki/col_TEST_MACHINE/col_TEST_MACHINE.crt
  * bin/federations/pki/col_TEST_MACHINE/col_TEST_MACHINE.key

While on an machine you want to run as an aggregator with FQDN AGGREGATOR.FULLY.QUALIFIED.DOMAIN.NAME, you should have:
  * bin/federations/pki/cert_chain.crt
  * bin/federations/pki/agg_AGGREGATOR.FULLY.QUALIFIED.DOMAIN.NAME/agg_AGGREGATOR.FULLY.QUALIFIED.DOMAIN.NAME.crt
  * bin/federations/pki/agg_AGGREGATOR.FULLY.QUALIFIED.DOMAIN.NAME/agg_AGGREGATOR.FULLY.QUALIFIED.DOMAIN.NAME.key
