from django.db import models

class Vendor(models.Model):

    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:

        db_table = 'vendor'

        
class Category(models.Model):

    VEHICLE_TYPE = (
        ('Sedan', 'Sedan'),
        ('Coupe', 'Coupe'),
        ('Hatchback', 'Hatchback'),
        ('SUV', 'SUV'),
        ('Minivan', 'Minivan')
    )  
    vehicle_type = models.CharField(max_length=20, choices=VEHICLE_TYPE)    

    def __str__(self):
        return self.vehicle_type

    class Meta:

        db_table = 'category' 

class Vehicle(models.Model):

    name = models.CharField(max_length=50)
    price = models.DecimalField(decimal_places=2, max_digits=20)
    launch_date = models.DateField()
    vendor = models.ForeignKey(Vendor, related_name="vehicles", on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        
        db_table='vehicle'        
