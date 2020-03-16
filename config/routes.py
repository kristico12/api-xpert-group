# dependencies
from flask import Blueprint

# import controllers
from controllers.conversation_history import conversation_history
from controllers.qualification import qualification

routes = Blueprint('routes', __name__)


@routes.route("/api/conversation_history", methods=['POST'])
def index():
    return conversation_history()


@routes.route("/api/qualification", methods=['GET'])
def index1():
    return qualification()
