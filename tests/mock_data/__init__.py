import json
from pathlib import Path
from app.data_models.text import TextModel

MOCK_DATA_DIR = Path(__file__).parent

TEXT_DATA_MODEL_JSON = MOCK_DATA_DIR.joinpath("text_data_model.json")
TEXT_RECORD_JSON = MOCK_DATA_DIR.joinpath("text_record.json")


with open(TEXT_DATA_MODEL_JSON) as f:
    d = json.load(f)
    DATA_MODEL_TEXT = TextModel.model_validate(d)

with open(TEXT_RECORD_JSON) as f:
    RECORD_TEXT = json.load(f)
