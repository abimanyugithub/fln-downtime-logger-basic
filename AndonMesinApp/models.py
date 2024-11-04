from django.db import models

# Create your models here.
class KategoriMesin(models.Model):
    kategori = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.kategori

class Mesin(models.Model):
    kategori = models.ForeignKey(KategoriMesin, on_delete=models.CASCADE)
    nomor_mesin = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.kategori} - {self.nomor_mesin}'
    
class Departemen(models.Model):
    departemen =  models.CharField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.departemen

class Role(models.Model):
    departemen = models.ForeignKey(Departemen, on_delete=models.CASCADE)
    nama_role = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.nama_role
