from django.db import models
from django.contrib import admin
from django.utils.html import format_html
from django.utils.text import slugify
from datetime import date, datetime
from django.contrib.auth.models import User
import random
from django.utils.translation import gettext_lazy as _
from googletrans import Translator
today_date = date.today()


class Construction(models.Model):
    """Модель строительного объекта и расшифровкой на русский и английский язык"""
    id = models.AutoField(primary_key=True)
    object_name = models.CharField(max_length=10, unique=True, db_index=True)
    object_place = models.CharField(max_length=500)

    def __str__(self):
        return self.object_name

    class Meta:
        db_table = 'construction_table'
        verbose_name = 'Объект'
        verbose_name_plural = 'Объекты'


class QualityPlanNumber(models.Model):
    """Тут добавить информацию о плане качества"""
    id = models.AutoField(primary_key=True)
    quality_plan_name = models.CharField(max_length=100,
                                         default='AKU.2008.00UKU.0.CS.QA0005_C01')

    description_of_work = models.CharField(max_length=500,
                                           blank=True, null=True)

    status_of_control_points = models.CharField(max_length=10,
                                                blank=True, null=True)

    def __str__(self):
        return self.quality_plan_name

    class Meta:
        db_table = 'quality_plan_table'
        verbose_name = 'План качества'
        verbose_name_plural = 'Планы качества'


CHOICES = (
    (0, 'Zero'),
    (1, 'One'),
    (2, 'Two')
)


class Inspector(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    checklists_copies = models.IntegerField(choices=CHOICES[:2], default=0, verbose_name='Количество копий Чеклистов')
    rfi_copies = models.IntegerField(choices=CHOICES, default=0, verbose_name='Количество копий ЗНО')

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'

    class Meta:
        verbose_name = 'Инспектор'
        verbose_name_plural = 'Инспекторы'


class PtoEngineer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    construction = models.ManyToManyField('Construction')

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'Инженер ПТО'
        verbose_name_plural = 'Инженеры ПТО'


class Project(models.Model):
    """Содержит информацию о проекте строитроительной документации, ссылается на строительный Объект"""
    id = models.AutoField(primary_key=True)
    constriction_object = models.CharField(max_length=5, default='AKU')
    code = models.CharField(max_length=4, default=0000)
    object_name = models.ForeignKey(Construction, on_delete=models.CASCADE)
    type_of_works = models.CharField(max_length=2,
                                     choices=[('AR', 'AR'), ('AS', 'AS'),
                                              ('KZ', 'KZ'), ('KM', 'KM'),
                                              ('TM', 'TM')])
    project_name = models.CharField(max_length=10)

    quality_plan = models.ForeignKey(QualityPlanNumber,
                                     on_delete=models.CASCADE,
                                     null=True,
                                     blank=True)

    def __str__(self):
        return f'{self.constriction_object}.{self.code}.{self.object_name}.0.{self.type_of_works}.{self.project_name}'

    def name(self):
        return f'{self.constriction_object}.{self.code}.{self.object_name}.0.{self.type_of_works}.{self.project_name}'

    def short(self):
        return f'{self.object_name}  {self.project_name}'

    class Meta:
        db_table = 'project_table'
        verbose_name = 'Проект'
        verbose_name_plural = 'Проекты'


class Akkuyu(models.Model):
    """Представитель заказчика для подписания ЗНО"""
    id = models.AutoField(primary_key=True)
    object_name = models.CharField(max_length=255)
    signer_name = models.CharField(max_length=200)

    def __str__(self):
        return self.signer_name

    class Meta:
        db_table = 'akkuyu_nuclear'


class RelationAkkuyuRFI(models.Model):
    """Отношение Заказчик-заказчикПодписантЗНО"""
    constraction_name = models.ForeignKey(Construction, on_delete=models.CASCADE)
    signer_name = models.CharField(max_length=200)

    def __str__(self):
        return self.signer_name

    class Meta:
        verbose_name = 'Представитель Аккую'
        verbose_name_plural = 'Представители Аккую'


class IndependentControl(models.Model):
    """Независимый контроль ссылается на строительный объект, настроить фильтрацию через внешнюю таблицу"""
    id = models.AutoField(primary_key=True)
    object_name = models.ForeignKey(Construction, on_delete=models.CASCADE)
    signer_name = models.CharField(max_length=200)

    def __str__(self):
        return self.signer_name

    class Meta:
        db_table = 'independent_control'


class RelationIndependentRFI(models.Model):
    """Отношение Независимый контроль - ЗНО"""
    construction_name = models.ForeignKey(Construction, on_delete=models.CASCADE)
    signer_name = models.CharField(max_length=200)

    def __str__(self):
        return self.signer_name

    class Meta:
        verbose_name = 'Независимый контроль'
        verbose_name_plural = 'Независимый контроль'


class DesignerSupervision(models.Model):
    """Авторский надзор, настроить фильтрацию через внешнюю таблицу"""
    id = models.AutoField(primary_key=True)
    object_name = models.ForeignKey(Construction, on_delete=models.CASCADE)
    signer_name = models.CharField(max_length=200)

    def __str__(self):
        return self.signer_name

    class Meta:
        db_table = 'designer_supervision'


class RelationSupervisionRFI(models.Model):
    """Relation between Designer Supervision and RFI"""
    construction_name = models.ForeignKey(Construction, on_delete=models.CASCADE)
    signer_name = models.CharField(max_length=200)

    def __str__(self):
        return self.signer_name

    class Meta:
        verbose_name = 'Авторский надзор'
        verbose_name_plural = 'Авторский надзор'


class RelationQaSignerRFI(models.Model):
    """Relation between Qa signer and RFI"""
    construction_name = models.ForeignKey(Construction, on_delete=models.CASCADE)
    signer_name = models.CharField(max_length=200)

    def __str__(self):
        return self.signer_name

    class Meta:
        verbose_name = 'Представитель Титан2/ДжейВИ'
        verbose_name_plural = 'Представители Титан2/ДжейВИ'


class QC(models.Model):
    """Контроль качества , человек. настроить фильтрацию через внешнюю таблицу"""
    id = models.AutoField(primary_key=True)
    object_name = models.ForeignKey(Construction, on_delete=models.CASCADE)
    signer_name = models.CharField(max_length=200)

    def __str__(self):
        return self.signer_name

    class Meta:
        db_table = 'qc_signer'


class Contractor(models.Model):
    """Исполнитель работ, человек подписант"""
    id = models.AutoField(primary_key=True)
    object_name = models.ForeignKey(Construction, on_delete=models.CASCADE)
    signer_name = models.CharField(max_length=200, default='-')

    def __str__(self):
        return self.signer_name

    class Meta:
        db_table = 'concractor'
        verbose_name = "Исполнитель работ"
        verbose_name_plural = "Исполнитель работ Титан2"


class RelationConstructionProject(models.Model):
    """Внешняя таблица для фильтрации строительный объект-Проба"""
    construction = models.ForeignKey(Construction, on_delete=models.CASCADE)
    test = models.ForeignKey(Project, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.construction} Project #{self.test}'


class DefaultSignersbyConstruction(models.Model):
    object_name = models.OneToOneField(Construction, on_delete=models.DO_NOTHING,
                                       verbose_name='Name of construction')
    akkuyy_signer = models.ForeignKey(RelationAkkuyuRFI, on_delete=models.DO_NOTHING,
                                      verbose_name='Name of akkuyu signer')
    independent_signer = models.ForeignKey(RelationIndependentRFI,
                                           on_delete=models.DO_NOTHING,
                                           verbose_name='Name of independent signer')
    supervision_signer = models.ForeignKey(RelationSupervisionRFI,
                                           on_delete=models.DO_NOTHING,
                                           verbose_name='Name of Designer signer')
    titan2_qc_signer = models.ForeignKey(RelationQaSignerRFI, on_delete=models.DO_NOTHING,
                                         verbose_name='Name of QC signer')
    titan2_contractor_signer = models.ForeignKey(Contractor,
                                                 on_delete=models.DO_NOTHING,
                                                 verbose_name='Name of Contractor signer')

    class Meta:
        db_table = 'rficrud_defaultsignersbyconstruction'

    def __str__(self):
        return f"Default signers for {self.object_name}"


class RFI(models.Model):
    """Основная таблица.
        Содержит всю необходимую информацию для составления ЗНО.
         Ссылается на таблицы: Строительный объект, Проект,
                                    План качества, 5 подписантов """
    id = models.AutoField(primary_key=True)
    excel_number = models.CharField(max_length=6, verbose_name='Эксель №')

    slug = models.SlugField(max_length=200, unique=True,
                            editable=False, null=True, blank=True)

    inspector = models.ForeignKey(Inspector, on_delete=models.SET_NULL, null=True,
                                  blank=True, verbose_name='Инспектор проводящий комиссию')

    rejected = 'rejected'
    accepted = 'accepted'
    in_process = 'in process'
    canceled = 'canceled'
    waiting = 'waiting for status'
    status_list = [
        (_(rejected), 'отказ'),
        (_(accepted), 'accepted'),
        (_(in_process), 'in process'),
        (_(canceled), 'canceled'),
        (_(waiting), 'Ожидание'),
    ]

    status = models.CharField(
        max_length=20,
        choices=status_list,
        default=waiting,
        verbose_name='Статус'
    )

    rfi_number_from_akkuyu = models.PositiveIntegerField(blank=True, null=True, verbose_name='Номер ЗНО')

    date_of_create = models.DateTimeField(verbose_name='Дата и Время создания')
    date_of_inspection = models.DateTimeField(verbose_name='Дата и Время проведения комиссии')

    object_name = models.ForeignKey(Construction, on_delete=models.CASCADE, verbose_name='Объект')
    # object_place = models.CharField(max_length=200, blank=True)

    project_name = models.ForeignKey(Project, on_delete=models.CASCADE,
                                     null=True, verbose_name='Имя Проекта')

    pk_points = models.CharField(max_length=8, default="H-H-H-H",
                                 choices=[('H-H-W-W', 'H-H-W-W'), ('H-H-R-R', 'H-H-R-R'),
                                          ('H-H-W-R', 'H-H-W-R'), ('H-H-H-H', 'H-H-H-H'),
                                          ('H-W-W-W', 'H-W-W-W')],
                                 blank=True, null=True,
                                 verbose_name="Точки из плана качества")

    type_of_work_list = ['Equipment', 'Piping', 'Civil',
                         'Painting', 'Structural', 'Electrical',
                         'Instrumentation', 'Insulation', 'QA/QC']

    type_of_work = models.CharField(max_length=255, blank=True, null=True, verbose_name='Тип работ')
    is_active_beton = models.BooleanField(default=False, help_text='Бетонирование',
                                          verbose_name='Бетонирование')

    description_of_work_russian = models.TextField(blank=True, verbose_name='Описание работы на русском')
    description_of_work_english = models.TextField(blank=True, verbose_name='Описание работы на английском')

    # quality_plan_code = models.CharField(max_length=255)

    akkuyu_signer = models.ForeignKey(RelationAkkuyuRFI,
                                      on_delete=models.DO_NOTHING,
                                      blank=True, null=True, verbose_name='Представитель заказчика на инспекции')
    independent_control = models.ForeignKey(RelationIndependentRFI,
                                            on_delete=models.DO_NOTHING, verbose_name='Независимный контроль')
    qc_signer = models.ForeignKey(RelationQaSignerRFI,
                                  on_delete=models.DO_NOTHING, verbose_name='Представитель Титан2/ДжейВИ')
    design_supervision_signer = models.ForeignKey(RelationSupervisionRFI,
                                                  on_delete=models.DO_NOTHING,
                                                  blank=True, null=True, verbose_name='Авторский надзор')
    contractor = models.ForeignKey(Contractor, on_delete=models.CASCADE,
                                   blank=True, null=True, verbose_name='Исполнитель')

    contractor_sintek = models.CharField(max_length=220, blank=True,
                                         null=True, verbose_name='Исполнитель Синтек',
                                         default='Серкан Кандемир /'
                                                 ' Serkan Kandemir +90 (552) '
                                                 '505-93-68')

    def __str__(self):
        return f'{self.date_of_inspection.date().strftime("%d %m %Y")} || RFI-{self.rfi_number_from_akkuyu}  '

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slug_create(self)
        # translator = Translator()
        #
        # result = translator.translate(self.description_of_work_russian, src='ru', dest='en')
        # self.description_of_work_english = result.text
        super(RFI, self).save(*args, **kwargs)

    @admin.display
    def rfi_number(self):
        colors = {
            'waiting for status': '3bc6d9f2',
            'accepted': '6bdb91',
            'canceled': 'baaf7552',
            'rejected': 'b31d27',
            'in process': 'ad9310'
        }
        return format_html(
            f'<span style="color: #{colors[self.status]};"> RFI-{self.rfi_number_from_akkuyu}</span>',

        )

    def short_description(self):
        return f'{self.description_of_work_russian[:50]} ...'

    class Meta:
        db_table = 'rfi_table'
        verbose_name = 'ЗНО'
        verbose_name_plural = 'Список ЗНО'


def slug_create(rfi):
    slug = slugify(rfi.excel_number)
    while RFI.objects.filter(slug=slug).exists():
        slug = slugify(rfi.excel_number + '-' + str(random.randint(1, 1000)))
    return slug


def create_copies_of_selected_rfis(modeladmin, request, queryset):
    def generate_excel_number():
        latest_rfi = RFI.objects.order_by('-excel_number').first()
        last_excel_number = latest_rfi.excel_number

        return int(last_excel_number) + 1

    for rfi in queryset:
        rfi_copy = rfi
        rfi_copy.pk = None
        rfi_copy.slug = slug_create(rfi_copy)
        rfi_copy.status = 'waiting for status'
        rfi_copy.rfi_number_from_akkuyu = None
        rfi_copy.excel_number = generate_excel_number()
        rfi_copy.date_of_create = datetime.now()
        rfi_copy.save()

    modeladmin.message_user(request, "Copies of selected RFIs have been created.")


create_copies_of_selected_rfis.short_description = "Создать копии выбраных RFIs"


class Comment(models.Model):
    rfi = models.ForeignKey(RFI, on_delete=models.CASCADE, related_name='comments')
    inspector = models.ForeignKey(Inspector, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'Comment by {self.inspector} on {self.rfi}'
