import time
from cassandra.cqlengine import columns
from cassandra.cqlengine.models import Model
from cassandra.util import datetime_from_timestamp


def date_now():
    return datetime_from_timestamp(time.time())


class FriendRelation(Model):
    user_id = columns.Text(primary_key=True)
    friend_id = columns.Text()
    friend_since = columns.DateTime(default=date_now)

    def to_object(self):
        return {
            'user_id': str(self.user_id),
            'friend_id': self.friend_id,
            'friend_since': self.friend_since.isoformat(),
        }


class RequestBySenderId(Model):
    sender_id = columns.Text(primary_key=True)
    request_id = columns.Text()
    receiver_id = columns.Text()

    def to_object(self):
        return {
            'sender_id': self.sender_id,
            'request_id': self.request_id,
            'receiver_id': self.receiver_id,
        }


class RequestByReceiverId(Model):
    receiver_id = columns.Text(primary_key=True)
    request_id = columns.Text()
    sender_id = columns.Text()

    def to_object(self):
        return {
            'receiver_id': self.receiver_id,
            'request_id': self.request_id,
            'sender_id': self.sender_id,
        }
