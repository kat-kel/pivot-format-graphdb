from pathlib import Path
import yaml

cwd = Path(__file__).parent.parent
config_file = cwd.joinpath("config.yml")
with open(config_file, mode="r") as f:
    config = yaml.safe_load(f)

CONTRIBUTORS = config["contributors"]
HEURIST_DB = config["file paths"]["heurist database"]
KUZU_DB = config["file paths"]["graph database"]
OUTDIR_PATH = config["file paths"]["output directory"]

# text_tree_model_filepath
text_tree_model_filepath = config["file paths"]["text TEI model"]

TEXT_TEI_MODEL = cwd.joinpath(text_tree_model_filepath)

if not TEXT_TEI_MODEL.is_file():
    raise FileNotFoundError(TEXT_TEI_MODEL)
