from django.contrib import admin, messages
from .models import Construction, Project, QualityPlanNumber, Akkuyu, \
    IndependentControl, DesignerSupervision, QC,  \
    Contractor, RFI, RelationConstructionProject, \
    RelationSupervisionRFI, RelationQaSignerRFI,\
    RelationIndependentRFI, RelationAkkuyuRFI, \
    create_copies_of_selected_rfis, Inspector, PtoEngineer, DefaultSignersbyConstruction
from django import forms
from rangefilter.filters import DateRangeFilter
from django.contrib.admin import SimpleListFilter

admin.site.register(Construction)
admin.site.register(PtoEngineer)
admin.site.register(Contractor)
admin.site.register(RelationSupervisionRFI)
admin.site.register(RelationQaSignerRFI)
admin.site.register(RelationIndependentRFI)
admin.site.register(RelationAkkuyuRFI)
admin.site.register(Inspector)
admin.site.register(DefaultSignersbyConstruction)
# Register your models here.

# class RFIForm(forms.ModelForm):
#     class Meta:
#         model = RFI
#         fields = '__all__'

#Другой сбособ фильтрации // Не понадобился
# class RFIAdmin(admin.ModelAdmin):
#     form = RFIForm
#
#     def get_form(self, request, obj=None, **kwargs):
#         form = super().get_form(request, obj=obj, **kwargs)
#
#         if obj is not None:
#             # If we are editing an existing RFI object, set the queryset of the test_rfi field
#             # based on the current object_name value
#             form.base_fields['test_rfi'].queryset = Relation_Construction_Test.objects.filter(construction=obj.object_name)
#         else:
#             # If we are creating a new RFI object, set the queryset of the test_rfi field
#             # based on the selected object_name value in the form
#             class DynamicRFIForm(form):
#                 def __init__(self, *args, **kwargs):
#                     super().__init__(*args, **kwargs)
#                     self.fields['test_rfi'].queryset = Relation_Construction_Test.objects.none()
#
#                 def clean(self):
#                     cleaned_data = super().clean()
#                     object_name = cleaned_data.get('object_name')
#                     if object_name:
#                         self.fields['test_rfi'].queryset = Relation_Construction_Test.objects.filter(construction=object_name)
#                     return cleaned_data
#
#             form = DynamicRFIForm
#
#         return form


class ProjectListFilter(SimpleListFilter):
    title = 'Project filter'
    parameter_name = 'project'

    def lookups(self, request, model_admin):
        projects = set([b.project_name for b in model_admin.model.objects.all()])

        sorted_projects = sorted(projects)
        return [(a.name) for a in sorted_projects]

    # def queryset(self, request, queryset):
    #     if self.value():
    #         return queryset.filter()
    #     else:
    #         return  queryset


class RFIAdmin(admin.ModelAdmin):
    """Фильтрация для Строительный объект-Проба"""
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'test_rfi':
            construction_id = request.POST.get('object_name')
            print('construction_id:', construction_id)  # debug statement
            if construction_id:
                queryset = RelationConstructionProject.objects.filter(construction_id=construction_id)
                print('queryset:', queryset)  # debug statement
                kwargs['queryset'] = queryset
            else:
                kwargs['queryset'] = RelationConstructionProject.objects.none()
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    verbose_name = "Custom Verbose Name"

    @admin.action(description='make_copies')
    def make_copies(modeladmin, request, queryset):
        for obj in queryset:
            obj.pk = None
            obj.id = None
            obj.save()
        messages.success(request, "Копии успешно созданы")

    list_filter = (('date_of_inspection', DateRangeFilter),
                    'object_name',
                    'project_name',
                    'status', 'inspector',
                   )

    list_display = ('excel_number', 'status',
                    'rfi_number',
                    'object_name', 'project_name',
                    'description_of_work_russian')

    search_fields = ('description_of_work_russian',)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "project_name":
            kwargs["queryset"] = Project.objects.order_by('object_name', 'project_name')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def set_status_rejected(self, request, queryset):
        queryset.update(status='rejected')
    set_status_rejected.short_description = "Set status to 'rejected'"

    def set_inspector(self, request, queryset):
        inspector = Inspector.objects.get(user__username='noker.hanov')
        queryset.update(inspector=inspector)
    set_inspector.short_description = "Set inspector to Noker Hanov"

    def set_status_accepted(self, request, queryset):
        queryset.update(status='accepted')
    set_status_accepted.short_description = "Set status to 'accepted'"

    def set_status_in_process(self, request, queryset):
        queryset.update(status='in process')
    set_status_in_process.short_description = "Set status to 'in process'"

    def set_status_canceled(self, request, queryset):
        queryset.update(status='canceled')
    set_status_canceled.short_description = "Set status to 'canceled'"

    def set_beton_status(self, request, queryset):
        queryset.update(is_active_beton=True)
    set_beton_status.short_description = "Set beton status to Active"

    actions = [create_copies_of_selected_rfis, set_status_rejected,
               set_status_accepted, set_status_in_process,
               set_status_canceled, set_inspector, set_beton_status]


admin.site.register(RFI, RFIAdmin)


class ProjectAdmin(admin.ModelAdmin):
    list_filter = ('object_name',)


admin.site.register(Project, ProjectAdmin)


class QualityPlanNumberAdmin(admin.ModelAdmin):
    search_fields = ('quality_plan_name', 'description_of_work', 'status_of_control_points')

    ordering = ('quality_plan_name',)

    def get_search_results(self, request, queryset, search_term):
        # Фильтрация по регулярному выражению
        use_distinct = False
        if 'regex:' in search_term:
            search_term = search_term.split('regex:', 1)[1]
            queryset = queryset.filter(quality_plan_name__regex=search_term)
        else:
            queryset, use_distinct = super().get_search_results(request, queryset, search_term)
        return queryset, use_distinct


admin.site.register(QualityPlanNumber, QualityPlanNumberAdmin)
