import json
from app.data_models.text import TextModel
from tests.mock_data.constants import TEXT_DATA_MODEL_JSON, TEXT_RECORD_JSON

with open(TEXT_DATA_MODEL_JSON) as f:
    d = json.load(f)
    DATA_MODEL = TextModel.model_validate(d)

with open(TEXT_RECORD_JSON) as f:
    DB_RECORD = json.load(f)
