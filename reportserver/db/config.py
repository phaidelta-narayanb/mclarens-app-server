from pydantic import AnyUrl, BaseModel, ConfigDict, MariaDBDsn, MySQLDsn, PostgresDsn
from typing import Dict, List, Optional, Union


ConnectionName = str
AppName = str


class AppModule(BaseModel):
    models: List[str]
    default_connection: str = "default"


class DBSettings(BaseModel):
    connections: Dict[
        ConnectionName, Union[AnyUrl, PostgresDsn, MySQLDsn, MariaDBDsn]
    ] = {"default": "sqlite://:memory:"}
    apps: Dict[AppName, AppModule]
    routers: Optional[List[str]] = None
    use_tz: bool = False
    timezone: str = "UTC"

    model_config = ConfigDict(frozen=True)
