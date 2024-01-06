from tortoise.models import Model
from tortoise import fields

from .data_models import WorkTaskInsert


class DBWorkTask(Model):
    class Meta:
        table = "work_task"

    uuid = fields.UUIDField(pk=True)
    name = fields.CharField(max_length=256, null=True)
    created_by = fields.UUIDField()  # TODO: FK
    created_ts = fields.DatetimeField(auto_now_add=True)
    updated_ts = fields.DatetimeField(auto_now=True, null=True)

    @classmethod
    def from_model(cls, model: WorkTaskInsert):
        return cls(
            uuid=model.id,
            name=model.name,
            created_by=model.created_by_user,
        )
