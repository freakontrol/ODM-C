from django.db import models

class Category(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=3, unique=True)
    description = models.CharField(max_length=255, null=True, blank=True)
    class Meta:
        abstract = True

    def __str__(self):
        return self.name
    
class PartCategory(Category):
    # Add any additional fields or methods specific to PartCategory here
    pass

class DocumentCategory(Category):
    # Add any additional fields or methods specific to DocumentCategory here
    pass

class Part(models.Model):
    id = models.AutoField(primary_key=True)
    internal_part_number = models.CharField(max_length=255, unique=True)
    description = models.CharField(max_length=255, null=True, blank=True)
    released = models.BooleanField(default=False)
    purchase_option = models.ForeignKey('PurchaseOption', on_delete=models.SET_NULL, null=True)
    repository_link = models.CharField(max_length=255, null=True, blank=True)
    storage_code = models.CharField(max_length=255, null=True, blank=True)
    creation_date = models.DateField(auto_now_add=True)
    category = models.ForeignKey('PartCategory', on_delete=models.SET_NULL, null=True)
    item_number = models.IntegerField(null=True, blank=True)
    variant = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    revision = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    image = models.BinaryField(null=True, blank=True)

    def __str__(self):
        return self.internal_part_number

    def save(self, *args, **kwargs):
        if not self._state.adding:  # Check if the instance is being created or updated
            original_part = Part.objects.get(pk=self.pk)
            if (original_part.category != self.category or
                    original_part.item_number != self.item_number or
                    original_part.variant != self.variant or
                    original_part.revision != self.revision):
                raise ValueError("Direct editing of category, item_number, variant, and revision is not allowed for existing parts.")
        else:
            if not self.category:
                raise ValueError("Part Category undefined")
            if not self.item_number:
                self.create_new_item()
            if not self.variant:
                self.create_new_variant()
            if not self.revision:
                self.create_new_revision()
            self._update_internal_part_number()
        super().save(*args, **kwargs)

    def clean(self):
        if self.item_number < 1 or self.variant < 1 or self.revision < 1:
            raise ValidationError("Fields item_number, variant, and revision must be greater than or equal to 1.")

    def create_new_item(self, category=None):
        if category is not None:
            self.category = category
        elif not self.category:
            raise ValueError("Part Category undefined")
        last_part = Part.objects.filter(category=self.category).order_by('-item_number').first()
        if last_part:
            self.item_number = last_part.item_number + 1
        else:
            self.item_number = 1
        self.variant = 1
        self.revision = 1
    def create_new_variant(self, category=None, item_number=None):
        if category is not None:
            self.category = category
        elif not self.category:
            raise ValueError("Part Category undefined")
        if item_number is not None:
            self.item_number = item_number
        last_part = Part.objects.filter(category=self.category, item_number=self.item_number).order_by('-variant').first()
        if last_part:
            self.variant = last_part.variant + 1
        else:
            self.variant = 1
        self.revision = 1
    def create_new_revision(self, category=None, item_number=None, variant=None):
        if category is not None:
            self.category = category
        elif not self.category:
            raise ValueError("Part Category undefined")
        if item_number is not None:
            self.item_number = item_number
        if variant is not None:
            self.variant = variant
        last_part = Part.objects.filter(category=self.category, item_number=self.item_number, variant=self.variant).order_by('-revision').first()
        if last_part:
            self.revision = last_part.revision + 1
        else:
            self.revision = 1
    def _update_internal_part_number(self):
        item_number_str = str(self.item_number).zfill(3)
        variant_str = str(int(self.variant)).zfill(2)
        revision_str = str(int(self.revision)).zfill(2)
        self.internal_part_number = f'HW-{self.category}-{item_number_str}-v{variant_str}r{revision_str}'

class Manufacturer(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, unique=True)
    contact_info = models.CharField(max_length=255, null=True, blank=True)
    # Add any other fields you need for the Manufacturer model

class PurchaseOption(models.Model):
    id = models.AutoField(primary_key=True)
    part_ipn = models.ForeignKey('Part', on_delete=models.CASCADE, null=True)
    manufacturer = models.ForeignKey('Manufacturer', on_delete=models.SET_NULL, null=True)
    manufacturer_code = models.CharField(max_length=255, null=True, blank=True)
    datasheet = models.CharField(max_length=255, null=True, blank=True)
    obsolete = models.BooleanField(default=False)

class Container(models.Model):
    id = models.AutoField(primary_key=True)
    part_a = models.ForeignKey('Part', on_delete=models.CASCADE, related_name='containers_as_part_a')
    part_b = models.ForeignKey('Part', on_delete=models.CASCADE, related_name='containers_as_part_b')
    quantity = models.IntegerField()
    creation_date = models.DateField(auto_now_add=True)
    
    def clean(self):
        if self.part_a.released or self.part_b.released:
            raise ValidationError("Cannot modify container because one of the parts is released.")

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
    category = models.ForeignKey('DocumentCategory', on_delete=models.SET_NULL, null=True)
    item_number = models.IntegerField(null=True, blank=True)
    revision = models.CharField(max_length=255, null=True, blank=True)
    creation_date = models.DateField(auto_now_add=True)

class PartDocument(models.Model):
    id = models.AutoField(primary_key=True)
    part = models.ForeignKey('Part', on_delete=models.CASCADE)
    document = models.ForeignKey('Document', on_delete=models.CASCADE)