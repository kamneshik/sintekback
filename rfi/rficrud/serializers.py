from rest_framework import serializers, filters
from .models import DefaultSignersbyConstruction, \
                    Construction, RelationAkkuyuRFI, \
                    RelationIndependentRFI, RelationSupervisionRFI, \
                    RelationQaSignerRFI, Contractor, Project
from .models import RFI
import pytz

local_tz = pytz.timezone('Europe/Moscow')

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Добавьте дополнительные поля пользователя в токен, если это необходимо
        token['username'] = user.username
        return token


class ProjectSerializer(serializers.ModelSerializer):
    project_name = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = ('id', "project_name", )
        filter_backends = [filters.SearchFilter]
        search_fields = ['object_name__object_name']

    def get_project_name(self, obj):
        return {
            'name': obj.name()
        }


class DefaultSignersConstructionSerializer(serializers.ModelSerializer):
    object_name = serializers.SerializerMethodField()
    akkuyy_signer = serializers.SerializerMethodField()
    independent_signer = serializers.SerializerMethodField()
    supervision_signer = serializers.SerializerMethodField()
    titan2_qc_signer = serializers.SerializerMethodField()
    titan2_contractor_signer = serializers.SerializerMethodField()

    class Meta:
        model = DefaultSignersbyConstruction
        fields = ('id', 'object_name', 'akkuyy_signer', 'independent_signer',
                  'supervision_signer', 'titan2_qc_signer', 'titan2_contractor_signer')

        filter_backends = [filters.SearchFilter]
        search_fields = ['object_name']

    def get_object_name(self, obj):
        return {
            'id': obj.object_name.id,
            'name': obj.object_name.object_name
        }

    def get_akkuyy_signer(self, obj):
        return {
            'id': obj.akkuyy_signer.id,
            'name': obj.akkuyy_signer.signer_name
        }

    def get_independent_signer(self, obj):
        return {
            'id': obj.independent_signer.id,
            'name': obj.independent_signer.signer_name
        }

    def get_supervision_signer(self, obj):
        return {
            'id': obj.supervision_signer.id,
            'name': obj.supervision_signer.signer_name
        }

    def get_titan2_qc_signer(self, obj):
        return {
            'id': obj.titan2_qc_signer.id,
            'name': obj.titan2_qc_signer.signer_name
        }

    def get_titan2_contractor_signer(self, obj):
        return {
            'id': obj.titan2_contractor_signer.id,
            'name': obj.titan2_contractor_signer.signer_name
        }


class RFISerializer(serializers.ModelSerializer):
    project_name = serializers.SerializerMethodField()
    object_name = serializers.SerializerMethodField()
    description_of_work_russian = serializers.SerializerMethodField()
    date_of_create = serializers.SerializerMethodField()
    date_of_inspection = serializers.SerializerMethodField()

    class Meta:
        model = RFI
        fields = '__all__'

    def get_project_name(self, obj):
        return {
            'id': obj.project_name.id,
            'name': obj.project_name.name(),
            'short_name': f"{obj.project_name.type_of_works}.{obj.project_name.project_name}",
        }

    def get_object_name(self, obj):
        return {
            'id': obj.object_name.id,
            'name': obj.object_name.object_name
        }

    def get_description_of_work_russian(self, obj):
        return {
            'full': obj.description_of_work_russian,
            'short': obj.short_description()
        }

    def get_date_of_create(self, obj):
        localized_create_time = obj.date_of_create.astimezone(local_tz)
        return {
            'date': obj.date_of_create.date(),
            'time': localized_create_time.time(),
        }

    def get_date_of_inspection(self, obj):
        localized_create_time = obj.date_of_inspection.astimezone(local_tz)

        return {
            'date': obj.date_of_inspection.date(),
            'time': localized_create_time.time(),
        }
