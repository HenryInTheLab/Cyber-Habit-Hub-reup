from django.db import models


class BlacklistedDomains(models.Model):
    id = models.BigAutoField(primary_key=True)
    registry_id = models.IntegerField()
    domain = models.CharField(max_length=255)
    date_added = models.DateField(null=True, blank=True)
    date_removed = models.DateField(null=True, blank=True)
    
    class Meta:
        db_table = 'domains'
        managed = False

    def __str__(self):
        return f"{self.domain}"