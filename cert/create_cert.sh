#!/bin/sh
set -e

cd "$(dirname "${0}")"

#------------------------------------------------------------------------------
# cleanup any previously created files
rm -f exampleca.* example.*

#------------------------------------------------------------------------------
# create a CA called "myca"

# create a private key
openssl genrsa -out exampleca.key 1024

# create certificate
cat > exampleca.conf << EOF
[ req ]
distinguished_name     = req_distinguished_name
prompt                 = no
[ req_distinguished_name ]
C = DC
ST = Batman
L = Gotham
O = CAExample
CN = Example Certificate Authority
EOF
openssl req -new -x509 -days 3650 -key exampleca.key -out exampleca.crt -config exampleca.conf
# create serial number file
echo "01" > exampleca.srl

#------------------------------------------------------------------------------
# create a certificate for the ESP (hostname: "myesp")

# create a private key
openssl genrsa -out example.key 1024
# create certificate signing request
cat > example.conf << EOF
[ req ]
distinguished_name     = req_distinguished_name
prompt                 = no
[ req_distinguished_name ]
C = DC
ST = Batman
L = Gotham
O = Example
CN = uhttps.example.com
EOF
openssl req -new -key example.key -out example.csr -config example.conf

# have myca sign the certificate
openssl x509 -days 3650 -CA exampleca.crt -CAkey exampleca.key -in example.csr -req -out example.crt

# verify
openssl verify -CAfile exampleca.crt example.crt
