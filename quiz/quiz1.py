from flask import Flask
from threading import Thread
import logging
import os
from contextlib import redirect_stdout, redirect_stderr

app = Flask(__name__)

@app.route("/")
def home():
    return "Hello from quiz1!"

def run_server(host="127.0.0.1", port=5000):
    url = f"http://{host}:{port}"

    logging.getLogger("werkzeug").disabled = True
    app.logger.disabled = True

    def run_app():
        with open(os.devnull, "w") as devnull:
            with redirect_stdout(devnull), redirect_stderr(devnull):
                app.run(
                    host=host,
                    port=port,
                    debug=False,
                    use_reloader=False
                )

    thread = Thread(target=run_app, daemon=True)
    thread.start()

    return url