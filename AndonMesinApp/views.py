import json
import requests
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, ListView, UpdateView
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, HttpResponseForbidden, JsonResponse, Http404
from django.utils import timezone
from django.db.models import Q
from django.conf import settings
from .models import Mesin, KategoriMesin, Departemen, Role, Downtime
from .forms import MesinForm, KategoriForm, DepartemenForm, PeranForm
from datetime import timedelta
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


# fungsi kirim grup telegram
def send_telegram_message(message):
    bot_token = settings.TELEGRAM_API_TOKEN
    chat_id = '-1002408042848' # id grup
    
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        'chat_id': chat_id,
        'text': message
    }
    response = requests.post(url, data=payload)
    
    if response.status_code == 200:
        print("Message sent successfully")
    else:
        print("Failed to send message")            

class ViewDashboard(TemplateView):
    template_name = 'AndonMesinApp/dashboard.html'

    def get_context_data(self, **kwargs):
        # Call the superclass method to get the base context
        context = super().get_context_data(**kwargs)
        mesin_list = Mesin.objects.all().order_by('-kategori', 'nomor_mesin')

        for item in mesin_list:
            
            if item.status == "running":
                item.color = "success text-white"
            elif item.status == "downtime":
                item.color = "warning text-dark"
            else:
                item.color = "secondary text-white"

        context['mesin_list'] = mesin_list

        return context

'''
class ViewDashboard(ListView):
    template_name = 'AndonMesinApp/dashboard.html'
    model = Mesin
    context_object_name = 'mesin_list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['fields'] = {'kategori': 'Category', 'nomor_mesin': 'Machine No.'}
        return context
'''

class RegisterKategori(CreateView):
    template_name = 'AndonMesinApp/CrudKategori/register-kategori.html'
    model = KategoriMesin
    form_class = KategoriForm
    success_url = reverse_lazy('list_kategori')

class UpdateKategori(UpdateView):
    template_name = 'AndonMesinApp/CrudKategori/register-kategori.html'
    model = KategoriMesin
    form_class = KategoriForm
    success_url = reverse_lazy('list_kategori')

class ListKategori(ListView):
    template_name = 'AndonMesinApp/CrudKategori/list-kategori.html'
    model = KategoriMesin
    context_object_name = 'kategori_list'
    ordering = ['kategori']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['fields'] = {'kategori': 'Category'}
        return context

class RegisterMesin(CreateView):
    template_name = 'AndonMesinApp/CrudMesin/register-mesin.html'
    model = Mesin
    form_class = MesinForm
    success_url = reverse_lazy('list_mesin')

class UpdateMesin(UpdateView):
    template_name = 'AndonMesinApp/CrudMesin/register-mesin.html'
    model = Mesin
    form_class = MesinForm
    success_url = reverse_lazy('list_mesin')

class ListMesin(ListView):
    template_name = 'AndonMesinApp/CrudMesin/list-mesin.html'
    model = Mesin
    context_object_name = 'mesin_list'
    ordering = ['-kategori', 'nomor_mesin']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['fields'] = {'kategori': 'Category', 'nomor_mesin': 'Machine No.'}
        return context

class RegisterDepartemen(CreateView):
    template_name = 'AndonMesinApp/CrudDepartemen/register-departemen.html'
    model = Departemen
    form_class = DepartemenForm
    success_url = reverse_lazy('list_departemen')

class UpdateDepartemen(UpdateView):
    template_name = 'AndonMesinApp/CrudDepartemen/register-departemen.html'
    model = Departemen
    form_class = DepartemenForm
    success_url = reverse_lazy('list_departemen')

class ListDepartemen(ListView):
    template_name = 'AndonMesinApp/CrudDepartemen/list-departemen.html'
    model = Departemen
    context_object_name = 'departemen_list'
    ordering = ['departemen']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['fields'] = {'departemen': 'Department'}
        return context
    
class RegisterPeran(CreateView):
    template_name = 'AndonMesinApp/CrudRole/register-role.html'
    model = Role
    form_class = PeranForm
    success_url = reverse_lazy('list_role')

class UpdatePeran(UpdateView):
    template_name = 'AndonMesinApp/CrudRole/register-role.html'
    model = Role
    form_class = PeranForm
    success_url = reverse_lazy('list_role')

class ListPeran(ListView):
    template_name = 'AndonMesinApp/CrudRole/list-role.html'
    model = Role
    context_object_name = 'peran_list'
    ordering = ['nama_role', '-departemen']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['fields'] = {'nama_role': 'Role name', 'departemen': 'Department'}
        return context
    
class ListDowntime(TemplateView):
    template_name = 'AndonMesinApp/CrudDowntime/list-downtime.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['fields'] = {'mesin': 'Mesin', 'role': 'Role', 'start_time': 'Start time', 'end_time': 'End time', 'status': 'Status', 'duration': 'Duration'}
        
        return context

# menapilkan card di dashboard
def AsyncMesinCard(request):
    mesin_list = Mesin.objects.all().order_by('-kategori', 'nomor_mesin')

    for item in mesin_list:
        if item.status == "running":
            item.color = "success text-white"
        elif item.status == "downtime":
            item.color = "warning text-dark"
        else:
            item.color = "secondary text-white"

    return render(request, 'AndonMesinApp/HtmxPartial/list-card-mesin.html', {'mesin_list': mesin_list})

# menampilkan list downtime
def AsyncDowntimeList(request):
    downtime_list = Downtime.objects.all().order_by('-start_time')
    return render(
        request,
        'AndonMesinApp/HtmxPartial/list-downtime.html',  # Path to the partial template for rendering downtime data
        {
            'downtime_list': downtime_list,  # Context variable containing the downtime entries
            'fields': {  # Add the field names like you did in the context of the class-based view
                'mesin': 'Mesin',
                'role': 'Role',
                'start_time': 'Start time',
                'end_time': 'End time',
                'status': 'Status',
                'duration': 'Duration'
            }
        }
    )

class Esp32EndpointView(APIView):

    # @csrf_exempt
    def post(self, request):
        try:
            # Memuat data JSON yang dikirimkan dalam request body
            # data = json.loads(request.body)
            # Data JSON sudah otomatis diparse oleh DRF menjadi request.data
            data = request.data  
            
            # Mencetak data yang diterima untuk debugging
            print("Received data:", data)
            
            # Mengambil data dari JSON yang diterima
            no_machine = data.get('no_machine')
            category = data.get('category')
            role_name = data.get('role_name')
            department = data.get('department')
            status = data.get('status')

            # Mengambil objek Mesin dan Role sesuai dengan data yang diterima
            mesin = get_object_or_404(Mesin, nomor_mesin=no_machine, kategori__kategori=category)
            peran = get_object_or_404(Role, nama_role=role_name, departemen__departemen=department)

            # Jika status downtime "mulai"
            if status == 'mulai':
                # Jika status mesin adalah running, ubah statusnya menjadi downtime
                if mesin.status == "running":
                    mesin.status = 'downtime'
                    mesin.save()

                # Membuat entri downtime baru
                downtime = Downtime.objects.create(
                    mesin=mesin,
                    role=peran,
                    start_time=timezone.now()
                )

                # Mengirim notifikasi ke grup Telegram
                message = f"⚠️ Downtime Alert for Machine\n\n"
                message += f"Machine: {mesin.kategori} - {mesin.nomor_mesin}\n"
                message += f"Status: {mesin.status.capitalize()}\n"
                message += f"Downtime started at: {downtime.start_time.strftime('%d-%m-%Y %H:%M')}\n"
                message += f"Role: {downtime.role}\n"
                send_telegram_message(message)

            # Jika status downtime "selesai"
            elif status == 'selesai':

                # Mencari downtime yang sedang dalam status "waiting"
                downtime_update = Downtime.objects.filter(mesin=mesin, role=peran, status='waiting').first()
                downtime_update.end_time = timezone.now()
                downtime_update.status = 'done'
                downtime_update.save()

                # Memeriksa apakah ada downtime lain yang sedang dalam status "waiting"
                cek_status_mesin = Downtime.objects.filter(mesin=mesin, status='waiting').exists()

                # Jika tidak ada downtime lain, update status mesin menjadi "running"
                if not cek_status_mesin:
                    mesin.status = "running"
                    mesin.save()

                # Mengirimkan notifikasi ke grup Telegram
                message = f"✅ Downtime Finished for Machine\n\n"
                message += f"Machine: {mesin.kategori} - {mesin.nomor_mesin}\n"
                message += f"Status: {mesin.status.capitalize()}\n"
                message += f"Downtime started at: {downtime_update.start_time.strftime('%d-%m-%Y %H:%M')}\n"
                message += f"Downtime ended at: {downtime_update.end_time.strftime('%d-%m-%Y %H:%M')}\n"
                message += f"Role: {downtime_update.role}\n"
                message += f"Duration: {str(downtime_update.duration()).split('.')[0]}\n"
                send_telegram_message(message)

            # Mengirimkan data sebagai response dalam format JSON
            response_data = {
                "status": "success",
                "message": "Data received successfully",
                "received_data": data  # Menambahkan data yang diterima dalam response
            }
            return JsonResponse(response_data)
        
        except json.JSONDecodeError:
            return Response({"status": "error", "message": "Invalid JSON data"}, status=400)
        except Exception as e:
            return Response({"status": "error", "message": str(e)}, status=500)