from flask import Flask, render_template, render_template_string, request

app = Flask(__name__)


@app.route("/debug")
def debug():
    if request.headers.get("X-Forwarded-For") != "127.0.0.1":
        return "Access Denied", 403

    params = request.args.to_dict()
    if not params:
        return render_template("debug.html")

    forbidden_chars = ["<", ">", '"', "'", "[", "]"]

    for key, value in params.items():
        for char in forbidden_chars:
            if char in value:
                return "Forbidden character used!", 400

    reflected_output = ""
    for key, value in params.items():
        reflected_output += f"{key} = {value}<br>"

    try:
        rendered_output = render_template_string(reflected_output)
        return rendered_output
    except Exception:
        return "Template Error", 500


@app.route("/")
def index():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=1337)
