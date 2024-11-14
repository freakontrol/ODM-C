from django.db import models

# Create your models here.

class Plm(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    slug = models.SlugField(unique=True, max_length=200)
    
    def __str__ (self):
        return self.title

class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=3, unique=True)
    description = models.CharField(max_length=255, null=True, blank=True)
    is_component = models.BooleanField(default=False)
    is_document = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class Part(models.Model):
    id = models.AutoField(primary_key=True)
    internal_part_number = models.CharField(max_length=255, unique=True)
    description = models.CharField(max_length=255, null=True, blank=True)
    released = models.BooleanField(default=False)
    repository_link = models.CharField(max_length=255, null=True, blank=True)
    storage_code = models.CharField(max_length=255, null=True, blank=True)
    creation_date = models.DateField(auto_now_add=True)
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True)
    item_number = models.IntegerField(null=True, blank=True)
    variant = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    revision = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    image = models.BinaryField(null=True, blank=True)
    purchase_option = models.ForeignKey('PurchaseOption', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.internal_part_number

class PurchaseOption(models.Model):
    id = models.AutoField(primary_key=True)
    part_ipn = models.ForeignKey('Part', on_delete=models.CASCADE, null=True)
    manufacturer = models.CharField(max_length=255, null=True, blank=True)
    manufacturer_code = models.CharField(max_length=255, null=True, blank=True)
    datasheet = models.CharField(max_length=255, null=True, blank=True)
    obsolete = models.BooleanField(default=False)

class Container(models.Model):
    id = models.AutoField(primary_key=True)
    part_a = models.ForeignKey('Part', on_delete=models.CASCADE, related_name='containers_as_part_a')
    part_b = models.ForeignKey('Part', on_delete=models.CASCADE, related_name='containers_as_part_b')
    quantity = models.IntegerField()
    creation_date = models.DateField(auto_now_add=True)

    class Meta:
        unique_together = ('part_a', 'part_b',)

class Document(models.Model):
    id = models.AutoField(primary_key=True)
    document_number = models.CharField(max_length=255, unique=True)
    description = models.CharField(max_length=255, null=True, blank=True)
    checked = models.BooleanField(default=False)
    doc_file = models.BinaryField(null=True, blank=True)
    link = models.CharField(max_length=255, null=True, blank=True)
    obsolete = models.BooleanField(default=False)
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True)
    item_number = models.IntegerField(null=True, blank=True)
    revision = models.CharField(max_length=255, null=True, blank=True)
    creation_date = models.DateField(auto_now_add=True)

class PartDocument(models.Model):
    id = models.AutoField(primary_key=True)
    part = models.ForeignKey('Part', on_delete=models.CASCADE)
    document = models.ForeignKey('Document', on_delete=models.CASCADE)