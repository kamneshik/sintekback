from django.shortcuts import render, get_object_or_404, \
    HttpResponseRedirect, redirect, reverse
from django.utils import timezone
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.utils.text import slugify
from .models import RFI, Project, Construction, Inspector, Comment, DefaultSignersbyConstruction
from .forms import RfiFilterForm, CommentForm, RFICreateForm
from django.db.models import Q
from datetime import datetime, timedelta
import pytz
from django.views.generic.edit import CreateView
from .autocomplete import ObjectAutocomplete
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import random
from django_filters.rest_framework import DjangoFilterBackend
from .filter import RFIFilter
from django.db.models import Value, CharField
from django.db.models.functions import Concat
from django import template
from dal import autocomplete

from rest_framework import viewsets, filters
from rest_framework.response import Response
from rest_framework.decorators import api_view, action
from .serializers import RFISerializer, \
    DefaultSignersConstructionSerializer, ProjectSerializer

register = template.Library()

from .serializers import CustomTokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            refresh = RefreshToken.for_user(user)
            return Response({'access-token': str(refresh.access_token)})
        else:
            return Response({'error': 'Invalid credentials'}, status=400)


@register.filter
def has_group(user, group_name):
    return user.groups.filter(name=group_name).exists()


@login_required
def add_comment(request, rfi_slug):
    rfi = get_object_or_404(RFI, slug=rfi_slug)

    if request.method == 'POST':
        comment_text = request.POST.get('comment', '').strip()

        if comment_text:
            # Get the Inspector instance associated with the logged-in user
            inspector = get_object_or_404(Inspector, user=request.user)

            comment = Comment(
                rfi=rfi,
                inspector=inspector,
                text=comment_text,
            )
            comment.save()

    return redirect('rficrud:single_rfi_read', rfi_slug=rfi.slug)


def update_rfi_status(request, rfi_id, new_status):
    if request.method == 'POST':
        print('We entered here')
        # Check if the user has the necessary permission to update the status
        if request.user.groups.filter(name='Inspectors').exists():
            rfi = get_object_or_404(RFI, id=rfi_id)
            rfi.status = new_status
            rfi.save()
            print('We are very soon', new_status)
            return JsonResponse(
                {'status': 'success', 'update_status': 'new_status', 'message': 'Status updated successfully'})
        else:
            return JsonResponse({'status': 'error', 'message': "You dont have permission to update the status"})
    print("we are not entered")
    # Return an error response for other request methods or non-AJAX requests
    return JsonResponse({'status': 'error', 'message': 'Invalid request'})


class RFIViewSet(viewsets.ModelViewSet):
    queryset = RFI.objects.all().order_by('-excel_number')
    serializer_class = RFISerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = RFIFilter


class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['object_name']

    def get_queryset(self):
        queryset = super().get_queryset()

        object_name = self.request.query_params.get('object-name')

        if object_name:
            queryset = queryset.filter(object_name__object_name=object_name)

        return queryset


def mainpage(request):
    """Функция для главной страницы. Ведомость ///
            ДОДЕЛАТЬ: отображение по датам и отображение по номеру"""

    rfi_data = RFI.objects.all().order_by('-date_of_create')
    return render(request, template_name='rficrud/index.html')


def rfi_list(request):
    filter_form = RfiFilterForm(request.GET or None)
    rfis = RFI.objects.all().order_by('-excel_number')

    if filter_form.is_valid():
        object_name = request.GET.get('object_name')
        project_name = request.GET.get('project_name')
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')
        status = filter_form.cleaned_data.get('status')
        inspector_name = request.GET.get('inspector_filter')

        # if object_name:
        #     rfis = rfis.filter(object_name__object_name__icontains=object_name)
        if inspector_name:
            rfis = rfis.filter(inspector__user__username=inspector_name)

        else:
            if object_name:
                rfis = rfis.filter(object_name_id=object_name)

            if project_name:
                rfis = rfis.filter(project_name_id=project_name)

            if start_date:
                rfis = rfis.filter(date_of_create__gte=start_date)

            if end_date:
                rfis = rfis.filter(date_of_create__lte=end_date)

            # if start_date and end_date:
            #     start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
            #     end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
            #     start_datetime = timezone.make_aware(datetime.combine
            #                                          (start_date, datetime.min.time()), pytz.timezone('Europe/Moscow'))
            #     end_datetime = timezone.make_aware(datetime.combine
            #                                        (end_date, datetime.max.time()), pytz.timezone('Europe/Moscow'))
            #     rfis = rfis.filter(date_of_create__range=(start_datetime, end_datetime))
            # elif start_date:
            #     start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
            #     rfis = rfis.filter(date_of_create__date=start_date)

            if status:
                rfis = rfis.filter(status=status)

    paginator = Paginator(rfis, 20)

    page = request.GET.get('page')

    try:
        rfis_page = paginator.page(page)
    except PageNotAnInteger:
        rfis_page = paginator.page(1)
    except EmptyPage:
        rfis_page = paginator.page(paginator.num_pages)

    context = {'rfis_page': rfis_page, 'filter_form': filter_form}
    return render(request, 'rficrud/rfi_list.html', context)


def inspector_view(request, username):
    filter_form = RfiFilterForm(request.GET or None)
    print(username)
    rfis = RFI.objects.filter(inspector__user__username=username).order_by("-excel_number")
    if request.method == 'GET':
        print(username, ': Inspector')

    if filter_form.is_valid():
        object_name = request.GET.get('object_name')
        project_name = request.GET.get('project_name')
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')
        status = filter_form.cleaned_data.get('status')
        inspector_name = request.GET.get('inspector_filter')
        print('Inspector: ', username)
        # if object_name:
        #     rfis = rfis.filter(object_name__object_name__icontains=object_name)

        if object_name:
            rfis = rfis.filter(object_name_id=object_name)

        if project_name:
            rfis = rfis.filter(project_name_id=project_name)

        if start_date:
            rfis = rfis.filter(date_of_inspection__gte=start_date)

        if end_date:
            rfis = rfis.filter(date_of_inspection__lte=end_date)

        # if start_date and end_date:
        #     start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
        #     end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
        #     start_datetime = timezone.make_aware(datetime.combine
        #                                          (start_date, datetime.min.time()), pytz.timezone('Europe/Moscow'))
        #     end_datetime = timezone.make_aware(datetime.combine
        #                                        (end_date, datetime.max.time()), pytz.timezone('Europe/Moscow'))
        #     rfis = rfis.filter(date_of_create__range=(start_datetime, end_datetime))
        # elif start_date:
        #     start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
        #     rfis = rfis.filter(date_of_create__date=start_date)

        if status:
            rfis = rfis.filter(status=status)

    update_rfi_status_url = reverse('rficrud:update_rfi_status', args=[0, 'placeholder'])
    print(update_rfi_status_url)
    context = {'rfis': rfis, 'filter_form': filter_form,
               'update_rfi_status_url': update_rfi_status_url,
               }
    return render(request, 'rficrud/inspector_view.html', context)


class DefaultSignersConstructionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = DefaultSignersbyConstruction.objects.filter()
    serializer_class = DefaultSignersConstructionSerializer

    @action(detail=False, methods=['GET'], url_path='one-object')
    def def_signers(self, request):
        print("we here")
        construction_name = request.query_params.get('object-name')
        print(construction_name)
        if construction_name is not None:
            # get the Construction object with the given object_name
            # construction = get_object_or_404(Construction, object_id=construction_id)
            # get the DefaultSignersbyConstruction object related to the Construction object
            response = get_object_or_404(DefaultSignersbyConstruction, object_name__object_name=construction_name)
            serializer = self.serializer_class(response)
            return Response(serializer.data)
        else:
            return Response({'error': 'Construction code (constr) is missing.'})


def get_projects_by_object(request, object_id):
    if request.method == "GET":
        projects = Project.objects.filter(object_name__id=object_id)
        empty_label = {'id': '', 'name': 'All projects'}
        project_list = [{'id': project.id, 'name': project.name()} for project in projects]
        # project_list.append(empty_label)
    else:
        project_list = []
    return JsonResponse(project_list, safe=False)


def rfi_create(request):
    if request.method == 'POST':
        form = RFICreateForm(request.POST)
        if form.is_valid():
            rfi = form.save()
            # Perform any additional processing or redirect to a success page
            return redirect('rfi_list/', rfi_slug=rfi.slug)
    else:
        form = RFICreateForm()

    return render(request, 'rficrud/rfi_create.html', {'form': form})


class RFICreateView(CreateView):
    model = RFI
    form_class = RFICreateForm
    template_name = 'rficrud/rfi_create.html'
    success_url = '/rfi_list/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_autocomplete_url'] = reverse('rficrud:object_autocomplete')
        return context

    def generate_excel_number(self):
        latest_rfi = RFI.objects.order_by('-excel_number').first()
        last_excel_number = latest_rfi.excel_number

        return int(last_excel_number) + 1

    def form_valid(self, form):
        # Получение данных из формы
        beton_work = form.cleaned_data['beton_work']
        executive_scheme = form.cleaned_data['executive_scheme']
        axes = form.cleaned_data['axes']
        from_elevation = form.cleaned_data['from_elevation']
        # description_of_work_russian = form.description_of_work_russian['description_of_work_russian']

        rfi = form.save(commit=False)
        rfi.date_of_create = datetime.now()
        rfi.excel_number = self.generate_excel_number()  # Замените на свою логику генерации номера
        if executive_scheme:
            rfi.description_of_work_russian += f" согласно исполнительной схеме {rfi.project_name}-SINTEK-ABD"
        # rfi.beton_work = beton_work
        # rfi.description_of_work_russian = executive_scheme
        # rfi.axes = axes
        # rfi.elevation = elevation
        rfi.save()

        return redirect('excelfiles:success')


def search(request):
    query = request.GET.get('q', '')  # Get the search query parameter from the request
    related_field = request.GET.get('related_field')  # Get the related field parameter from the request
    results = []

    if related_field == '#project':
        # Filter the projects based on the selected object
        object_id = request.GET.get('object_id')
        projects = Project.objects.filter(object_id=object_id, name__icontains=query)
        for project in projects:
            results.append({'id': project.id, 'text': project.name})
    else:
        # Perform a general search
        constructions = Construction.objects.filter(name__icontains=query)
        for construction in constructions:
            results.append({'id': construction.id, 'text': construction.name})

    return JsonResponse(results, safe=False)


def slug_create(request):
    rfis = RFI.objects.all()
    data = []
    for rfi in rfis:
        slug = slugify(rfi.excel_number)

        while RFI.objects.filter(slug=slug).exists():
            slug = slugify(rfi.excel_number + '-' + str(random.randint(1, 1000)))

        data.append(slug)
        rfi.slug = slug
        rfi.save()

    return JsonResponse(data, safe=False)


def single_rfi_read(request, rfi_slug):
    """
    Функция отображения
    :param request:
    :param rfi_slug:
    :return:
    """
    rfi = get_object_or_404(RFI, slug=rfi_slug)
    is_inspector = request.user.groups.filter(name='Inspectors').exists()

    if is_inspector:
        inspector, created = Inspector.objects.get_or_create(user=request.user)
    else:
        inspector = None

    if request.method == 'POST' and is_inspector:
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.rfi = rfi
            comment.inspector = inspector
            comment.save()
            return redirect('rficrud:single_rfi_read', rfi_slug=rfi_slug)
    else:
        form = CommentForm()

    comments = Comment.objects.filter(rfi=rfi)
    context = {'rfi': rfi, 'form': form,
               'is_inspector': is_inspector,
               'comments': comments}
    return render(request, 'rficrud/single_rfi.html', context=context)
