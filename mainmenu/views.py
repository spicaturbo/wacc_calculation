from django.shortcuts import render
from django.http import HttpResponse
from .forms import SumForm

# Create your views here.
def my_view(request):
    return render(request, "index.html")

def wacc_view(request):
    COE = None
    EED = None
    DED = None
    WACC = None
    if request.method == "POST":
        num1 = float(request.POST.get('num1', 0))
        num2 = float(request.POST.get('num2', 0))
        num3 = float(request.POST.get('num3', 0))
        num4 = float(request.POST.get('num4', 0))
        num5 = float(request.POST.get('num5', 0))
        num6 = float(request.POST.get('num6', 0))
        num7 = float(request.POST.get('num7', 0))
        num8 = float(request.POST.get('num8', 0))

        # Result
        COE = num5 + num6 * (num7 - num5)
        EED = num1 / (num1 + num2)
        DED = num2 / (num1 + num2)
        WACC = (DED * num7) + (DED * num3 * (1 - num4))

        result1 = f"{COE:.2f}"
        result2 = f"{EED:.2f}"
        result3 = f"{DED:.2f}"
        result4 = f"{WACC:.2f}"

    return render(request, "wacc_calculation.html", {
            'num1': num1, 
            'num2': num2, 
            'num3': num3,
            'num4': num4,
            'num5': num5,
            'num6': num6,
            'num7': num7,
            'num8': num8,
            'COE': result1,
            'EED': result2,
            'DED': result3,
            'WACC': result4
        })
