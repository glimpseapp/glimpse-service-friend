from cassandra.cqlengine import connection
from flask_restful import Resource

from conf.config import CASSANDRA_HOSTS, FRIEND_KEYSPACE
from model.friend import FriendRelation


class GetFriendList(Resource):
    def get(self, user_id):
        connection.setup(hosts=CASSANDRA_HOSTS, default_keyspace=FRIEND_KEYSPACE)

        friend_rows = FriendRelation.filter(user_id=user_id)

        friends = []

        for friend_row in friend_rows:
            friends.append(friend_row.to_object())

        return {
            "tot": len(friends),
            "friends": friends
        }
