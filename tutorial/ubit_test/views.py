from django.shortcuts import render
from rest_framework.decorators import api_view
from ubit_test.ubit_tests.api_unittest import runUbitTrunk
from django.http import HttpResponse, JsonResponse, FileResponse
# import threading
from .models import ReportLog

# Create your views here.

from .form import UbitTrunkForm
@api_view(['GET', 'POST'])
def ubitTrunk(request):
    if request.method == 'POST':
        form = UbitTrunkForm(request.POST)
        if form.is_valid():
            env = int(form.cleaned_data['env'])
            file = runUbitTrunk(env)
            

            ReportLog.objects.create(
                report_env=env,
                report_file=str(file.name)
                )

            return FileResponse(file)
    else:
        form = UbitTrunkForm()
        return render(request, 'ubit_trunk.html', {'form': form})
    
