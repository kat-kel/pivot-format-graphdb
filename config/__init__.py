from pathlib import Path
import yaml
import os
from dotenv import load_dotenv, find_dotenv

# Establish the root of this config folder
root = Path(__file__).parent

# Create a Path object pointing to the YAML file
contributor_yaml_file = root.joinpath("contributors.yml")

# Read and save the contents of the YAML file to a constant
with open(contributor_yaml_file) as f:
    CONTRIBUTOR_CONFIG = yaml.safe_load(f)

# Create a Path object pointing to the base text TEI file
TEXT_BASE_FILE = root.joinpath("text.tei.xml")

# Try to load a path to the dumped Heurist database
if load_dotenv(find_dotenv()):
    DB_PATH = os.getenv("DB_PATH")
else:
    DB_PATH = root.parent.joinpath("heurist.db")

if not Path(DB_PATH).is_file():
    raise FileNotFoundError()

# Try to load a path to the output directory for the generated TEI files
OUTDIR_PATH = os.getenv("OUTDIR")
