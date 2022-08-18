from web3.auto import w3
from web3 import Web3
import os
from eth_account.messages import encode_defunct
from eth_keys import keys


class KeyPair(object):
    def __init__(self) -> None:
        self.sk_bytes = os.urandom(32)
        self.sk = keys.PrivateKey(self.sk_bytes)
        self.pk = keys.PublicKey.from_private(self.sk)
        self.address = self.pk.to_address()

    def save_txt(self, path_to_file):
        os.makedirs(os.path.dirname(path_to_file), exist_ok=True)
        with open(path_to_file, "w") as f:
            f.write(self.sk_bytes.hex())
            f.write("\n")
            f.write(self.address)

    def sign_address(self, address: str):
        message_hash = encode_defunct(primitive=Web3.solidityKeccak(['address'], [address]))
        signed_message = w3.eth.account.sign_message(message_hash, private_key=self.sk_bytes)
        return signed_message.signature.hex()
