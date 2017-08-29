from cassandra.cqlengine import connection
from flask import make_response
from flask_restful import Resource

from conf.config import CASSANDRA_HOSTS, FRIEND_KEYSPACE
from model.friend import RequestByReceiverId
from service.common import get_user_id_from_jwt


class GetFriendRequests(Resource):
    @staticmethod
    def get():
        user_id = get_user_id_from_jwt()
        if not user_id:
            return make_response("You must send the userInfo into the header X-Endpoint-Api-Userinfo", 405)

        connection.setup(hosts=CASSANDRA_HOSTS, default_keyspace=FRIEND_KEYSPACE)

        request_list = RequestByReceiverId.filter(receiver_id=user_id)

        requests = []

        for request_row in request_list:
            requests.append(request_row.to_object())

        return {
            "tot": len(requests),
            "requests": requests
        }
