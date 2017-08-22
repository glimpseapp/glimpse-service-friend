import uuid

from cassandra.cqlengine import connection
from cassandra.cqlengine.query import LWTException
from flask import make_response, request
from flask_restful import Resource

from conf.config import CASSANDRA_HOSTS, USER_KEYSPACE
from model.friend import RequestBySenderId, RequestByReceiverId


class SendFriendRequest(Resource):
    def post(self):
        data = request.get_json(silent=True)

        connection.setup(hosts=CASSANDRA_HOSTS, default_keyspace=USER_KEYSPACE)

        request_id = str(uuid.uuid4())

        RequestBySenderId.create(
            sender_id=data.get('user_id'),
            receiver_id=data.get('receiver_id'),
            request_id=request_id
        )

        RequestByReceiverId.create(
            sender_id=data.get('user_id'),
            receiver_id=data.get('receiver_id'),
            request_id=request_id
        )
        return {"request_id": request_id}


