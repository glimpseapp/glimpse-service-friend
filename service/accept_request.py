from cassandra.cqlengine import connection
from flask import request, make_response
from flask_restful import Resource

from conf.config import CASSANDRA_HOSTS, FRIEND_KEYSPACE
from model.friend import RequestBySenderId, RequestByReceiverId, FriendRelation
from service.common import get_user_id_from_jwt


class AcceptRequest(Resource):
    @staticmethod
    def post():
        user_id = get_user_id_from_jwt()
        if not user_id:
            return make_response("You must send the userInfo into the header X-Endpoint-Api-Userinfo", 405)

        data = request.get_json(silent=True)
        request_id = data.get("request_id")
        if not request_id:
            return make_response("You must specify the request_id parameter", 405)

        connection.setup(hosts=CASSANDRA_HOSTS, default_keyspace=FRIEND_KEYSPACE)

        friend_request_object = RequestByReceiverId.filter(receiver_id=user_id, request_id=request_id)
        if not friend_request_object:
            return make_response("Request not found", 404)

        friend_request = friend_request_object.get().to_object()

        if friend_request:
            friend_id = friend_request.get("sender_id")

        # create new friend relation
        FriendRelation.create(
            user_id=user_id,
            friend_id=friend_id
        )

        FriendRelation.create(
            user_id=friend_id,
            friend_id=user_id
        )

        # delete friend request
        RequestByReceiverId.get(receiver_id=user_id, request_id=request_id).delete()
        RequestBySenderId.get(sender_id=friend_id, request_id=request_id).delete()

        return {
            "status": True
        }
