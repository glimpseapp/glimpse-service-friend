import uuid

from cassandra.cqlengine import connection
from flask import request, make_response
from flask_restful import Resource

from conf.config import CASSANDRA_HOSTS, FRIEND_KEYSPACE
from model.friend import RequestBySenderId, RequestByReceiverId
from service.common import get_user_id_from_jwt


class SendFriendRequest(Resource):
    @staticmethod
    def post():
        user_id = get_user_id_from_jwt()
        if not user_id:
            return make_response("You must send the userInfo into the header X-Endpoint-Api-Userinfo", 405)

        data = request.get_json(silent=True)
        request_id = str(uuid.uuid4())
        receiver_id = data.get('receiver_id')
        if not receiver_id:
            return make_response("You must specify the receiver_id parameter", 405)

        connection.setup(hosts=CASSANDRA_HOSTS, default_keyspace=FRIEND_KEYSPACE)

        RequestBySenderId.create(
            sender_id=user_id,
            receiver_id=receiver_id,
            request_id=request_id
        )

        RequestByReceiverId.create(
            sender_id=user_id,
            receiver_id=receiver_id,
            request_id=request_id
        )
        return {"request_id": request_id}
