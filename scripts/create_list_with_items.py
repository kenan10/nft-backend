import os
from dotenv import load_dotenv
import csv
import argparse
from coincurve.keys import PrivateKey, PublicKey
from app.db import models, schemas, crud
from app.dependencies import get_db
from hashlib import sha3_256


class KeyPair(object):
    def __init__(self) -> None:
        self.sk = PrivateKey()
        self.pk = self.sk.public_key

    def from_pem(self, pem):
        self.sk = PrivateKey.from_pem(pem)
        self.pk = self.sk.public_key

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
        return '0x' + sha3_256(self.pk.format(False)[1:]).hexdigest()[-40:]


def parse_file(path_to_file):
    rows = []
    columns = None
    with open(path_to_file) as csv_file:
        csv_reader = csv.DictReader(csv_file)
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                columns = row
                line_count += 1
            rows.append(row)
            line_count += 1
    return columns, rows

# 0xbc67d98834f0825fd33e4829eacf8357101fd2e0
# 0x16A765B12F9f364aed12F836dA9ae42DB10B2d88

# b35825d96a211f9356ac29bf56cabd2432a2741441adb6278bdee97870e076a8
# efb94e54aec99e6cd750c9a1b5966b4ba6b72179639fa056bcf8958766030f17


parser = argparse.ArgumentParser(prog='List creator', description="""You can use this small utility to add allowlist addresses
                                 and addresses digests to database. Input *.csv file.""")
parser.add_argument('-lf', '--list-file',
                    help='Path to *.csv input file', required=True, action='store', dest='path_to_file')
parser.add_argument('-wc', '--win-status-column',
                    help='Specify column name with wallet win state', required=True, action='store', dest='status_col')
parser.add_argument('-cn', '--collection-name', help='Collection name',
                    required=True, action='store', dest='collection_name')
parser.add_argument('-ln', '--list_name', help='List name',
                    required=True, action='store', dest='list_name')
parser.add_argument('-ltn', '--list-type-name',
                    help='List type name', required=True, action='store', dest='list_type_name')
# parser.add_argument('-dc', '--disqualified-column',
#                     help='Specify adding rows with disqualified mark. If yes specify column name. Default false', required=False, default=False, action='store', dest='disqualified_col', type=bool)
parser.add_argument('-k', '--signing-key-filepath',
                    help='Signing key file path', required=True, default=False, action='store', dest='pem_key_path')
args = parser.parse_args()


column_names, rows = parse_file(args.path_to_file)
keypair = KeyPair()
db = next(get_db())


print("Resolving collection... ", end="")
db_collection = crud.get_collection(db, args.collection_name)
if not db_collection:
    db_collection = crud.create_collection(
        db, schemas.CollectionCreate(name=args.collection_name))
print("Success!")

print("Resolving list type... ", end="")
db_access_list_type = crud.get_access_list_type_by_name(
    db, args.list_type_name)
if not db_access_list_type:
    db_access_list_type = crud.create_access_list_type(
        db, schemas.AccessListTypeCreate(name=args.list_type_name))
print("Success!")


print("Resolving list... ", end="")
db_access_list = crud.get_access_list_by_name_and_collection_name(
    db, args.list_name, args.collection_name)
if not db_access_list:
    db_access_list = crud.create_access_list(
        db, schemas.AccessListCreate(name=args.list_name,
                                     collection_id=db_collection.id,
                                     list_type_id=db_access_list_type.id,
                                     signing_pk=keypair.get_public_key()))
print("Success!")


for row in rows:
    if row["winner"].capitalize() == "True":
        address = row["wallet_address"]
        db_wallet = crud.get_wallet(db, address=address)
        if not db_wallet:
            db_wallet = crud.create_wallet(db,
                                           schemas.WalletCreate(address=address))
        signed_address = keypair.sk.sign_recoverable(address.encode("utf-8")).hex()
        print(signed_address)
