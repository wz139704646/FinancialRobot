import bigchaindb_driver.crypto
# !!!要安装bigchaindb_driver必须先安装pywin32
from collections import namedtuple
from bigchaindb_driver import BigchainDB
from app.config import BIGCHAINDB_URL
import time

# BIGCHAINDB_URL = "http://47.100.244.29:9984"

class BigchainUtils(object):


    @staticmethod
    def gen_random_keypair():
        return bigchaindb_driver.crypto.generate_keypair()

    @staticmethod
    def gen_keypair(private_key, public_key):
        pair = namedtuple('CryptoKeypair', ('private_key', 'public_key'))
        return pair(private_key=private_key, public_key=public_key)

    @staticmethod
    def get_keypair(kid):
        pair = namedtuple('CryptoKeypair', ('private_key', 'public_key'))
        if kid == "scrap":
            private_key = '3zGAqReYyv7rwLx9CRY5yZCrvfZMFxtPaRGnitPFaC5P'
            public_key = 'APAbwxtxbmH3HNPtsVnDdyqQrMDHXMTfi1Mbn7EnYDyW'
            return pair(private_key=private_key, public_key=public_key)
        private_key = 'GMUvYtpYrdj6JWqv2DcMHucTUmu96UvKAWzBYBowK7gg'
        public_key = '2BkCkcZKoP4tQcRfbvRku7wDHgPPHYjaR1fys9NrR8Gg'
        return pair(private_key=private_key, public_key=public_key)


    def __init__(self):
        self.conn = BigchainDB(BIGCHAINDB_URL)

    def search_asset(self,keyword,limit=0):
        return self.conn.assets.get(search=keyword,limit=limit)

    def search_transactions(self,asset_id,operation="CREATE"):
        return self.conn.transactions.get(asset_id=asset_id,operation=operation)



    def create_asset(self, signer, asset, metadata=None):
        # Prepare transaction
        prep_tx = self.conn.transactions.prepare(operation="CREATE",
                                                 signers=signer.public_key,
                                                 asset={"data":asset},
                                                 metadata=metadata)
        # Sign transaction
        signed_tx = self.conn.transactions.fulfill(prep_tx, signer.private_key)
        # Send transaction
        send_tx = self.conn.transactions.send_commit(signed_tx)
        # Verify and return txid if successful
        if send_tx == signed_tx:
            return signed_tx["id"]
        else:
            return False

    def send_asset(self, txid, signer, recipient, metadata=None):
        # Find previous transaction
        prev_tx = self.conn.transactions.retrieve(txid)
        # prepare transfer transaction
        prepared_transfer_tx = self._craft_tx(prev_tx, recipient.public_key,metadata=metadata)
        # Fulfill transfer transaction
        fulfilled_transfer_tx = self.conn.transactions.fulfill(
            prepared_transfer_tx,
            private_keys=signer.private_key,
        )
        sent_transfer_tx = self.conn.transactions.send_commit(fulfilled_transfer_tx)
        return sent_transfer_tx["id"]

    def check_transaction(self, txid):
        try:
            status = self.conn.transactions.status(txid)
            return status
        except Exception as e:
            print(e)
            return None

    def get_transaction(self, txid):
        return self.conn.transactions.retrieve(txid)

    def check_status(self, txid):
        return self.conn.transactions.status(txid)

    def get_utxos(self, public_key):
        utxos = self.conn.outputs.get(public_key=public_key)
        return [utxo.split('/')[2] for utxo in utxos]

    def _craft_tx(self, prev_tx, recipient_pub_key,metadata):

        transfer_asset = {"id": None}
        if prev_tx["operation"] == "CREATE":
            transfer_asset["id"] = prev_tx["id"]
        elif prev_tx["operation"] == "TRANSFER":
            transfer_asset["id"] = prev_tx['asset']['id']

        output_index = 0
        output = prev_tx['outputs'][output_index]

        transfer_input = {
            'fulfillment': output['condition']['details'],
            'fulfills': {
                'output_index': output_index,
                'transaction_id': prev_tx['id'],
                'detail': metadata,
                'timestamp': int(time.time())
            },
            'owners_before': output['public_keys'],
        }
        return self.conn.transactions.prepare(operation="TRANSFER",
                                              asset=transfer_asset,
                                              inputs=transfer_input,
                                              recipients=recipient_pub_key,
                                              metadata=metadata)