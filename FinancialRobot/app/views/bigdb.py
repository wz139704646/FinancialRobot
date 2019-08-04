from flask import Blueprint, render_template, request, session, jsonify
from app.utils.json_util import *
from app.dao.KeyDao import KeyDao

big_db = Blueprint("big_db", __name__)
big_db.secret_key = 'bigChainDB'


@big_db.route('/addKeys/<string:id>', methods=['POST'])
def addKeys(id):
    keys_dao = KeyDao()
    try:
        keys_dao.addKeys(id)
        return json.dumps(return_success('ok'))
    except Exception as e:
        return json.dumps(return_unsuccess('Error ' + str(e)))


@big_db.route('/queryKeys/<string:id>', methods=['POST'])
def queryKeys(id):
    keys_dao = KeyDao()
    try:
        res = keys_dao.queryKeys(id)
        return json.dumps(return_success(KeyDao.to_dict(res)))
    except Exception as e:
        return json.dumps(return_unsuccess('Error ' + str(e)))


@big_db.route('/queryPublicKey/<string:id>', methods=['POST'])
def queryPubKeys(id):
    keys_dao = KeyDao()
    try:
        res = keys_dao.query_public_key(id)
        return json.dumps(return_success({'publicKey': res[0][0]}))
    except Exception as e:
        return json.dumps(return_unsuccess('Error ' + str(e)))


@big_db.route('/queryPrivateKey/<string:id>', methods=['POST'])
def queryPriKeys(id):
    keys_dao = KeyDao()
    try:
        res = keys_dao.query_private_key(id)
        return json.dumps(return_success({'privateKey': res[0][0]}))
    except Exception as e:
        return json.dumps(return_unsuccess('Error ' + str(e)))

# bdb = BigchainDB('https://test.bigchaindb.com')
# alice = generate_keypair()
# tx = bdb.transactions.prepare(
#     operation='CREATE',
#     signers=alice.public_key,
#     asset={'data': {'message': 'Blockchain all the things!'}})
# signed_tx = bdb.transactions.fulfill(
#     tx,
#     private_keys=alice.private_key)
# bdb.transactions.send_commit(signed_tx)
