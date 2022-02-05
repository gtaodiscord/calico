from tortoise import fields
from tortoise.models import Model


class User(Model):
    """Model representing a user."""

    id = fields.BigIntField(pk=True)
    name = fields.CharField(max_length=32)
    discriminator = fields.CharField(max_length=4)
    created_at = fields.DatetimeField()
    joined_at = fields.DatetimeField()
    in_guild = fields.BooleanField()

    class Meta:
        table = "users"


class Category(Model):
    """Model representing a category channel."""

    id = fields.BigIntField(pk=True)
    name = fields.CharField(max_length=99)

    class Meta:
        table = "categories"


class Channel(Model):
    """Model representing a channel."""

    id = fields.BigIntField(pk=True)
    name = fields.CharField(max_length=99, unique=False)
    staff = fields.BooleanField()

    category: fields.ForeignKeyRelation[Category] = fields.ForeignKeyField(
        "models.Category", related_name="categories"
    )

    class Meta:
        table = "channels"


class Message(Model):
    """Model representing a message."""

    id = fields.BigIntField(pk=True)
    created_at = fields.DatetimeField()
    deleted = fields.BooleanField(default=False)

    channel: fields.ForeignKeyRelation[Channel] = fields.ForeignKeyField(
        "models.Channel", related_name="channels"
    )
    author: fields.ForeignKeyRelation[User] = fields.ForeignKeyField(
        "models.User", related_name="users"
    )

    class Meta:
        table = "messages"
