import base64
import json

import requests
from cassandra.cqlengine import connection
from flask import make_response
from flask_restful import Resource

from conf.config import CASSANDRA_HOSTS, FRIEND_KEYSPACE
from conf.service import USER_INFO_BULK_URL
from model.friend import FriendRelation
from service.common import get_user_id_from_jwt


class GetFriendList(Resource):
    def get(self):
        user_id = get_user_id_from_jwt()
        if not user_id:
            return make_response("You must send the userInfo into the header X-Endpoint-Api-Userinfo", 405)

        connection.setup(hosts=CASSANDRA_HOSTS, default_keyspace=FRIEND_KEYSPACE)

        friend_rows = FriendRelation.filter(user_id=user_id)

        friends = {}
        friend_ids = []

        for friend_row in friend_rows:
            friend = friend_row.to_object()
            friend_id = friend['user_id']
            friends[friend_id] = friend
            friend_ids.append(friend_id)

        user_info_list = self._get_user_info_bulk(friend_ids)

        for user in user_info_list:
            user_id = user['user_id']
            friends[user_id]['username'] = user['username']

        return {
            "results": len(friends),
            "friends": friends
        }

    @staticmethod
    def _get_user_info_bulk(user_ids):
        payload = json.dumps({"user_ids": user_ids})
        headers = {'Content-Type': 'application/json'}
        response = requests.post(USER_INFO_BULK_URL, data=payload, headers=headers)
        data = response.json()
        return data.get("users")
