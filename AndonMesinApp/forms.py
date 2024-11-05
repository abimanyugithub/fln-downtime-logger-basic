from django import forms
from .models import Mesin, KategoriMesin, Departemen, Role


class KategoriForm(forms.ModelForm):
    class Meta:
        model = KategoriMesin
        fields = [
            'kategori',
        ]

        labels = {
            'kategori': 'Category name',
        }

        widgets = {
            'kategori': forms.TextInput(attrs={'class': 'form-control mt-2 mb-2', 'required': 'required'}),
        }


class MesinForm(forms.ModelForm):
    class Meta:
        model = Mesin
        fields = [
            'kategori',
            'nomor_mesin',
        ]

        labels = {
            'kategori': 'Select category',
            'nomor_mesin': 'Machine number',
        }

        widgets = {
            'nomor_mesin': forms.TextInput(attrs={'class': 'form-control mt-2 mb-2', 'required': 'required'}),
            'kategori': forms.Select(attrs={'class': 'form-control mt-2 mb-2 bg-light text-muted', 'readonly': 'readonly'}),
        }

class DepartemenForm(forms.ModelForm):
    class Meta:
        model = Departemen
        fields = [
            'departemen',
        ]

        labels = {
            'departemen': 'Department name',
        }

        widgets = {
            'departemen': forms.TextInput(attrs={'class': 'form-control mt-2 mb-2', 'required': 'required'}),
        }

class PeranForm(forms.ModelForm):
    class Meta:
        model = Role
        fields = [
            'nama_role',
            'departemen',
            # 'area_kerja',
        ]

        labels = {
            # 'area_kerja': 'Working Area',
            'departemen': 'Select departemen',
            'nama_role': 'Role name',
        }

        widgets = {
            'nama_role': forms.TextInput(attrs={'class': 'form-control mt-2 mb-2', 'required': 'required'}),
            'departemen': forms.Select(attrs={'class': 'form-control mt-2 mb-2 bg-light text-muted', 'readonly': 'readonly'}),
            # 'area_kerja': forms.Select(attrs={'class': 'form-control mt-2 mb-2 bg-light text-muted'}),
        }