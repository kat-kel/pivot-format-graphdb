from pydantic import BaseModel
from app.database import DBConn
from dataclasses import dataclass
from app.data_models.term import TermModel


@dataclass
class ForeignKey:
    alias: str
    extra: dict


class BaseDataModel(BaseModel):

    @classmethod
    def fk_aliases_single(cls) -> list[ForeignKey]:
        return [
            ForeignKey(alias=f.validation_alias, extra=f.json_schema_extra)
            for f in cls.model_fields.values()
            if (
                f.validation_alias is not None
                and f.validation_alias.endswith("H-ID")
                and f.validation_alias != "H-ID"
                and "List" not in repr(f.annotation)
            )
        ]

    @classmethod
    def fk_aliases_repeated(cls) -> list[ForeignKey]:
        return [
            ForeignKey(alias=f.validation_alias, extra=f.json_schema_extra)
            for f in cls.model_fields.values()
            if (
                f.validation_alias is not None
                and f.validation_alias.endswith("H-ID")
                and f.validation_alias != "H-ID"
                and "List" in repr(f.annotation)
            )
        ]

    @classmethod
    def term_aliases_single(cls) -> list:
        return [
            f.validation_alias
            for f in cls.model_fields.values()
            if (
                f.validation_alias is not None
                and f.validation_alias.endswith("TRM-ID")
                and "List" not in repr(f.annotation)
            )
        ]

    @classmethod
    def term_aliases_repeated(cls) -> list:
        return [
            f.validation_alias
            for f in cls.model_fields.values()
            if (
                f.validation_alias is not None
                and f.validation_alias.endswith("TRM-ID")
                and "List" in repr(f.annotation)
            )
        ]

    @classmethod
    def get_one_term(cls, id: int | None, db: DBConn) -> TermModel | None:
        if id:
            query = f"SELECT * FROM trm WHERE trm_ID = {id}"
            term_row_dict = db.select_one(query=query)
            return TermModel(**term_row_dict)

    @classmethod
    def validate_terms(cls, row_dict: dict, db: DBConn) -> None:
        # Fetch and validate term IDs in singular data fields
        for alias in cls.term_aliases_single():
            trm_id = row_dict.get(alias)
            if trm_id:
                model = cls.get_one_term(id=trm_id, db=db)
                row_dict.update({alias: model})

        # Fetch and validate term IDs for repeateable
        for alias in cls.term_aliases_repeated():
            id_list = row_dict.get(alias)
            if len(id_list) > 0:
                models = [cls.get_one_term(id=id, db=db) for id in id_list]
                row_dict.update({alias: models})

    @classmethod
    def validate_foreign_keys(cls, row_dict: dict, db: DBConn) -> None:
        # Fetch and validate fk IDs in singular data fields
        for fk in cls.fk_aliases_single():
            table = fk.extra["table"]
            Model = fk.extra["model"]
            if not table or not Model:
                continue
            fk_id = row_dict.get(fk.alias)
            if fk_id:
                row = db.get_by_id(table=table, hid=fk_id)
                nested_dict = Model.build_nested_dict(row_dict=row, db=db)
                row_dict.update({fk.alias: nested_dict})

        # Fetch and validate fk IDs in repeated data fields
        for fk in cls.fk_aliases_repeated():
            table = fk.extra["table"]
            Model = fk.extra["model"]
            if not table or not Model:
                continue
            ids = row_dict.get(fk.alias)
            if ids == [None]:
                continue
            elif len(ids) > 0:
                nested_dicts = []
                for fk_id in ids:
                    row = db.get_by_id(table=table, hid=fk_id)
                    nested_dict = Model.build_nested_dict(row_dict=row, db=db)
                    nested_dicts.append(nested_dict)
                row_dict.update({fk.alias: nested_dicts})

    @classmethod
    def build_nested_dict(cls, row_dict: dict, db: DBConn) -> dict:
        # Fetch and validate the model's vocabulary terms
        cls.validate_terms(row_dict=row_dict, db=db)

        # Fetch and validate the model's foreign keys
        cls.validate_foreign_keys(row_dict=row_dict, db=db)

        return row_dict
