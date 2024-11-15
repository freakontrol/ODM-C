from django.test import TestCase
from .models import Category, PartCategory, DocumentCategory, Part, Manufacturer, PurchaseOption, Container, Document, PartDocument

# Create your tests here.
class PartModelTest(TestCase):
    def setUp(self):
        self.category = PartCategory.objects.create(name='TST')
        self.purchase_option = PurchaseOption.objects.create()
        self.part = Part.objects.create(description='Test part', purchase_option=self.purchase_option, category=self.category)
        self.assertEqual(self.part.internal_part_number, 'HW-TST-001-v01r01')
    def test_new_item_number(self):
        next_part = Part.objects.create(description='Test part', purchase_option=self.purchase_option, category=self.category)
        self.assertEqual(next_part.internal_part_number, 'HW-TST-002-v01r01')
    def test_new_variant(self):
        next_part = Part.objects.create(description='Test part', purchase_option=self.purchase_option, category=self.category, item_number=1)
        self.assertEqual(next_part.internal_part_number, 'HW-TST-001-v02r01')
    def test_new_revision(self):
        next_part = Part.objects.create(description='Test part', purchase_option=self.purchase_option, category=self.category, item_number=1, variant=1)
        self.assertEqual(next_part.internal_part_number, 'HW-TST-001-v01r02')
    def test_edit_part_ipn_attributes(self):
        new_category = PartCategory.objects.create(name='CAT')
        with self.assertRaises(ValueError):
            self.part.category = new_category
            self.part.save()

        with self.assertRaises(ValueError):
            self.part.item_number = 123
            self.part.save()

        with self.assertRaises(ValueError):
            self.part.variant = 456
            self.part.save()

        with self.assertRaises(ValueError):
            self.part.revision = 789
            self.part.save()