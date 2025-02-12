import bentoml
import easyocr

if __name__ == '__main__':
    with bentoml.models.create('easyocr--ch-en') as bentomodel_ref:
        reader = easyocr.Reader(['ch_sim', 'en'], model_storage_directory=bentomodel_ref.path_of('/'))
