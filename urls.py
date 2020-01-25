from screen_capture.views import ShowViewScreen, StartServer, StartClient
from flask import Blueprint
screen_share = Blueprint('screen_share', __name__)
screen_share.add_url_rule("/", view_func=ShowViewScreen.as_view('broadcast_server'))
screen_share.add_url_rule("/start_server",
                 view_func=StartServer.as_view('view_screen'), methods=["GET"])
screen_share.add_url_rule("/start_client",
                 view_func=StartClient.as_view('start_client'), methods=["GET"])