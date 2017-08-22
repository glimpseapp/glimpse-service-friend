from flask import Flask
from flask_restful import Api

from conf.config import HTTP_HOST, HTTP_PORT
from service.accept_request import AcceptRequest
from service.healthz import Healthz
from service.get_friend_requests import GetFriendRequests
from service.reject_request import RejectRequest
from service.send_friend_request import SendFriendRequest

app = Flask(__name__)
api = Api(app)

api.add_resource(Healthz, '/healthz')
api.add_resource(SendFriendRequest, '/request')
api.add_resource(GetFriendRequests, '/requests')
api.add_resource(AcceptRequest, '/request/accept')
api.add_resource(RejectRequest, '/request/reject')

if __name__ == '__main__':
    app.run(host=HTTP_HOST, port=HTTP_PORT)
