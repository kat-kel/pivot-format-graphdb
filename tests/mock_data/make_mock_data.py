import json
from datetime import datetime

from app.database import DBConn
from tests.mock_data.constants import TEXT_RECORD_JSON, TEXT_DATA_MODEL_JSON


# Mock text data
MOCK_TEXT_ID = 47788


def make_text(db: DBConn):
    from app.data_models.text import TextModel

    # Select real data from the database
    example_data = db.get_by_id(table="TextTable", hid=MOCK_TEXT_ID)

    # Save the record's metadata to a JSON file
    with open(TEXT_RECORD_JSON, "w") as f:
        json_obj = {}
        for k, v in example_data.items():
            # Serialize list of dates to list of strings
            if isinstance(v, list) and len(v) > 0 and isinstance(v[0], datetime):
                v = [str(i) for i in v]
            json_obj.update({k: v})
        json.dump(json_obj, f, indent=4)

    # Validate the real data in the data model
    nested_dict = TextModel.build_nested_dict(row_dict=example_data, db=db)
    data_model = TextModel.model_validate(nested_dict)

    # Serialize the data model to JSON and write it into a file
    with open(TEXT_DATA_MODEL_JSON, "w") as f:
        json_str = data_model.model_dump_json(by_alias=True, indent=4)
        f.write(json_str)


if __name__ == "__main__":
    db = DBConn()
    make_text(db=db)
