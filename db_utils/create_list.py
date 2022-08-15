from dotenv import load_dotenv
import csv
import argparse
from .db import models, schemas, crud
from .db.database import get_db
from .key_pair import KeyPair


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


parser = argparse.ArgumentParser(
    prog="List creator",
    description="""You can use this small utility to add allowlist addresses
                                 and addresses digests to database. Input *.csv file.""",
)
parser.add_argument(
    "-db",
    "--db_url",
    help="""Database url. Example: dialect+driver://username:password@host:port/database;
    mysql+mysqlconnector://username:password@host:3306/database_name""",
    required=True,
    action="store",
    dest="db_url",
)
parser.add_argument(
    "-lf",
    "--list-file",
    help="Path to *.csv input file",
    required=True,
    action="store",
    dest="path_to_file",
)
parser.add_argument(
    "-wc",
    "--win-status-column",
    help="Specify column name with wallet win state",
    required=True,
    action="store",
    dest="status_col",
)
parser.add_argument(
    "-cn",
    "--collection-name",
    help="Collection name",
    required=True,
    action="store",
    dest="collection_name",
)
parser.add_argument(
    "-ln",
    "--list_name",
    help="List name",
    required=True,
    action="store",
    dest="list_name",
)
parser.add_argument(
    "-ltn",
    "--list-type-name",
    help="List type name",
    required=True,
    action="store",
    dest="list_type_name",
)
# parser.add_argument('-dc', '--disqualified-column',
#                     help='Specify adding rows with disqualified mark. If yes specify column name. Default false', required=False, default=False, action='store', dest='disqualified_col', type=bool)
parser.add_argument(
    "-k",
    "--signing-key-filepath",
    help="Signing key file path",
    required=True,
    default=False,
    action="store",
    dest="pem_key_path",
)
args = parser.parse_args()


column_names, rows = parse_file(args.path_to_file)
keypair = KeyPair()
db = next(get_db(args.db_url))


print("Resolving collection... ", end="")
db_collection = crud.get_collection(db, args.collection_name)
if not db_collection:
    db_collection = crud.create_collection(
        db, schemas.CollectionCreate(name=args.collection_name)
    )
print("Success!")

print("Resolving list type... ", end="")
db_access_list_type = crud.get_access_list_type_by_name(db, args.list_type_name)
if not db_access_list_type:
    db_access_list_type = crud.create_access_list_type(
        db, schemas.AccessListTypeCreate(name=args.list_type_name)
    )
print("Success!")


print("Resolving list... ", end="")
db_access_list = crud.get_access_list_by_name_and_collection_name(
    db, args.list_name, args.collection_name
)
if not db_access_list:
    db_access_list = crud.create_access_list(
        db,
        schemas.AccessListCreate(
            name=args.list_name,
            collection_id=db_collection.id,
            list_type_id=db_access_list_type.id,
            signing_pk=keypair.get_public_key(),
        ),
    )
print("Success!")


for row in rows:
    if row["winner"].capitalize() == "True":
        address = row["wallet_address"]
        db_wallet = crud.get_wallet(db, address=address)
        if not db_wallet:
            db_wallet = crud.create_wallet(db, schemas.WalletCreate(address=address))
        signed_address = keypair.sk.sign_recoverable(address.encode("utf-8")).hex()

        db_access_list_item = crud.get_access_list_item(
            db,
            address=address,
            list_id=db_access_list.id,
        )
        if not db_access_list_item:
            db_access_list_item = crud.create_access_list_item(
                db,
                schemas.AccessListItemCreate(
                    wallet_id=db_wallet.id,
                    list_id=db_access_list.id,
                    signed_address=signed_address,
                ),
            )
        print(db_access_list_item)

keypair.save_pem(args.pem_key_path)
