from dal import autocomplete
from .models import Construction, Project


class ObjectAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Construction.objects.all()

        if self.q:
            qs = qs.filter(name__icontains=self.q)
        return qs


class ProjectAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Project.objects.all()

        if self.q:
            qs = qs.filter(name__icontains=self.q)
        return qs