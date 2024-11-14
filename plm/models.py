from django.db import models

# Create your models here.

# class Plm(models.Model):
#     title = models.CharField(max_length=200)
#     content = models.TextField()
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#     slug = models.SlugField(unique=True, max_length=200)
    
#     def __str__ (self):
#         return self.title

class Category(models.Model):
    id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=3, unique=True)
    description = models.CharField(max_length=255, null=True, blank=True)
    is_comp = models.BooleanField(default=False)
    is_doc = models.BooleanField(default=False)

    def __str__(self):
        return self.category_name

class AlternativaParte(models.Model):
    id = models.AutoField(primary_key=True)
    ipn = models.ForeignKey('PartMaster', on_delete=models.CASCADE, null=True, related_name='alternative_parts')
    produttore = models.CharField(max_length=255, null=True, blank=True)
    codice_produttore = models.CharField(max_length=255, null=True, blank=True)
    datasheet = models.CharField(max_length=255, null=True, blank=True)
    obsoleto = models.BooleanField(default=False)

class PartMaster(models.Model):
    id = models.AutoField(primary_key=True)
    ipn = models.CharField(max_length=255, unique=True)
    descrizione = models.CharField(max_length=255, null=True, blank=True)
    produttore = ArrayField(models.CharField(max_length=255), default=list, blank=True)
    codice_produttore = ArrayField(models.CharField(max_length=255), default=list, blank=True)
    datasheet = ArrayField(models.CharField(max_length=255), default=list, blank=True)
    indice_alternativa = models.IntegerField(default=1)
    released = models.BooleanField(default=False)
    link_repo = models.CharField(max_length=255, null=True, blank=True)
    codice_magazzino = models.CharField(max_length=255, null=True, blank=True)
    create_time = models.DateField(auto_now_add=True)
    obsoleto = ArrayField(models.BooleanField(), default=list, blank=True)
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True)
    id_number = models.IntegerField(null=True, blank=True)
    variante = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    revisione = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    origin_project = models.ForeignKey('Project', on_delete=models.SET_NULL, null=True, to_field='project_name')
    image = models.BinaryField(null=True, blank=True)

    def __str__(self):
        return self.ipn

class ContainerMaster(models.Model):
    id = models.AutoField(primary_key=True)
    ipn_a = models.ForeignKey('PartMaster', on_delete=models.CASCADE, related_name='containers_as_ipn_a')
    ipn_b = models.ForeignKey('PartMaster', on_delete=models.CASCADE, related_name='containers_as_ipn_b')
    qnty = models.IntegerField()
    create_time = models.DateField(auto_now_add=True)

    class Meta:
        unique_together = ('ipn_a', 'ipn_b',)

class Docs(models.Model):
    id = models.AutoField(primary_key=True)
    idn = models.CharField(max_length=255, unique=True)
    descrizione = models.CharField(max_length=255, null=True, blank=True)
    checked = models.BooleanField(default=False)
    drawing_file = models.BinaryField(null=True, blank=True)
    link = models.CharField(max_length=255, null=True, blank=True)
    obsoleto = models.BooleanField(default=False)
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True)
    id_number = models.IntegerField(null=True, blank=True)
    revisione = models.CharField(max_length=255, null=True, blank=True)
    create_time = models.DateField(auto_now_add=True)

class PartDoc(models.Model):
    id = models.AutoField(primary_key=True)
    ipn = models.ForeignKey('PartMaster', on_delete=models.CASCADE)
    idn = models.ForeignKey('Docs', on_delete=models.CASCADE, to_field='id')
