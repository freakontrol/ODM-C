# views.py
from django.shortcuts import render, redirect
from .models import PartCategory, DocumentCategory
from .forms import PartCategoryForm, DocumentCategoryForm

def categories_view(request):
    if request.method == 'POST':
        part_category_form = PartCategoryForm(request.POST)
        document_category_form = DocumentCategoryForm(request.POST)

        if part_category_form.is_valid():
            part_category_form.save()
            return redirect('categories')

        if document_category_form.is_valid():
            document_category_form.save()
            return redirect('categories')
    else:
        part_category_form = PartCategoryForm()
        document_category_form = DocumentCategoryForm()

    part_categories = PartCategory.objects.all()
    document_categories = DocumentCategory.objects.all()

    context = {
        'part_categories': part_categories,
        'document_categories': document_categories,
        'part_category_form': part_category_form,
        'document_category_form': document_category_form,
    }
    return render(request, 'plm/categories.html', context)
