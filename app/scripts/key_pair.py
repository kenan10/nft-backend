from coincurve.keys import PrivateKey, PublicKey
from hashlib import sha3_256
import os


class KeyPair(object):
    def __init__(self) -> None:
        self.sk = PrivateKey()
        self.pk = self.sk.public_key

    @classmethod
    def from_pem_file(cls, pem_file_path):
        with open(pem_file_path, "r") as pem_file:
            pem = bytes(pem_file.read(), "utf-8")
        key_pair = cls()
        key_pair.sk = PrivateKey.from_pem(pem)
        key_pair.pk = key_pair.sk.public_key
        return key_pair

    def save_pem(self, path_to_file):
        os.makedirs(os.path.dirname(path_to_file), exist_ok=True)
        pem = self.sk.to_pem()
        with open(path_to_file, "w") as pem_file:
            pem_file.write(str(pem, "utf-8"))

    def get_eth_style_sk(self) -> str:
        """Return an Ethereum-style secret key."""
        return self.sk.to_hex()

    def get_public_key(self) -> str:
        return str(self.pk.format().hex())

    def get_address(self) -> str:
        """Derive an Ethereum-style address from the given public key."""
        return "0x" + sha3_256(self.pk.format(False)[1:]).hexdigest()[-40:]