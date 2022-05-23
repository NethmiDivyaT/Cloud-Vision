from fileinput import filename
from flask import Flask, request, render_template
from google.cloud import vision
from google.cloud import storage
import os
import sys


app = Flask(__name__, template_folder="templates")


@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("main.html")


@app.route("/display", methods=["GET", "POST"])
def uploadimg():

    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "auth.json"

    # bucket_name = "lively-metrics-337209.appspot.com"

    filename = request.files['filename']

    """Uploads a file to the bucket."""
    # The ID of your GCS bucket
    bucket_name = "lively-metrics-337209.appspot.com"

    # The path to your filively-metrics-337209.appspot.comle to upload
    destination_blob_name = "%s/%s" % ('', filename.filename)

    # The ID of your GCS object
    source_file_name = 'gs://lively-metrics-337209.appspot.com/' + filename.filename

    # data = Image.open(os.path.join(folder, file),'r'))

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_file(filename, filename.content_type)

    print(
        f"File {source_file_name} uploaded to {destination_blob_name}."
    )

    imgurl = "gs://lively-metrics-337209.appspot.com//" + filename.filename

    object = []
    client = vision.ImageAnnotatorClient()
    image = vision.Image()
    image.source.image_uri = source_file_name

    response = client.web_detection(image=image)
    annotations = response.web_detection

    if annotations.pages_with_matching_images:

        for page in annotations.pages_with_matching_images:
            for page in annotations.pages_with_matching_images:
                if page.full_matching_images:
                    object.append(format(page.url))

    return render_template('main.html', object=object)


if __name__ == "__main__":
    app.run(debug=True, threaded=True)
