from flask import Flask, render_template, request, make_response
from random import randint

app = Flask(__name__)


@app.route("/", methods=["GET"])
def index():
    existing_secret = request.cookies.get("secret")
    response = make_response(render_template("game.html"))

    if not existing_secret:
        secret = randint(1, 10)
        response.set_cookie("secret", str(secret))
        response.set_cookie("attempts", "0")

    return response


@app.route("/result", methods=["POST"])
def result():
    guess = int(request.form.get("guess"))
    secret = int(request.cookies.get("secret"))
    attempts = int(request.cookies.get("attempts"))
    attempts += 1

    if guess == secret:
        result = "correct"

        response = make_response(render_template("result.html", result=result, attempts=attempts))

        secret = randint(1, 10)
        response.set_cookie("secret", str(secret))
        response.set_cookie("attempts", "0")
        return response

    elif guess < secret:
        result = "too SMALL"
    elif guess > secret:
        result = "too BIG"

    response = make_response(render_template("result.html", result=result, attempts=attempts))
    response.set_cookie("attempts", str(attempts))

    return response


if __name__ == "__main__":
    app.run()
