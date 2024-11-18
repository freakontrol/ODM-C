from django.test import TestCase
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from .models import Category, PartCategory, DocumentCategory, Part, Manufacturer, PurchaseOption, Container, Document

class PartModelTest(TestCase):
    def setUp(self):
        self.category = PartCategory.objects.create(name='TST')
        self.purchase_option = PurchaseOption.objects.create()
        self.part = Part()
        self.part.create_new_item(description='Test part', purchase_option=self.purchase_option, 
                                  category=self.category)
        self.part.save()
        self.assertEqual(self.part.internal_part_number, 'HW-TST001-v01r01')
    def test_new_item_number(self):
        next_part = Part()
        next_part.create_new_item(description='Test part', purchase_option=self.purchase_option, 
                                  category=self.category)
        next_part.save()
        self.assertEqual(next_part.internal_part_number, 'HW-TST002-v01r01')
    def test_new_variant(self):
        next_part = Part()
        next_part.create_new_variant(description='Test part', purchase_option=self.purchase_option, 
                                     category=self.category, item_number=1)
        next_part.save()
        self.assertEqual(next_part.internal_part_number, 'HW-TST001-v02r01')
    def test_new_revision(self):
        next_part = Part()
        next_part.create_new_revision(description='Test part', purchase_option=self.purchase_option, 
                                      category=self.category, item_number=1, variant=1)
        next_part.save()
        self.assertEqual(next_part.internal_part_number, 'HW-TST001-v01r02')
        
    def test_bad_format_ipn(self):
        with self.assertRaises(ValueError):
            next_part = Part(internal_part_number='malformed-ipn', description='Test part', 
                             category=self.category, item_number=2, variant=1, revision=1)
            next_part.save()
            
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
    def test_new_not_unique_ipn(self):
        with self.assertRaises(ValidationError):
            new_part = Part.objects.create(description='Test part',
                                            purchase_option=self.purchase_option,
                                            category=self.category,
                                            item_number=1,
                                            variant=1,
                                            revision=1,
                                            internal_part_number='HW-TST001-v01r01')
    def test_release_lock(self):
        self.part.released = True
        self.part.save()
        with self.assertRaises(ValidationError):
            self.part.description = "change the description"
            self.part.save()