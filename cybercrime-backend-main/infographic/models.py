from django.db import models

class Victimisation(models.Model):
    tab = models.CharField(max_length=100)
    main_type = models.CharField(max_length=255)
    subcategory = models.CharField(max_length=255, null=True, blank=True)
    incident_type = models.CharField(max_length=255, null=True, blank=True)
    gender = models.CharField(max_length=20)
    age = models.CharField(max_length=50)
    sme_status = models.CharField(max_length=100)
    prevalence_2024 = models.FloatField()
    adjusted_2023 = models.FloatField(null=True, blank=True)
    adjusted_2024 = models.FloatField(null=True, blank=True)
    significant_diff = models.CharField(max_length=20)

    class Meta:
        db_table = 'victimisation'


class OnlineBehaviour(models.Model):
    tab = models.CharField(max_length=100)
    behaviour_type = models.CharField(max_length=255)
    variable = models.CharField(max_length=255)
    tech_level = models.CharField(max_length=100, null=True, blank=True)
    gender = models.CharField(max_length=20)
    age = models.CharField(max_length=50)
    sme_status = models.CharField(max_length=100, null=True, blank=True)
    adjusted_2023 = models.FloatField(null=True, blank=True)
    adjusted_2024 = models.FloatField(null=True, blank=True)
    significant_diff = models.BooleanField(null=True)

    class Meta:
        db_table = 'online_behaviours'



class FinancialLoss(models.Model):
    median_type = models.CharField(max_length=255)
    cybercrime = models.CharField(max_length=255)
    value = models.IntegerField()
    tooltip = models.CharField(max_length=255)

    class Meta:
        db_table = 'financial_losses'

    def __str__(self):
        return f"{self.median_type} - {self.cybercrime}"
