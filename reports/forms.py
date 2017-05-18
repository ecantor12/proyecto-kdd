from datetime import datetime
from django import forms

class DateFilterReport(forms.Form):

    initial_date = forms.DateField(label="Fecha inicial", required=False)
    final_date = forms.DateField(label="Fecha final", required=False)


class LimitFilterReport(forms.Form):
    
    limit = forms.IntegerField(label="Limite", required=False)
    