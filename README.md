# Pivot Heurist database to TEI documents
[![License: CC BY-SA 4.0](https://img.shields.io/badge/License-CC_BY--SA_4.0-lightgrey.svg)](https://creativecommons.org/licenses/by-sa/4.0/)

This Python package is used to convert metadata from the relational entities created in LostMa's Heurist database into TEI documents. The TEI documents are based at the level of a Text and feature a `<listWit>` entity, in which are listed the related Witness entities' metadata.

## Table of contents

- [Installation](#installation)
- [Usage](#usage)
- [Development](#development)
- [License](#license)

## Installation

This project is packaged with a `pyproject.toml` file. Install it with `pip install`.

```console
$ pip install .
Obtaining file:///home/user/Dev/pivot-format
  Installing build dependencies ... done
  Checking if build backend supports build_editable ... done
  Getting requirements to build editable ... done
  Installing backend dependencies ... done
...
Successfully built pivot heurist
```

## Usage

### Update the Heurist data

This project's command `pivot` requires access to the Heurist database's data. More specifically, it expects to find a DuckDB database file that a partner Python package [`heurist`](https://lostma-erc.github.io/heurist-etl-pipeline/) generates with its `download` command. The `heurist` Python package is automatically installed with this package.

Refresh the downloaded database, using the record-type option `-r` to collect entities relevant to the TEI pivot format.

```shell
-r "My record types" -r "Place, features" -r "People and organisations"
```



If you haven't or are having trouble setting up the `heurist` CLI (see [setup](https://lostma-erc.github.io/heurist-etl-pipeline/usage/#installation)), don't worry. The program will prompt you to manually enter any missing information that's necessary for its API to connect to the Heurist database.

```console
$ heurist download -f heurist.db -r "My record types" -r "Place, features" -r "People and organisations"

A connection to your Heurist database could not be established.
Please provide the information when prompted. To quit, press Ctrl+C then Enter.
Heurist database name: jbcamps_gestes
Heurist user login: ############
Heurist login password: ############
Retrying the connection...
Success!
Get DB Structure ⠼ 0:00:00
Get Records ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 25/25 0:00:12

Created the following tables
┌───────────────┐
│     name      │
│    varchar    │
├───────────────┤
│ CreativeWork  │
│ Digitization  │
│ DocumentTable │
│ Footnote      │

```

### Pivot all texts to TEI documents

If necessary, make edits to the configuration file, located at [config.yml](./config.yml). Most importantly, make sure that the path to the Heurist database you transformed and downloaded as a DuckDB file is correct.

```yaml
file paths:
  database: heurist.db
  output directory: output
  text TEI model: tei_base_text.xml

```

Run the `pivot all` command. The package will look for the configuration file at `./config.yml` and proceed to process all the text metadata in the downloaded Heurist database file.

```console
$ pivot all
Transforming text metadata... ━━━━━━━━━━━━━━━━━━━━━━━╺━━━━━━━━━━━━━━━━ 283/487 0:00:06
```

As detailed in the configuration file (see `output directory: output`), the generated TEI documents will be written to the directory `./output`. The beginning of the files will ressemble that shown below:

```xml
<?xml version='1.0' encoding='utf-8'?>
<?xml-model href="http://www.tei-c.org/release/xml/tei/custom/schema/relaxng/tei_all.rng" type="application/xml" schematypens="http://relaxng.org/ns/structure/1.0"?>
<?xml-model href="http://www.tei-c.org/release/xml/tei/custom/schema/relaxng/tei_all.rng" type="application/xml"
	schematypens="http://purl.oclc.org/dsdl/schematron"?>
<TEI xmlns="http://www.tei-c.org/ns/1.0">
  <!-- Add Heurist ID of text as xml:id -->
  <teiHeader>
    <fileDesc>
      <titleStmt>
        <title>Encoded metadata of "Iwein"</title>
        <funder>European Research Council</funder>
        <principal>Jean-Baptiste Camps</principal>
        <respStmt>
          <name>Mike Kestemont</name>
          <resp>data entry and proof correction</resp>
          <name>Kelly Christensen</name>
          <resp>conversion of metadata to TEI markup</resp>
          <name>Théo Moins</name>
          <resp>conversion of text to TEI markup</resp>
        </respStmt>
      </titleStmt>
      <publicationStmt>
        <publisher>LostMa ERC Project</publisher>
        <pubPlace>Paris</pubPlace>
        <date>2025-03-20</date>
        <availability status="restricted">
          <licence target="https://creativecommons.org/licenses/by/4.0/">Distributed under a Creative Commons Attribution 4.0 International License</licence>
        </availability>
      </publicationStmt>
```

## Development

Install an editable version of this application with the development dependencies.

```console
$ pip install -e .["dev"]
Obtaining file:///home/kchrist/Dev/pivot-format
  Installing build dependencies ... done
  Checking if build backend supports build_editable ... done
  Getting requirements to build editable ... done
  Installing backend dependencies ... done
  Preparing editable metadata (pyproject.toml) ... done
```

Practice Test-Driven Development and run tests with `pytest`.

When a data model is needed for a test, privilege creating a stable version of the data model, storing it in the [`tests/mock_data/`](./tests/mock_data/) directory, and making it importable in the [`__init__.py`](./tests/mock_data/__init__.py) file.

A model for how to create mock data (i.e. a Text), can be found in the [`make_mock_data.py`](./tests/mock_data/make_mock_data.py) module.

## License

[![License: CC BY-SA 4.0](https://img.shields.io/badge/License-CC_BY--SA_4.0-lightgrey.svg)](https://creativecommons.org/licenses/by-sa/4.0/)

Attribution-ShareAlike 4.0 International.
