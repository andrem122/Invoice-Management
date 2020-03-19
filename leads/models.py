from django.db import models
from property.models import Company

class Lead(models.Model):
    """Leads captured from marketing"""
    name = models.CharField(max_length=150)
    phone_number = models.CharField(max_length=50, null=True)
    email = models.EmailField(null=True)
    date_of_inquiry = models.DateTimeField()
    renter_brand = models.CharField(max_length=50)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True)
    sent_text_date = models.DateTimeField(auto_now_add=True)
    sent_email_date = models.DateTimeField(auto_now_add=True)
    filled_out_form = models.BooleanField(default=False)
    made_appointment = models.BooleanField(default=False)

    def __str__(self):
        return 'Lead #{0} - {1} - {2}'.format(self.pk, self.name, self.company.name)
