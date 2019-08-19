from flask import Blueprint, render_template, request, session, jsonify
from app.utils.json_util import *
from app.dao.KeyDao import KeyDao

big_db = Blueprint("big_db", __name__)
big_db.secret_key = 'bigChainDB'


@big_db.route('/addKeys/<string:account>', methods=['POST'])
def addKeys(account):
    keys_dao = KeyDao()
    try:
        user_id = request.args.get('user_id')
        res = keys_dao.addKeys(account, user_id)
        if res == 1:
            return json.dumps(return_success('Add success'))
        else:
            return json.dumps(return_success('Add failed'))
    except Exception as e:
        return json.dumps(return_unsuccess('Error ' + str(e)))


@big_db.route('/queryKeys/<string:account>', methods=['POST', 'GET'])
def queryKeys(account):
    keys_dao = KeyDao()
    try:
        res = keys_dao.queryKeys(account)
        if len(res) > 0:
            return json.dumps(return_success(KeyDao.to_dict(res)))
        else:
            return json.dumps(return_unsuccess('No data '))
    except Exception as e:
        return json.dumps(return_unsuccess('Error ' + str(e)))


@big_db.route('/queryPublicKey/<string:account>', methods=['POST', 'GET'])
def queryPubKey(account):
    keys_dao = KeyDao()
    try:
        res = keys_dao.query_public_key(account)
        if len(res) > 0:
            return json.dumps(return_success(KeyDao.to_dict(res)))
        else:
            return json.dumps(return_unsuccess('No data '))
    except Exception as e:
        return json.dumps(return_unsuccess('Error ' + str(e)))


@big_db.route('/queryPrivateKey/<string:account>', methods=['POST', 'GET'])
def queryPriKey(account):
    keys_dao = KeyDao()
    try:
        res = keys_dao.query_private_key(account)
        if len(res) > 0:
            return json.dumps(return_success({'privateKey': res[0][0]}))
        else:
            return json.dumps(return_unsuccess('No data '))

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
