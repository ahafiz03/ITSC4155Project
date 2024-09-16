from flask import Flask
app = Flask(__name__)

@app.route("/")
def main():
    return "Welcome!"

if __name__ == "_main_":
    app.run()