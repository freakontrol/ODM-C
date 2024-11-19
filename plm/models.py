from django.db import models
from django.core.exceptions import ValidationError

class Category(models.Model):
    name = models.CharField(max_length=3, unique=True)
    description = models.CharField(max_length=255, null=True, blank=True)
    class Meta:
        abstract = True
    def __str__(self):
        return self.name
    
class PartCategory(Category):
    pass

class DocumentCategory(Category):
    pass

class Document(models.Model):
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
    
    def __str__(self):
        return self.document_number

class Part(models.Model):
    internal_part_number = models.CharField(max_length=255, unique=True)
    description = models.CharField(max_length=255, null=True, blank=True)
    released = models.BooleanField(default=False)
    purchase_option = models.ForeignKey('PurchaseOption', on_delete=models.SET_NULL, null=True)
    repository_link = models.CharField(max_length=255, null=True, blank=True)
    documents = models.ManyToManyField(Document, related_name='parts')
    storage_code = models.CharField(max_length=255, null=True, blank=True)
    creation_date = models.DateField(auto_now_add=True)
    category = models.ForeignKey('PartCategory', on_delete=models.SET_NULL, null=True)
    item_number = models.IntegerField(null=True, blank=True)
    variant = models.IntegerField(null=True, blank=True)
    revision = models.IntegerField(null=True, blank=True)
    related_part = models.ManyToManyField('self', through='Container')
    image = models.BinaryField(null=True, blank=True)

    class Meta:
        unique_together = ('category', 'item_number', 'variant', 'revision')

    def __str__(self):
        return self.internal_part_number

    def save(self, *args, **kwargs):
        self.custom_checks()
        self.full_clean()
        super().save(*args, **kwargs)
            
    def custom_checks(self):
        #super().clean()
        fields = [self.item_number, self.variant, self.revision]
        if not all(field is None or field >= 1 for field in fields):
            raise ValidationError("Fields item_number, variant, and revision must be greater than or equal to 1.")
        if not self._state.adding:
            original_part = Part.objects.get(pk=self.pk)
            if (original_part.category != self.category or
                    original_part.item_number != self.item_number or
                    original_part.variant != self.variant or
                    original_part.revision != self.revision or
                    original_part.internal_part_number != self.internal_part_number):
                raise ValueError("Direct editing of category, item_number, variant, revision and ipn is not allowed for existing parts.")
            if original_part.released is True and self.released is not False:
                raise ValidationError("Cannot modify the part because it has already been released.")
        else:
            if not self.category:
                raise ValueError("Part Category undefined")
            if not self.item_number:
                self.create_new_item()
            elif not self.variant:
                self.create_new_variant()
            elif not self.revision:
                self.create_new_revision()
            elif self.internal_part_number != self._update_internal_part_number():
                raise ValueError("The Internal Part Number does not match the correct pattern")
    def create_new_item(self, category=None, description=None, purchase_option=None, repository_link=None, storage_code=None, *args):
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

        if description is not None:
            self.description = description
        if purchase_option is not None:
            self.purchase_option = purchase_option
        if repository_link is not None:
            self.repository_link = repository_link
        if storage_code is not None:
            self.storage_code = storage_code

        self.internal_part_number = self._update_internal_part_number()
    def create_new_variant(self, category=None, item_number=None, description=None, purchase_option=None, repository_link=None, storage_code=None, *args):
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

        if description is not None:
            self.description = description
        if purchase_option is not None:
            self.purchase_option = purchase_option
        if repository_link is not None:
            self.repository_link = repository_link
        if storage_code is not None:
            self.storage_code = storage_code

        self.internal_part_number = self._update_internal_part_number()
    def create_new_revision(self, category, item_number, variant, description=None, purchase_option=None, repository_link=None, storage_code=None, *args):
        if category is not None:
            self.category = category
        elif not self.category:
            raise ValueError("Part Category undefined")

        if item_number is not None:
            self.item_number = item_number
        elif not self.item_number:
            raise ValueError("Item Number undefined")

        if variant is not None:
            self.variant = variant
        elif not self.variant:
            raise ValueError("Variant undefined")

        last_part = Part.objects.filter(category=self.category, item_number=self.item_number, variant=self.variant).order_by('-revision').first()
        if last_part:
            self.revision = last_part.revision + 1
        else:
            self.revision = 1

        # Set optional attributes directly
        if description is not None:
            self.description = description
        if purchase_option is not None:
            self.purchase_option = purchase_option
        if repository_link is not None:
            self.repository_link = repository_link
        if storage_code is not None:
            self.storage_code = storage_code

        self.internal_part_number = self._update_internal_part_number()
    def _update_internal_part_number(self):
        item_number_str = str(self.item_number).zfill(3)
        variant_str = str(int(self.variant)).zfill(2)
        revision_str = str(int(self.revision)).zfill(2)
        return f'HW-{self.category}{item_number_str}-v{variant_str}r{revision_str}'

class Manufacturer(models.Model):
    name = models.CharField(max_length=255, unique=True)
    contact_info = models.CharField(max_length=255, null=True, blank=True)
    
    def __str__(self):
        return self.name

class PurchaseOption(models.Model):
    part_ipn = models.ForeignKey('Part', on_delete=models.CASCADE, null=True)
    manufacturer = models.ForeignKey('Manufacturer', on_delete=models.SET_NULL, null=True)
    manufacturer_code = models.CharField(max_length=255, null=True, blank=True)
    datasheet = models.CharField(max_length=255, null=True, blank=True)
    obsolete = models.BooleanField(default=False)

class Container(models.Model):
    part_a = models.ForeignKey('Part', on_delete=models.CASCADE, related_name='containers_as_part_a')
    part_b = models.ForeignKey('Part', on_delete=models.CASCADE, related_name='containers_as_part_b')
    quantity = models.IntegerField()
    creation_date = models.DateField(auto_now_add=True)

    class Meta:
        unique_together = ('part_a', 'part_b',)
        
    def clean(self):
        if self.part_a.released or self.part_b.released:
            raise ValidationError("Cannot modify container because one of the parts is released.")
        
    def __str__(self):
        return self.part_a
