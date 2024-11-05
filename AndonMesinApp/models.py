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
    status = models.CharField(max_length=255, default='ready')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.kategori} - {self.nomor_mesin}'
    
class Departemen(models.Model):
    departemen =  models.CharField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.departemen

class Role(models.Model):
    # area_kerja = models.ForeignKey(KategoriMesin, on_delete=models.CASCADE, blank=True, null=True)
    departemen = models.ForeignKey(Departemen, on_delete=models.CASCADE)
    nama_role = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.nama_role
    
class Downtime(models.Model):
    mesin = models.ForeignKey(Mesin, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=255, default='waiting')

    def duration(self):
        """Calculate the duration of the downtime."""
        if self.start_time and self.end_time:
            return self.end_time - self.start_time
        return None

    def __str__(self):
        return f"Downtime from {self.start_time} to {self.end_time}"
