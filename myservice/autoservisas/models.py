from django.db import models

# Create your models here.
class AutomobilioModelis(models.Model):
    marke = models.CharField(verbose_name='Gamintojas', max_length=50)
    modelis = models.CharField(verbose_name='Modelis', max_length=50)

    def __str__(self):
        return f'{self.marke} {self.modelis}'

    class Meta:
        verbose_name = "Automobilio modelis"
        verbose_name_plural = "Automobilio modeliai"

class Paslauga(models.Model):
    pavadinimas = models.CharField(verbose_name='Pavadinimas', max_length=50)
    kaina = models.IntegerField(verbose_name='Kaina')

    def __str__(self):
        return self.pavadinimas

    class Meta:
        verbose_name = "Paslauga"
        verbose_name_plural = "Paslaugos"

from tinymce.models import HTMLField
class Automobilis(models.Model):
    valstybinis_nr = models.CharField(verbose_name='Valstybinis numeris', max_length=6)
    vin = models.CharField(verbose_name='VIN kodas', max_length=17)
    kliento_vardas = models.CharField(verbose_name='Savininkas', max_length=50)
    automobilio_modelis = models.ForeignKey(to='AutomobilioModelis', verbose_name='Automobilio modelis', on_delete=models.SET_NULL, null=True)
    photo = models.ImageField(verbose_name="Nuotrauka", upload_to='vehicles', null=True, blank=True) #arba tik blank=True
    description = HTMLField(verbose_name='Aprasymas', max_length=2000, default='')

    def __str__(self):
        return f'{self.automobilio_modelis} ({self.valstybinis_nr})'

    class Meta:
        verbose_name = "Automobilis"
        verbose_name_plural = "Automobiliai"


from django.contrib.auth.models import User
from datetime import date

class Uzsakymas(models.Model):
    data = models.DateTimeField(verbose_name='Data ir laikas', auto_now_add=True)
    automobilis = models.ForeignKey(to='Automobilis', verbose_name='Automobilis', on_delete=models.SET_NULL, null=True)
    klientas = models.ForeignKey(to=User, on_delete=models.SET_NULL, null=True, blank=True)
    grazinimo_data = models.DateField(verbose_name='Bus atlikta', null=True, blank=True)


    def total(self):
        total_suma = 0
        for line in self.lines.all():
            total_suma += line.suma()
        return total_suma

    LOAN_STATUS = (
        ('p', 'Patvirtinta'),
        ('v', 'Vykdoma'),
        ('a', 'Atsaukta'),
        ('t', 'Tvirtinama'),
        ('i', 'Ivykdyta'),
    )
    status = models.CharField(verbose_name="Busena", max_length=1, choices=LOAN_STATUS, blank=True, default='t')

    def is_overdue(self):
        return self.grazinimo_data and date.today() > self.grazinimo_data

    def __str__(self):
        return f'Priimta: [{self.data}], {self.automobilis}, grazinimas: [{self.grazinimo_data}]'

    class Meta:
        verbose_name = "Uzsakymas"
        verbose_name_plural = "Uzsakymai"

class UzsakymoEilute(models.Model):
    uzsakymas = models.ForeignKey(to='Uzsakymas', on_delete=models.CASCADE, related_name='lines')
    paslauga = models.ForeignKey(to='Paslauga', verbose_name='Paslauga', on_delete=models.SET_NULL, null=True)
    kiekis = models.IntegerField(verbose_name='Kiekis')

    def suma(self):
        return self.paslauga.kaina * self.kiekis

    def __str__(self):
        return f'{self.uzsakymas.automobilis} {self.uzsakymas.data}: {self.paslauga} - {self.kiekis}'

    class Meta:
        verbose_name = "Uzsakymo eilute"
        verbose_name_plural = "Uzsakymo eilutes"


class OrderReview(models.Model):
    uzsakymas = models.ForeignKey(to='Uzsakymas', verbose_name='Uzsakymas', on_delete=models.SET_NULL, null=True, blank=True, related_name='reviews')
    komentatorius = models.ForeignKey(to=User, on_delete=models.SET_NULL, null=True, blank=True)
    sukurimo_data = models.DateTimeField(verbose_name='Data', auto_now_add=True)
    komentaras = models.TextField(verbose_name='Atsiliepimas', max_length=3000)

    class Meta:
        verbose_name = 'Atsiliepimas'
        verbose_name_plural = 'Atsiliepimai'
        ordering = ['-sukurimo_data']


from PIL import Image
class Profilis(models.Model):
    vartotojas = models.OneToOneField(to=User, on_delete=models.CASCADE)
    nuotrauka = models.ImageField(verbose_name='Nuotrauka', upload_to='profile_pics', default='profile_pics/default.png')

    def __str__(self):
        return f'{self.vartotojas.username} profilis'

    class Meta:
        verbose_name = 'Profilis'
        verbose_name_plural = 'Profiliai'

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        super().save(force_insert, force_update, using, update_fields)
        img = Image.open(self.nuotrauka.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.nuotrauka.path)

