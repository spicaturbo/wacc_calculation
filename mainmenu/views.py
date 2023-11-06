from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def my_view(request):
    return render(request, "index.html")

def wacc_view(request):
    return render(request, "wacc_calculation.html")
