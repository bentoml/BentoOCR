from __future__ import annotations

import typing
import pathlib
import bentoml
import numpy

Image = typing.Annotated[pathlib.Path, bentoml.validators.ContentType('image/*')]

with bentoml.importing():
    import easyocr


@bentoml.service(
    resources={'gpu': 1}, image=bentoml.images.PythonImage(python_version='3.11').requirements_file('requirements.txt')
)
class OCRService:
    models = bentoml.models.BentoModel('easyocr--ch-en')

    def __init__(self):
        self.reader = easyocr.Reader(
            ['ch_sim', 'en'], model_storage_directory=self.models.path, download_enabled=False, gpu=True
        )

    @bentoml.api()
    def detect(self, image: Image) -> list[dict]:
        detections = self.reader.readtext(str(image))
        return [{'text': text, 'bbox': numpy.array(bbox).tolist()} for (bbox, text, _) in detections]

    @bentoml.api()
    def classify(self, image: Image) -> list[dict]:
        detections = self.reader.readtext(str(image))
        return [{'text': text, 'confidence': confidence} for (_, text, confidence) in detections]
