from django import forms
from rficrud.models import RFI, Construction, Project, RelationAkkuyuRFI, RelationIndependentRFI, RelationQaSignerRFI, RelationSupervisionRFI, Contractor
from django.forms.widgets import DateInput


class RfiFilterForm(forms.Form):
    object_name = forms.CharField(label='Object Name', required=False)
    project_name = forms.CharField(label='Project Name', required=False)
    date_of_create = forms.DateField(label='Date of Create', required=False, widget=DateInput(attrs={'type': 'date'}))
    status = forms.ChoiceField(label='Status', required=False, choices=[('', '---------')] + RFI.status_list)


class RFIForm(forms.ModelForm):
    class Meta:
        model = RFI
        fields = ['object_name', 'project_name', 'akkuyu_signer', 'independent_control', 'qc_signer', 'design_supervision_signer', 'contractor']


class NumberRangeForm(forms.Form):
    from_number = forms.IntegerField(label='From number', required=True)
    to_number = forms.IntegerField(label='To number', required=True)