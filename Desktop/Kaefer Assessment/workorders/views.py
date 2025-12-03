from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.db.models import Count
from .models import ScaffoldComponent
from .forms import ScaffoldComponentForm
from django.urls import reverse_lazy

# List View
def scaffold_component_list(request):
    components = ScaffoldComponent.objects.all()

    # Filters
    q = request.GET.get('q')
    site_filter = request.GET.get('site')
    category_filter = request.GET.get('category')
    condition_filter = request.GET.get('condition')
    in_use_filter = request.GET.get('in_use')

    if q:
        components = components.filter(name__icontains=q) | components.filter(asset_code__icontains=q)
    if site_filter:
        components = components.filter(site=site_filter)
    if category_filter:
        components = components.filter(category=category_filter)
    if condition_filter:
        components = components.filter(condition=condition_filter)
    if in_use_filter:
        components = components.filter(is_in_use=(in_use_filter == 'true'))

    # Summary Counts
    site_counts = components.values('site').annotate(count=Count('site')).order_by('site')
    condition_counts = components.values('condition').annotate(count=Count('condition')).order_by('condition')

    # Pagination
    paginator = Paginator(components, 10) # 10 components per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'site_choices': ScaffoldComponent.SITE_CHOICES,
        'category_choices': ScaffoldComponent.CATEGORY_CHOICES,
        'condition_choices': ScaffoldComponent.CONDITION_CHOICES,
        'q': q,
        'site_filter': site_filter,
        'category_filter': category_filter,
        'condition_filter': condition_filter,
        'in_use_filter': in_use_filter,
        'site_counts': site_counts,
        'condition_counts': condition_counts,
    }
    return render(request, 'workorders/scaffold_component_list.html', context)

# Create View
def scaffold_component_create(request):
    if request.method == 'POST':
        form = ScaffoldComponentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('scaffold_component_list')
    else:
        form = ScaffoldComponentForm()
    return render(request, 'workorders/scaffold_component_form.html', {'form': form, 'form_type': 'create'})

# Detail View
def scaffold_component_detail(request, pk):
    component = get_object_or_404(ScaffoldComponent, pk=pk)
    return render(request, 'workorders/scaffold_component_detail.html', {'component': component})

# Edit View
def scaffold_component_edit(request, pk):
    component = get_object_or_404(ScaffoldComponent, pk=pk)
    if request.method == 'POST':
        form = ScaffoldComponentForm(request.POST, instance=component)
        if form.is_valid():
            form.save()
            return redirect('scaffold_component_list')
    else:
        form = ScaffoldComponentForm(instance=component)
    return render(request, 'workorders/scaffold_component_form.html', {'form': form, 'form_type': 'edit'})

# Delete View
def scaffold_component_delete(request, pk):
    component = get_object_or_404(ScaffoldComponent, pk=pk)
    if request.method == 'POST':
        component.delete()
        return redirect('scaffold_component_list')
    return render(request, 'workorders/scaffold_component_confirm_delete.html', {'component': component})