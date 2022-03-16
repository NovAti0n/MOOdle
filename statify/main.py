from flask import Flask, render_template

app = Flask(
    __name__,
    template_folder="../public/templates/",
    static_folder="../public/static",
    static_url_path="",
)


@app.route("/")
def index():
    name = None
    return render_template("index.html", name=name)
