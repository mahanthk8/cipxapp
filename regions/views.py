from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from users.decorators import role_required
from .models import Region
from .forms import RegionForm

@login_required
@role_required('ADMIN')
def region_list(request):
    regions = Region.objects.all()
    return render(request, 'region/list.html', {'regions': regions})


@login_required
@role_required('ADMIN')
def region_create(request):
    if request.method == 'POST':
        form = RegionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('region_list')
    else:
        form = RegionForm()

    return render(request, 'region/create.html', {'form': form})


@login_required
@role_required('ADMIN')
def region_update(request, pk):
    region = get_object_or_404(Region, pk=pk)

    if request.method == 'POST':
        form = RegionForm(request.POST, instance=region)
        if form.is_valid():
            form.save()
            return redirect('region_list')
    else:
        form = RegionForm(instance=region)

    return render(request, 'region/update.html', {'form': form})


@login_required
@role_required('ADMIN')
def region_delete(request, pk):
    region = get_object_or_404(Region, pk=pk)
    region.delete()
    return redirect('region_list')
