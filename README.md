<div align="center">
    <h1 align="center">Turning OCR Models into Inference APIs with BentoML</h1>
</div>

This is a BentoML example project that demonstrates how to serve an OCR model. It accepts images as input and returns the text contained within. While the example uses [EasyOCR](https://github.com/JaidedAI/EasyOCR), you can choose any other OCR model.

See [here](https://docs.bentoml.com/en/latest/examples/overview.html) for a full list of BentoML example projects.

## Install dependencies

1. Make sure to install [uv](https://docs.astral.sh/uv/).
2. Clone the repo and install dependencies.

   ```bash
   git clone https://github.com/bentoml/BentoOCR.git && cd BentoOCR

   # Recommend Python 3.11
   pip install -r requirements.txt
   ```

## Save the model

Import the model into the [BentoML Model Store](https://docs.bentoml.com/en/latest/build-with-bentoml/model-loading-and-management.html).

```bash
python import_model.py
```

## Run the BentoML Service

We have defined a BentoML Service in `service.py` to serve the model. To start it, run:

```bash
bentoml serve
```

The server is now active at [http://localhost:3000](http://localhost:3000/). It exposes two API endpoints:

- `detect`: Takes an image as input and returns a list of detected text regions. Each detection includes the extracted text and the bounding box coordinates of where the text was found in the image.
- `classify`: Takes an image as input and returns a list with the extracted text and the confidence score for each text detection.

You can call these endpoints using the Swagger UI or in other different ways.

### cURL

```bash
curl -X 'POST' \
  'http://localhost:3000/detect' \
  -H 'accept: application/json' \
  -H 'Content-Type: multipart/form-data' \
  -F 'image=@sample-image.png;type=image/png'
```

### Python client

```python
import bentoml
from pathlib import Path

with bentoml.SyncHTTPClient("http://localhost:3000/") as client:
    result = client.detect(
        image=Path("image.jpg"),
    )
```

## Deploy to BentoCloud

After the Service is ready, you can deploy the application to BentoCloud for better management and scalability. [Sign up](https://www.bentoml.com/) if you haven't got a BentoCloud account.

Make sure you have [logged in to BentoCloud](https://docs.bentoml.com/en/latest/scale-with-bentocloud/manage-api-tokens.html).

```bash
bentoml cloud login
```

Deploy it to BentoCloud:

```bash
bentoml deploy
```

Once the application is up and running on BentoCloud, you can access it via the exposed URL.

## Community

BentoML has a thriving open source community where thousands of ML/AI practitioners are contributing to the project, helping other users and discussing the future of AI. 👉 [Pop into our Slack community!](https://l.bentoml.com/join-slack)
