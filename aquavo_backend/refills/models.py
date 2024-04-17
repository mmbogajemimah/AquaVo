from django.db import models
from django.utils.translation import gettext_lazy as _
from accounts.models import CustomUser

# Create your models here.
class Refill(models.Model):
    customer = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="refills")
    amount_liters = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("Amount in Litres"))
    amount_money =  models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("Amount in Kenyan Shillings"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created At'))
    updated_at = models.DateField(auto_now=True, verbose_name=_("Updated At"))
    
    class Meta:
        verbose_name = _("Refill")
        verbose_name_plural = _("Refills")
        ordering = ["-created_at"] # Order by the latest Refills First
        
    def __str__(self):
        return f"Refill {self.id} for Customer {self.customer.email} at {self.created_at}"
    
