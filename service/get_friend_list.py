from cassandra.cqlengine import connection
from flask import make_response
from flask_restful import Resource

from conf.config import CASSANDRA_HOSTS, FRIEND_KEYSPACE
from model.friend import FriendRelation
from service.common import get_user_id_from_jwt


class GetFriendList(Resource):
    @staticmethod
    def get():
        user_id = get_user_id_from_jwt()
        if not user_id:
            return make_response("You must send the userInfo into the header X-Endpoint-Api-Userinfo", 405)

        connection.setup(hosts=CASSANDRA_HOSTS, default_keyspace=FRIEND_KEYSPACE)

        friend_rows = FriendRelation.filter(user_id=user_id)

        friends = []

        for friend_row in friend_rows:
            friends.append(friend_row.to_object())

        return {
            "tot": len(friends),
            "friends": friends
        }
