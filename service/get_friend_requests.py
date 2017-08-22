from cassandra.cqlengine import connection
from flask import request
from flask_restful import Resource

from conf.config import CASSANDRA_HOSTS, USER_KEYSPACE
from model.friend import RequestByReceiverId


class GetFriendRequests(Resource):
    def post(self):
        data = request.get_json(silent=True)

        connection.setup(hosts=CASSANDRA_HOSTS, default_keyspace=USER_KEYSPACE)

        user_id = data.get("user_id")

        request_list = RequestByReceiverId.filter(receiver_id=user_id)

        requests = []

        for request_row in request_list:
            requests.append(request_row.to_object())

        return {
            "tot": len(requests),
            "requests": requests
        }