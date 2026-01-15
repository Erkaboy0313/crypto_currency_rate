from tortoise import models, fields


class Price(models.Model):
    id = fields.IntField(pk=True)

    ticker = fields.CharField(max_length=20, index=True)
    price = fields.DecimalField(max_digits=20, decimal_places=8)
    timestamp = fields.BigIntField(index=True)

    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "prices"
        indexes = [
            ("ticker", "timestamp"),
        ]