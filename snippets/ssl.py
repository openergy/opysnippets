"""
opysnippets/ssl:1.0.0
"""

from OpenSSL import crypto
from socket import gethostname
from os.path import join

CERT_FILE = "myapp.crt"
KEY_FILE = "myapp.key"


def create_self_signed_cert(cert_dir):
    """
    https://skippylovesmalorie.wordpress.com/2010/02/12/how-to-generate-a-self-signed-certificate-using-pyopenssl/
    If datacard.crt and datacard.key don't exist in cert_dir, create a new
    self-signed cert and keypair and write them into that directory.
    """
    # create a key pair
    k = crypto.PKey()
    k.generate_key(crypto.TYPE_RSA, 1024)

    # create a self-signed cert
    cert = crypto.X509()
    cert.get_subject().C = "US"
    cert.get_subject().ST = "Minnesota"
    cert.get_subject().L = "Minnetonka"
    cert.get_subject().O = "my company"
    cert.get_subject().OU = "my organization"
    cert.get_subject().CN = gethostname()
    cert.set_serial_number(1000)
    cert.gmtime_adj_notBefore(0)
    cert.gmtime_adj_notAfter(10 * 365 * 24 * 60 * 60)
    cert.set_issuer(cert.get_subject())
    cert.set_pubkey(k)
    cert.sign(k, 'sha1')

    with open(join(cert_dir, CERT_FILE), "wb") as f:
        f.write(crypto.dump_certificate(crypto.FILETYPE_PEM, cert))
    with open(join(cert_dir, KEY_FILE), "wb") as f:
        f.write(crypto.dump_privatekey(crypto.FILETYPE_PEM, k))
