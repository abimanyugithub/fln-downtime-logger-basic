from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, ListView
from .models import Mesin, KategoriMesin, Departemen, Role
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import HttpResponse, HttpResponseForbidden, JsonResponse, Http404
from .forms import MesinForm, KategoriForm, DepartemenForm, PeranForm

class ViewDashboard(TemplateView):
    template_name = 'AndonMesinApp/dashboard.html'

class RegisterKategori(CreateView):
    template_name = 'AndonMesinApp/CrudKategori/register-kategori.html'
    model = KategoriMesin
    form_class = KategoriForm
    success_url = reverse_lazy('list_kategori')

class ListKategori(ListView):
    template_name = 'AndonMesinApp/CrudKategori/list-kategori.html'
    model = KategoriMesin
    context_object_name = 'kategori_list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['fields'] = {'kategori': 'Category'}
        return context

class RegisterMesin(CreateView):
    template_name = 'AndonMesinApp/CrudMesin/register-mesin.html'
    model = Mesin
    form_class = MesinForm
    success_url = reverse_lazy('list_mesin')

class ListMesin(ListView):
    template_name = 'AndonMesinApp/CrudMesin/list-mesin.html'
    model = Mesin
    context_object_name = 'mesin_list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['fields'] = {'kategori': 'Category', 'nomor_mesin': 'Machine No.'}
        return context

class RegisterDepartemen(CreateView):
    template_name = 'AndonMesinApp/CrudDepartemen/register-departemen.html'
    model = Departemen
    form_class = DepartemenForm
    success_url = reverse_lazy('list_departemen')

class ListDepartemen(ListView):
    template_name = 'AndonMesinApp/CrudDepartemen/list-departemen.html'
    model = Departemen
    context_object_name = 'departemen_list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['fields'] = {'departemen': 'Department'}
        return context
    
class RegisterPeran(CreateView):
    template_name = 'AndonMesinApp/CrudRole/register-role.html'
    model = Role
    form_class = PeranForm
    success_url = reverse_lazy('list_kategori')

class ListPeran(ListView):
    template_name = 'AndonMesinApp/CrudRole/list-role.html'
    model = Role
    context_object_name = 'peran_list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['fields'] = {'departemen': 'Department', 'nama_role': 'Role name'}
        return context

@csrf_exempt
def ReceiveData(request):
    if request.method == 'POST':
        try:
            # Load the incoming JSON data
            data = json.loads(request.body)
            
            # Extract fields from the data
            no_machine = data.get('nomor_mesin')
            category = data.get('kategori')
            role_name = data.get('role_name')

        except json.JSONDecodeError:
            return JsonResponse({"status": "error", "message": "Invalid JSON"}, status=400)
