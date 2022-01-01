from django.db import models


class ConfirmedShopManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().filter(status='C')


class AvailableProductManager(models.Manager):
    
    def get_queryset(self):
        return super().get_queryset().filter(is_available=1)
