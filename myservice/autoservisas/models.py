from django.db import models

# Create your models here.
class AutomobilioModelis(models.Model):
    marke = models.CharField(verbose_name='Gamintojas', max_length=50)
    modelis = models.CharField(verbose_name='Modelis', max_length=50)

    def __str__(self):
        return f'{self.marke} {self.modelis}'

class Paslauga(models.Model):
    pavadinimas = models.CharField(verbose_name='Pavadinimas', max_length=50)
    kaina = models.IntegerField(verbose_name='Kaina')

    def __str__(self):
        return self.pavadinimas

class Automobilis(models.Model):
    valstybinis_nr = models.CharField(verbose_name='Valstybinis numeris', max_length=6)
    vin = models.CharField(verbose_name='VIN kodas', max_length=17)
    kliento_vardas = models.CharField(verbose_name='Savininkas', max_length=50)
    automobilio_modelis = models.ForeignKey(to='AutomobilioModelis', verbose_name='Automobilio modelis', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f'{self.automobilio_modelis} ({self.valstybinis_nr})'

class Uzsakymas(models.Model):
    data = models.DateTimeField(verbose_name='Data ir laikas', auto_now_add=True)
    automobilis = models.ForeignKey(to='Automobilis', verbose_name='Automobilis', on_delete=models.SET_NULL, null=True)


    def __str__(self):
        return f'{self.data} ({self.automobilis})'

class UzsakymoEilute(models.Model):
    uzsakymas = models.ForeignKey(to='Uzsakymas', on_delete=models.CASCADE)
    paslauga = models.ForeignKey(to='Paslauga', verbose_name='Paslauga', on_delete=models.SET_NULL, null=True)
    kiekis = models.IntegerField(verbose_name='Kiekis')

    def __str__(self):
        return f'{self.uzsakymas.automobilis} {self.uzsakymas.data}: {self.paslauga} - {self.kiekis}'