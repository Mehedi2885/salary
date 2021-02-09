from django.db import models

class WageEstimation(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    job_title = models.CharField(db_column='JOB_TITLE', max_length=111, blank=True, null=True)
    worksite_city = models.CharField(db_column='WORKSITE_CITY', max_length=33, blank=True, null=True)
    worksite_state = models.CharField(db_column='WORKSITE_STATE', max_length=33, blank=True, null=True)
    disclose_wage_rate = models.FloatField(db_column='DISCLOSE_WAGE_RATE', blank=True, null=True)
    actual_wage_rate = models.FloatField(db_column='ACTUAL_WAGE_RATE', blank=True, null=True)
    
    def __str__(self):
        return str(self.id)

    class Meta:
        ordering = ['id'] #sort in asc order
        managed = False
        verbose_name_plural = "JOB_SALARY"
        db_table = 'job_salary'
