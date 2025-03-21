# Pivot Heurist database to TEI documents
[![License: CC BY-SA 4.0](https://img.shields.io/badge/License-CC_BY--SA_4.0-lightgrey.svg)](https://creativecommons.org/licenses/by-sa/4.0/)

From the relational entities in LostMa's Heurist database, this package generates TEI documents, based at the level of a Text.

## Table of contents

- [Installation](#installation)
- [Usage](#usage)
  - [Configure project](#configure-project)
  - [Download new Heurist data](#download-heurist-data)
  - [Pivot data to TEI](#pivot-data-to-tei)
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

1. [Configure project](#configure-project)
2. [Download new Heurist data](#download-heurist-data)
3. [Pivot data to TEI](#pivot-data-to-tei)

Short cut (for when you've already configured the project):

```shell
# First step
lostma-tei heurist download
```

```shell
# Second step
lostma-tei pivot texts
```


### Configure project

Write your Heurist login credentials in a `.env` file. See [setup](https://lostma-erc.github.io/heurist-etl-pipeline/usage/#installation) for more information.

```env
DB_NAME=database_name
DB_LOGIN="user.name"
DB_PASSWORD=password
```

In the [`config.yml`](./config.yml) file for this project, confirm the path to the DuckDB database file that will be generated when the Heurist data is downloaded from the remote server.

```yaml
file paths:
  database: heurist.db
  output directory: texts
```

### Download Heurist data

Run the `heurist download` command of this package, which automatically reads all the necessary parameters from this project's config file and the `.env` file you set up.

```console
$ lostma-tei heurist download
Get DB Structure ⠙ 0:00:01
Get Records ━━━━━━━━━━━━━━━━━━━━ 25/25 0:00:11
```

If you don't want to set up a `.env` file, pass the relevant parameters to the command as options.

```shell
lostma-tei heurist download \
--database heurist_database \
--login "user.name" \
--password "password"
```

### Pivot data to TEI

Run the `pivot texts` command of this package to select all the texts loaded into the DuckDB database and transform them into TEI-XML documents. The documents will be written in the `output directory` folder you specified in the [`config.yml`](./config.yml) file.

```console
$ lostma-tei pivot texts
Transforming text metadata... ━━━━━━━━━━━━━━━━━━━━ 487/487 0:00:13
```

## Development

Install an editable version of this application with the development dependencies.

```console
$ pip install -e .["dev"]
Obtaining file:///home/user/Dev/pivot-format
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
