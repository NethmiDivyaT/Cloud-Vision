from flask import Flask, request, render_template
from google.cloud import vision
from google.cloud import storage
import os

app = Flask(__name__, template_folder="templates")


@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("main.html")


@app.route("/display", methods=["GET", "POST"])
def speech():

    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "auth.json"

    bucket_name = "lively-metrics-337209.appspot.com"
    storage_client = storage.Client()
    blobs = storage_client.list_blobs(bucket_name)

    client = vision.ImageAnnotatorClient()

    dog = []
    cat = []

    for blob in blobs:

        image_file = f'gs://lively-metrics-337209.appspot.com/{blob.name}'

        objects = client.object_localization(
            {
                "source": {
                    "image_uri": image_file
                },
            }
        ).localized_object_annotations

        for object_ in objects:

            if str(object_.name) == 'dog' or str(object_.name) == 'Dog' or str(object_.name) == 'DOG':
                dog.append(blob.name)

            if str(object_.name) == 'cat' or str(object_.name) == 'Cat' or str(object_.name) == 'CAT':
                cat.append(blob.name)

    return render_template("main.html", cat=cat, dog=dog)


if __name__ == "__main__":
    app.run(debug=True, threaded=True)
