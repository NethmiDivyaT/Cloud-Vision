from google.cloud import vision
from flask import render_template, Flask, request
import os

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('main.html')


@app.route('/display',  methods=['GET', 'POST'])
def display():

    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "auth.json"

    # Imports the Google Cloud client library
    from google.cloud import vision

    # Instantiates a client
    client = vision.ImageAnnotatorClient()

    # Performs label detection on the image file
    response = client.label_detection(
        {
            "source": {
                "image_uri": "gs://lively-metrics-337209.appspot.com/humans-2.jpeg"
            },
        }
    )
    labels = response.label_annotations

    allDescreiptios = []

    for label in labels:
        allDescreiptios.append(
            {label.description: str(round(label.score * 100, 2))})

    return render_template("main.html", transcript=allDescreiptios)


if __name__ == "__main__":
    app.run(debug=True, threaded=True)
