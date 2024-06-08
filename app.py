"""A Flask web application module for serving an ice breaker interaction interface.

This module sets up a Flask web server with routes to handle requests for ice breaker interactions.
It utilizes the `ice_breaker` module to generate responses based on user input, and serves these
responses through a simple web interface.

Environment variables are loaded at the start of the module to configure necessary parameters
such as API keys or database URIs.

Routes:
    / (GET): Renders the main index page of the web application.
"""

from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv

from ice_breaker import ice_break_with

load_dotenv()

app = Flask(__name__)


@app.route("/")
def index():
    """Renders the main index page of the web application.

    Returns:
        str: The HTML content of the index page.
    """
    return render_template("index.html")


@app.route("/process", methods=["POST"])
def process():
    """Processes the user input received from the web interface, invoking the ice
    breaker logic.

    Returns:
        str: A formatted string or HTML content that includes the ice breaker's response to the
        user input.
    """
    name = request.form["name"]
    summary, profile_pic_url = ice_break_with(name=name)
    ret = jsonify(
        {
            "summary_and_facts": summary.to_dict(),
            "picture_url": profile_pic_url,
        }
    )
    return ret


if __name__ == "__main__":

    app.run(host="0.0.0.0", debug=True)
