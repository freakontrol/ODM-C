from django.test import TestCase
from .models import Category, PartCategory, DocumentCategory, Part, Manufacturer, PurchaseOption, Container, Document, PartDocument

# Create your tests here.
class PartModelTest(TestCase):
    def test_part_creation(self):
        # Create a new part and verify its attributes
        category = PartCategory.objects.create(name='MEC')
        purchase_option = PurchaseOption.objects.create()
        part = Part.objects.create(description='Test part', purchase_option=purchase_option, category=category)
        self.assertEqual(part.internal_part_number, 'HW-MEC-001-v01r01')
        self.assertFalse(part.released)
        
    def test_new_item_number(self):
        # Create a new part and verify its attributes
        category = PartCategory.objects.create(name='MEC')
        purchase_option = PurchaseOption.objects.create()
        first_part = Part.objects.create(description='Test part', purchase_option=purchase_option, category=category)
        second_part = Part.objects.create(description='Test part', purchase_option=purchase_option, category=category)
        self.assertEqual(second_part.internal_part_number, 'HW-MEC-002-v01r01')
        self.assertFalse(second_part.released)
        
    def test_new_variant(self):
        # Create a new part and verify its attributes
        category = PartCategory.objects.create(name='MEC')
        purchase_option = PurchaseOption.objects.create()
        first_part = Part.objects.create(description='Test part', purchase_option=purchase_option, category=category)
        second_part = Part.objects.create(description='Test part', purchase_option=purchase_option, category=category, item_number=1)
        self.assertEqual(second_part.internal_part_number, 'HW-MEC-001-v02r01')
        self.assertFalse(second_part.released)
        
    def test_new_revision(self):
        # Create a new part and verify its attributes
        category = PartCategory.objects.create(name='MEC')
        purchase_option = PurchaseOption.objects.create()
        first_part = Part.objects.create(description='Test part', purchase_option=purchase_option, category=category)
        second_part = Part.objects.create(description='Test part', purchase_option=purchase_option, category=category, item_number=1, variant=1)
        self.assertEqual(second_part.internal_part_number, 'HW-MEC-001-v01r02')
        self.assertFalse(second_part.released)
