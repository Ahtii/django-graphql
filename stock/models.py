from django.db import models

class Product(models.Model):

    name = models.CharField(max_length=20)
    price = models.DecimalField(decimal_places=2, max_digits=20)
    expire_date = models.DateField()
    created_date = models.DateField()

    def __str__(self):
        return self.name

    class Meta:
        
        db_table='product'