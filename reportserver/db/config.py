from pydantic import AnyUrl, BaseModel, ConfigDict, MariaDBDsn, MySQLDsn, PostgresDsn
from typing import Union


class DBSettings(BaseModel):
    db_uri: Union[AnyUrl, PostgresDsn, MySQLDsn, MariaDBDsn] = "sqlite:///:memory:"

    model_config = ConfigDict(frozen=True)
