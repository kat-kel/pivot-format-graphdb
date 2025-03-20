# Mock data

Some unit tests require modelled data from LostMa's Heurist database.

Rather than work with data directly from the database, which might change and must be stored in a binary (not human-readable) format, we have serialized data from the database in JSON files in this directory.

Use the [`make_mock_data.py`](./make_mock_data.py) module to select real data from the database, validate it in a data model, and serialize it into a JSON file.


```shell
$ python tests/mock_data/make_mock_data.py
```

Finally, in this directory's [`__init__.py`](./__init__.py) module, parse the JSON file and make it available for importing in the test modules.

```python
from pathlib import Path
import json

MOCK_DATA_DIR = Path(__file__).parent
TEXT_JSON_FILE = MOCK_DATA_DIR.joinpath("text_data_model.json")

with open(TEXT_JSON_FILE) as f:
    MOCK_TEXT_DATA = json.load(f)
```
