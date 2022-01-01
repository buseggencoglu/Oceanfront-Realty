from .models import House, Reservation
import django_filters
from .models import models
from .forms import forms
import datetime
from datetime import date


class houseFilter(django_filters.FilterSet):
    class Meta:
        model = House
        fields = {
            "name": ['exact'],
            "type": ['exact'],
            "description": ['exact'],
            "rooms": ['exact'],
            "price": ['exact', 'lt', 'gt'],
            "status": ['exact'],
            "branch": ['exact']
        }
        filter_overrides = {
            models.BooleanField: {
                'filter_class': django_filters.BooleanFilter,
                'extra': lambda f: {
                    'widget': forms.CheckboxInput,
                },
            },
        }


class ReservationFilter(django_filters.FilterSet):
    #pickUpDate = django_filters.DateFilter(lookup_type='gte', label='pickUpDate', input_formats=['%d-%m-%Y'],initial=date.today)
    class Meta:
        model = Reservation
        fields = {
            'location': ['exact'],
            'pickUpDate': ['exact', 'date__gte'],
            'returnDate': ['exact', 'date__gte'],
        }
        filter_overrides = {
            models.BooleanField: {
                'filter_class': django_filters.BooleanFilter,
                'extra': lambda f: {
                    'widget': forms.CheckboxInput,
                },
            },
        }

