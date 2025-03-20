from pathlib import Path

import yaml

cwd = Path(__file__).parent.parent
config_file = cwd.joinpath("config.yml")
with open(config_file, mode="r") as f:
    config = yaml.safe_load(f)

CONTRIBUTORS = config["contributors"]
DB_PATH = config["file paths"]["database"]
OUTDIR_PATH = config["file paths"]["output directory"]
TEXT_TEI_MODEL = config["file paths"]["text TEI model"]
