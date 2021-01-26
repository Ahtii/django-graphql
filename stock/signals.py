from django.db.models.signals import post_save, post_delete
from graphene_subscriptions.signals import post_save_subscription, post_delete_subscription

from stock.models import *

print("in signals")

post_save.connect(post_save_subscription, sender=Vendor, dispatch_uid="vendor_post_save")
post_delete.connect(post_delete_subscription, sender=Vendor, dispatch_uid="vendor_post_delete") 

post_save.connect(post_save_subscription, sender=Vehicle, dispatch_uid="vehicle_post_save")
post_delete.connect(post_delete_subscription, sender=Vehicle, dispatch_uid="vehicle_post_delete") 

post_save.connect(post_save_subscription, sender=Category, dispatch_uid="category_post_save")
post_delete.connect(post_delete_subscription, sender=Category, dispatch_uid="category_post_delete") 