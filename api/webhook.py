import os

from flask import Flask, Blueprint, request, jsonify
from telegram import Bot, Update

from helpers.bot import get_update_queue


app = Flask(__name__)
api = Blueprint("serverless_handler", __name__)
bot = Bot(os.environ["BOT_TOKEN"])
app.config["tg_bot"] = bot
app.config["update_queue"] = get_update_queue(bot)


@api.route("/", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), app.config["tg_bot"])
    app.config["update_queue"].put(update)
    return jsonify({"status": "ok"})


@api.route("/")
def home():
    return "Hello, World!"


app.register_blueprint(api, url_prefix="/api/webhook")
