from cassandra.cqlengine import connection
from flask import request
from flask_restful import Resource

from conf.config import CASSANDRA_HOSTS, FRIEND_KEYSPACE
from model.friend import RequestBySenderId, RequestByReceiverId


class RejectRequest(Resource):
    def post(self):
        data = request.get_json(silent=True)

        user_id = data.get("user_id")
        request_id = data.get("request_id")

        connection.setup(hosts=CASSANDRA_HOSTS, default_keyspace=FRIEND_KEYSPACE)

        friend_request_object = RequestByReceiverId.get(receiver_id=user_id, request_id=request_id).to_object()

        if friend_request_object:
            friend_id = friend_request_object.get("sender_id")

        # delete friend request
        RequestByReceiverId.get(receiver_id=user_id, request_id=request_id).delete()
        RequestBySenderId.get(sender_id=friend_id, request_id=request_id).delete()

        return {
            "status": True
        }
