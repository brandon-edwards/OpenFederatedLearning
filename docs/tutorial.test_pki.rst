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

3. Run the aggregator cert script, replacing AGGREGATOR.FULLY.QUALIFIED.DOMAIN.NAME with the actual FQDN for the aggregator machine.

.. code-block:: console

  $ bash create-aggregator.sh -c AGGREGATOR.FULLY.QUALIFIED.DOMAIN.NAME
  Generating a RSA private key
  ...............+++++
  ................................+++++
  writing new private key to 'AGGREGATOR.FULLY.QUALIFIED.DOMAIN.NAME.key'
  -----
  Using configuration from config/signing-ca.conf
  Check that the request matches the signature
  Signature ok
  Certificate Details:
          Serial Number: 3 (0x3)
          Validity
              Not Before: May 22 17:51:52 2020 GMT
              Not After : May 22 17:51:52 2021 GMT
          Subject:
              commonName                = AGGREGATOR.FULLY.QUALIFIED.DOMAIN.NAME
          X509v3 extensions:
              X509v3 Basic Constraints:
                  CA:FALSE
              X509v3 Authority Key Identifier:
                  keyid:FE:86:D8:25:97:B3:C5:A3:3D:8C:5C:2A:7D:99:84:25:19:DE:0C:A4

              X509v3 Key Usage: critical
                  Digital Signature, Key Encipherment
              X509v3 Extended Key Usage:
                  TLS Web Server Authentication
              X509v3 Subject Key Identifier:
                  43:C6:30:45:1B:51:60:74:2B:11:C1:CE:B0:DC:84:6A:50:A7:7E:FE
              X509v3 Subject Alternative Name:
  Certificate is to be certified until May 22 17:51:52 2021 GMT (365 days)

  Write out database with 1 new entries
  Data Base Updated
  (base)
  
4. **For each test machine you want to run collaborators on**, we create a collaborator cert, replacing TEST.MACHINE.NAME with the actual test machine name. This does not have to be the FQDN:


.. code-block:: console

  $ bash create-collaborator.sh -c TEST.MACHINE.NAME
  Generating a RSA private key
  .................................................+++++
  .................+++++
  writing new private key to 'TEST.MACHINE.NAME.key'
  -----
  req: Skipping unknown attribute "WD"
  Using configuration from config/signing-ca.conf
  Check that the request matches the signature
  Signature ok
  Certificate Details:
          Serial Number: 4 (0x4)
          Validity
              Not Before: May 22 18:00:34 2020 GMT
              Not After : May 22 18:00:34 2021 GMT
          Subject:
              commonName                = TEST.MACHINE.NAME
          X509v3 extensions:
              X509v3 Basic Constraints:
                  CA:FALSE
              X509v3 Authority Key Identifier:
                  keyid:FE:86:D8:25:97:B3:C5:A3:3D:8C:5C:2A:7D:99:84:25:19:DE:0C:A4

              X509v3 Key Usage: critical
                  Digital Signature, Key Encipherment
              X509v3 Extended Key Usage:
                  TLS Web Client Authentication
              X509v3 Subject Key Identifier:
                  BB:FB:75:2D:79:93:78:FC:78:03:32:DE:53:1F:99:85:C7:37:01:F3
              X509v3 Subject Alternative Name:
  Certificate is to be certified until May 22 18:00:34 2021 GMT (365 days)

  Write out database with 1 new entries
  Data Base Updated
  (base)
