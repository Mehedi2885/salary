from rest_framework import serializers
from . models import WageEstimation

class WageEstimationSerializer (serializers.ModelSerializer):
   # Maintenance table serializers
    def __init__(self, *args, **kwargs):
        many = kwargs.pop('many', True)
        super(WageEstimationSerializer, self).__init__(
            many=many, *args, **kwargs)

    class Meta:
        model = WageEstimation
        fields = ('id', 'job_title', 'worksite_city', 'worksite_state', 'disclose_wage_rate',
                  'actual_wage_rate')
