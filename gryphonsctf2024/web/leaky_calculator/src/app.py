from flask import Flask, render_template, request

app = Flask(__name__)
flag = open("flag.txt").read()


@app.route("/", methods=["GET", "POST"])
def index():
    result = ""
    if request.method == "POST":
        expression = request.form.get("expression")
        if expression:
            try:
                result = str(eval(expression))
            except Exception as e:
                result = "Error: " + str(e)
    return render_template("index.html", result=result)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=1337)
