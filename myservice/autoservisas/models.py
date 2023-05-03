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

class Automobilis(models.Model):
    valstybinis_nr = models.CharField(verbose_name='Valstybinis numeris', max_length=6)
    vin = models.CharField(verbose_name='VIN kodas', max_length=17)
    kliento_vardas = models.CharField(verbose_name='Savininkas', max_length=50)
    automobilio_modelis = models.ForeignKey(to='AutomobilioModelis', verbose_name='Automobilio modelis', on_delete=models.SET_NULL, null=True)
    photo = models.ImageField(verbose_name="Nuotrauka", upload_to='vehicles', null=True, blank=True) #arba tik blank=True

    def __str__(self):
        return f'{self.automobilio_modelis} ({self.valstybinis_nr})'

    class Meta:
        verbose_name = "Automobilis"
        verbose_name_plural = "Automobiliai"

class Uzsakymas(models.Model):
    data = models.DateTimeField(verbose_name='Data ir laikas', auto_now_add=True)
    automobilis = models.ForeignKey(to='Automobilis', verbose_name='Automobilis', on_delete=models.SET_NULL, null=True)

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

    def __str__(self):
        return f'{self.data} ({self.automobilis})'

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