from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from .models import WageEstimation
from .serializers import WageEstimationSerializer
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import APIException
import math


# Create your views here.
class NoSuchDataException(APIException):
    status_code = 400
    default_detail = 'No data with such query'


class WageEstimationViewSet(viewsets.ModelViewSet):
    # single/multiple request for WageEstimation - /api/wage-estimation/
    serializer_class = WageEstimationSerializer
    queryset = WageEstimation.objects.all()
    http_method_names = ['get', 'post', 'head', 'put', 'delete']
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['id', 'job_title', 'worksite_city', 'worksite_state', 'disclose_wage_rate',
                        'actual_wage_rate']

    def avg_salary_data(self, query_data):
        """
            args: queryset
            return: float
        """
        total_salary = 0
        for i in range(0, len(query_data)):
            salary_from = self.serializer_class(
                query_data[i]).data['disclose_wage_rate']
            salary_to = self.serializer_class(
                query_data[i]).data['actual_wage_rate']
            if salary_from > salary_to:
                total_salary += salary_from
            else:
                total_salary += salary_to
        return total_salary

    def high_salary(self, query_data, data):
        """
            args: queryset, int
            return: float
        """
        salary_from = self.serializer_class(
            query_data[data]).data['disclose_wage_rate']
        salary_to = self.serializer_class(
            query_data[data]).data['actual_wage_rate']
        if salary_from > salary_to:
            return salary_from
        else:
            return salary_to

    def create(self, request, *args, **kwargs):
        #  POST :
        """
        return: json response
        """
        try:
            mandatory_keys = ['title', 'city', 'state', ]
            req_data = request.data
            for key in mandatory_keys:
                if key not in req_data:
                    msg ="Invalid request body"
                    return Response({"messafe": msg, "status": "Failed"}, status=status.HTTP_400_BAD_REQUEST)
                elif key == "title":
                    if req_data['title'] == "" or req_data['title'] is None:
                        msg ="title is missing or invalid"
                        return Response({"messafe": msg, "status": "Failed"}, status=status.HTTP_400_BAD_REQUEST)
                    elif type(req_data['title']) == int or type(req_data['title']) == float:
                        msg = "Invalid title value"
                        return Response({"messafe": msg, "status": "Failed"}, status=status.HTTP_400_BAD_REQUEST)
                elif type(req_data[key]) == int or type(req_data[key]) == float:
                    msg ="Invalid request body type, must be string"
                    return Response({"messafe": msg, "status": "Failed"}, status=status.HTTP_400_BAD_REQUEST)

            query_data = []
            title = req_data['title'].upper()
            city = req_data['city'].upper()
            state = req_data['state'].upper()
            if title and city and state:
                    query_data = self.queryset.filter(job_title__icontains=title, worksite_city__icontains=city,
                                                      worksite_state__icontains=state)
            elif title and state:
                    query_data = self.queryset.filter(
                        job_title__icontains=title, worksite_state__icontains=state)
            elif title:
                    query_data = self.queryset.filter(job_title__icontains=title)

            if query_data:
                total_count = query_data.count()
                median = math.ceil(total_count / 2) - 1
                twenty_fifth_percentile = math.ceil(total_count * .25) - 1
                seventy_fifth_percentile = math.ceil(total_count * .75) - 1
                serializer_data_median = self.high_salary(query_data, median)
                serializer_data_twenty_fifth = self.high_salary(
                    query_data, twenty_fifth_percentile)
                serializer_data_seventy_fifth = self.high_salary(
                    query_data, seventy_fifth_percentile)
                avg_salary = round(self.avg_salary_data(
                    query_data) / total_count, 2)

                return Response(
                    {"Number of datapoints": total_count, "Avg salary": avg_salary,
                     "Median Salary": serializer_data_median,
                     "25th Percentile Salary": serializer_data_twenty_fifth,
                     "75th Percentile Salary": serializer_data_seventy_fifth})
            else:
                raise NoSuchDataException()
        except Exception:
            msg = "No data available with such information"
            return Response({"messafe": msg, "status": "Success"})