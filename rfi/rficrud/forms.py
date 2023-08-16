from django import forms
from django.forms.widgets import DateInput
from .models import RFI, Construction, Project, Comment
from django_select2.forms import Select2Widget
from dal import autocomplete
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _
from django.forms import widgets
from bootstrap_datepicker_plus.widgets import DateTimePickerInput


class RfiFilterForm(forms.Form):
    object_name = forms.ModelChoiceField(
        queryset=Construction.objects.all(),
        required=False,
        empty_label="All objects",
    )
    project_name = forms.ModelChoiceField(
        queryset=Project.objects.none(),
        required=False,
        empty_label="All projects",
    )
    start_date = forms.DateField(label='start_date', required=False, widget=DateInput(attrs={'type': 'date'}))
    end_date = forms.DateField(label='end_date', required=False, widget=DateInput(attrs={'type': 'date'}))
    status = forms.ChoiceField(label='Status', required=False, choices=[('', '---------')] + RFI.status_list)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        object_name = self.data.get('object_name')
        if object_name:
            self.fields['project_name'].queryset = Project.objects.filter(object_name_id=object_name)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 3})}


elevation_regex = r'^[+-]?(\d+([\.,]\d{3})?|\d*([\.,]\d{3}))?$'
elevation_validator = RegexValidator(elevation_regex, _('Введите отметку в формате "+12.210"'))


class RFICreateForm(forms.ModelForm):
    object_name = forms.ModelChoiceField(
        queryset=Construction.objects.all(), label=_("Объект")
    )
    description_of_work_russian = forms.CharField(widget=forms.Textarea, label=_("Описание работ"))

    axes = forms.CharField(max_length=100, required=False, label=_('Ось'))
    from_elevation = forms.CharField(max_length=100, required=False,
                                     validators=[elevation_validator], label=_('От Отметки'))
    to_elevation = forms.CharField(max_length=100, required=False,
                                   validators=[elevation_validator], label=_('До Отметки'))
    executive_scheme = forms.BooleanField(required=False, label=_("Исполнительная схема"))
    beton_work = forms.BooleanField(required=False, label=_("Добавить бетонирование"))

    date_of_inspection = forms.DateTimeField(
        widget=DateTimePickerInput(
            options={
                'format': 'YYYY-MM-DD HH:mm',
                'showTodayButton': True,
                'showClear': True,
                'sideBySide': True,  # Добавляем опцию для отображения даты и времени рядом
            }
        ), label=_('Дата и время проведения инспекции')
    )

    class Meta:
        model = RFI
        fields = (
            'object_name',
            'project_name',
            'date_of_inspection',
            'inspector',
            'description_of_work_russian',
            'pk_points',
            'akkuyu_signer',
            'independent_control',
            'qc_signer',
            'design_supervision_signer',
            'contractor',
            'axes',
            'from_elevation',
            'to_elevation',
            'executive_scheme',
            'beton_work',
        )

        # widgets = {
        #     'object_name': autocomplete.ModelSelect2(url='object_autocomplete',
        #                                              forward=('project_name',)),
        # }

        labels = {
            'object_name': "Название объекта",
            'project_name': "Название проекта",
            'date_of_inspection': "DATE",
            'description_of_work_russian': 'Описание работы',
            'executive_scheme': 'ELEVATOR 3000',
        }

    # Customize form field widgets, labels, and other attributes if needed
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['object_name'].widget.attrs['class'] = 'form-control'
        self.fields['project_name'].widget.attrs['class'] = 'form-control'
        self.fields['inspector'].widget.attrs['class'] = 'form-control'
        self.fields['date_of_inspection'].widget.attrs['class'] = 'form-control'
        self.fields['description_of_work_russian'].widget.attrs['class'] = 'form-control'
        self.fields['pk_points'].widget.attrs['class'] = 'form-control'
        self.fields['akkuyu_signer'].widget.attrs['class'] = 'form-control'
        self.fields['independent_control'].widget.attrs['class'] = 'form-control'
        self.fields['qc_signer'].widget.attrs['class'] = 'form-control'
        self.fields['design_supervision_signer'].widget.attrs['class'] = 'form-control'
        self.fields['contractor'].widget.attrs['class'] = 'form-control'
        self.fields['axes'].widget.attrs['class'] = 'form-control'
        self.fields['from_elevation'].widget.attrs['class'] = 'form-control'
        self.fields['to_elevation'].widget.attrs['class'] = 'form-control'
        self.fields['executive_scheme'].widget.attrs['class'] = 'form-control'
        self.fields['beton_work'].widget.attrs['class'] = 'form-control'

