from pathlib import Path

DB_PATH = Path(__file__).parent.parent.joinpath("heurist.db")

XML_ID = "{http://www.w3.org/XML/1998/namespace}id"
XML_NS = "{http://www.w3.org/XML/1998/namespace}ns"
XML_BASE = "{http://www.w3.org/XML/1998/namespace}base"

NSMAP = {
    "xml": "http://w3.org/XML/1998/namespace",
    "tei": "http://www.tei-c.org/ns/1.0",
}

ENCODER_RESP = ["Kelly Christensen"]

DATA_ENTRY_RESP = {
    "dum": [
        "Elisabeth de Bruijn",
        "Cecile Vermaas",
        "Mike Kestemont",
        "Remco Sleiderink",
    ],
    "gmh": [
        "Mike Kestemont",
    ],
    "default": [
        "Jean-Baptiste Camps",
        "Kelly Christensen",
    ],
    "non": [
        "Katarzyna Kapitan",
    ],
}
