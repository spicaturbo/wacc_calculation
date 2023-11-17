from django.shortcuts import render
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.platypus import Table, TableStyle

# Create your views here.
def my_view(request):
    return render(request, "index.html")

def wacc_view(request):
    # Defining variable
    num1 = None
    num2 = None
    num3 = None
    num4 = None
    num5 = None
    num6 = None
    num7 = None
    num8 = None

    COE = None
    EED = None
    DED = None
    WACC = None
    result = None
    result1 = None
    result2 = None
    result3 = None
    result4 = None
    resultTV = None

    year = None
    EBIT = None
    rEBIT = None
    DA = None
    CapEx = None
    NonCashWC = None
    rTax = None
    rDA = None
    rCapex = None
    rNoncashwc = None
    TV = None
    rFCF = None
    rDiscount = None
    rPVFCF = None
    PVTV = 0
    rPVTV = 0
    Cash = None
    MS = None
    STD = None
    LTD = None
    OSH = None
    rCash = None
    rMS = None
    rSTD = None
    rLTD = None
    rOSH = None
    EnterpriseValue = 0
    EquityValue = None
    IntrinsicValue = None

    arrayYear = None
    arrayEBIT = []
    arrayTax = []
    arrayDA = []
    arrayCapEx = []
    arrayNonCashWC = []
    arrayFCF = []
    arrayDiscount = []
    arrayPVFCF = []


    if request.method == "POST":
        year = int(request.POST.get('year', 0))
        num1 = float(request.POST.get('num1', 0))
        num2 = float(request.POST.get('num2', 0))
        num3 = float(request.POST.get('num3', 0))
        rnum3 = num3 / 100
        num4 = float(request.POST.get('num4', 0))
        rnum4 = num4 / 100
        num5 = float(request.POST.get('num5', 0))
        rnum5 = num5 / 100
        num6 = float(request.POST.get('num6', 0))
        num7 = float(request.POST.get('num7', 0))
        rnum7 = num7 / 100
        num8 = float(request.POST.get('num8', 0))
        rnum8 = num8 / 100
        EBIT = float(request.POST.get('EBIT', 0))
        DA = float(request.POST.get('DA', 0))
        CapEx = float(request.POST.get('CapEx', 0))
        NonCashWC = float(request.POST.get('NonCashWC', 0))
        Cash = float(request.POST.get('Cash', 0))
        MS = float(request.POST.get('MS', 0))
        STD = float(request.POST.get('STD', 0))
        LTD = float(request.POST.get('LTD', 0))
        OSH = float(request.POST.get('OSH', 0))

        # Result
        COE = (rnum5 + num6 * (rnum7 - rnum5))
        EED = (num1 / (num1 + num2))
        DED = (num2 / (num1 + num2))
        WACC = ((EED * COE) + (DED * rnum3 * (1 - rnum4)))

        # Result decimal
        result1 = f"{COE * 100:.3f}"
        result2 = f"{EED * 100 :.3f}"
        result3 = f"{DED * 100:.3f}"
        result4 = f"{WACC * 100:.3f}"

        arrayYear = [i for i in range(0, year + 1)]

        # Result EBIT
        for index, yr in enumerate(arrayYear):
            if index == 0:
                dec1 = EBIT * ((1 + rnum8) ** yr )
                rEBIT = f"{dec1:.3f}"
                rTax = EBIT * -rnum4
            else :
                dec1 = float(arrayEBIT[index - 1]) * ((1 + rnum8) ** yr )
                rEBIT = f"{dec1:.3f}"
                dec2 = float(dec1) * -rnum4
                rTax = f"{dec2:.3f}"

            if index == 0:
                dec1 = DA * ((1 + rnum8) ** yr )
                rDA = f"{dec1:.3f}"
            else :
                dec1 = float(arrayDA[index - 1]) * ((1 + rnum8) ** yr )
                rDA = f"{dec1:.3f}"

            if index == 0:
                dec1 = CapEx * ((1 + rnum8) ** yr )
                rCapex = f"{dec1:.3f}"
            else :
                dec1 = float(arrayCapEx[index - 1]) * ((1 + rnum8) ** yr )
                rCapex = f"{dec1:.3f}"

            if index == 0:
                dec1 = NonCashWC * ((1 + rnum8) ** yr )
                rNoncashwc = f"{dec1:.3f}"
            else :
                dec1 = float(arrayNonCashWC[index - 1]) * ((1 + rnum8) ** yr )
                rNoncashwc = f"{dec1:.3f}"

            rFCF = float(rEBIT) + float(rDA) + float(rTax) + float(rCapex) + float(rNoncashwc)

            if index != 0:
                dec1 = (1 / ((1 + WACC) ** yr))
                rDiscount = f"{dec1:.3f}"
                dec2 = (float(rDiscount) * float(rFCF))
                rPVFCF = f"{dec2:.3f}"

            arrayEBIT.append(rEBIT)
            arrayTax.append(rTax)
            arrayDA.append(rDA)
            arrayCapEx.append(rCapex)
            arrayNonCashWC.append(rNoncashwc)
            arrayFCF.append(rFCF)
            arrayDiscount.append(rDiscount)
            arrayPVFCF.append(rPVFCF)

        TV = (float(arrayFCF[-1]) * (1 + rnum8)) / (WACC - rnum8)
        resultTV = f"{TV:.3f}"

        PVTV = float(arrayDiscount[-1]) * float(resultTV)
        rPVTV = f"{PVTV:.3f}"

        res = 0

        for x in arrayPVFCF:
            if x is not None:
                res += float(x)

        res = res + PVTV

        EnterpriseValue = f"{res:.3f}"

        result = float(EnterpriseValue) + Cash + MS - STD - LTD
        EquityValue = f"{result:.3f}"

        results = float(EquityValue)/OSH
        IntrinsicValue = f"{results:.2f}"

    if request.method == "GET":
        # Sample data (replace with your actual data)
        year = int(request.GET.get('year', 0))
        num1 = float(request.GET.get('num1', 0))
        num2 = float(request.GET.get('num2', 0))
        num3 = float(request.GET.get('num3', 0))
        rnum3 = num3 / 100
        num4 = float(request.GET.get('num4', 0))
        rnum4 = num4 / 100
        num5 = float(request.GET.get('num5', 0))
        rnum5 = num5 / 100
        num6 = float(request.GET.get('num6', 0))
        num7 = float(request.GET.get('num7', 0))
        rnum7 = num7 / 100
        num8 = float(request.GET.get('num8', 0))
        rnum8 = num8 / 100
        EBIT = float(request.GET.get('EBIT', 0))
        DA = float(request.GET.get('DA', 0))
        CapEx = float(request.GET.get('CapEx', 0))
        NonCashWC = float(request.GET.get('NonCashWC', 0))
        Cash = float(request.GET.get('Cash', 0))
        MS = float(request.GET.get('MS', 0))
        STD = float(request.GET.get('STD', 0))
        LTD = float(request.GET.get('LTD', 0))
        OSH = float(request.GET.get('OSH', 0))

        # Result
        COE = (rnum5 + num6 * (rnum7 - rnum5))
        EED = (num1 / (num1 + num2))
        DED = (num2 / (num1 + num2))
        WACC = ((EED * COE) + (DED * rnum3 * (1 - rnum4)))

        # Result decimal
        result1 = f"{COE * 100:.3f}"
        result2 = f"{EED * 100 :.3f}"
        result3 = f"{DED * 100:.3f}"
        result4 = f"{WACC * 100:.3f}"

        arrayYear = [i for i in range(0, year + 1)]

        for index, yr in enumerate(arrayYear):
            if index == 0:
                dec1 = EBIT * ((1 + rnum8) ** yr )
                rEBIT = f"{dec1:.3f}"
                rTax = EBIT * -rnum4
            else :
                dec1 = float(arrayEBIT[index - 1]) * ((1 + rnum8) ** yr )
                rEBIT = f"{dec1:.3f}"
                dec2 = float(dec1) * -rnum4
                rTax = f"{dec2:.3f}"

            if index == 0:
                dec1 = DA * ((1 + rnum8) ** yr )
                rDA = f"{dec1:.3f}"
            else :
                dec1 = float(arrayDA[index - 1]) * ((1 + rnum8) ** yr )
                rDA = f"{dec1:.3f}"

            if index == 0:
                dec1 = CapEx * ((1 + rnum8) ** yr )
                rCapex = f"{dec1:.3f}"
            else :
                dec1 = float(arrayCapEx[index - 1]) * ((1 + rnum8) ** yr )
                rCapex = f"{dec1:.3f}"

            if index == 0:
                dec1 = NonCashWC * ((1 + rnum8) ** yr )
                rNoncashwc = f"{dec1:.3f}"
            else :
                dec1 = float(arrayNonCashWC[index - 1]) * ((1 + rnum8) ** yr )
                rNoncashwc = f"{dec1:.3f}"

            rFCF = float(rEBIT) + float(rDA) + float(rTax) + float(rCapex) + float(rNoncashwc)

            if index != 0:
                dec1 = (1 / ((1 + WACC) ** yr))
                rDiscount = f"{dec1:.3f}"
                dec2 = (float(rDiscount) * float(rFCF))
                rPVFCF = f"{dec2:.3f}"

            arrayEBIT.append(rEBIT)
            arrayTax.append(rTax)
            arrayDA.append(rDA)
            arrayCapEx.append(rCapex)
            arrayNonCashWC.append(rNoncashwc)
            arrayFCF.append(f"{rFCF:.3f}")
            arrayDiscount.append(rDiscount)
            arrayPVFCF.append(rPVFCF)
        
        TV = (float(arrayFCF[-1]) * (1 + rnum8)) / (WACC - rnum8)
        resultTV = f"{TV:.3f}"

        PVTV = float(arrayDiscount[-1]) * float(resultTV)
        rPVTV = f"{PVTV:.3f}"

        res = 0

        for x in arrayPVFCF:
            if x is not None:
                res += float(x)

        res = res + PVTV

        EnterpriseValue = f"{res:.3f}"

        result = float(EnterpriseValue) + Cash + MS - STD - LTD
        EquityValue = f"{result:.3f}"

        results = float(EquityValue)/OSH
        IntrinsicValue = f"{results:.2f}"

        data = [
            ['WACC CALCULATION'],
            ['Equity Value', num1],
            ['Debt Value', num2],
            ['Cost of Debt', str(num3) + " %"],
            ['Tax Rate', str(num4) + " %"],
            ['10y Treasury', str(num5) + " %"],
            ['Beta', num6],
            ['Market Return', str(num7) + " %"],
            ['Cost of Equity', result1 + " %"],
            ['Growth Rate', str(num8) + " %"],
            ['E / E + D', result2 + " %"],
            ['D / E + D', result3 + " %"],
            ['WACC', result4 + " %"]
            # Add more data as needed
        ]

        arrayYear.insert(0, 'Period')
        arrayEBIT.insert(0, 'EBIT')
        arrayTax.insert(0, 'Tax')
        arrayDA.insert(0, 'D&A')
        arrayCapEx.insert(0, 'CapEx')
        arrayNonCashWC.insert(0, 'Non Cash WC')
        arrayFCF.insert(0, 'FCF')
        arrayDiscount.insert(0, "Discount Factor")
        arrayPVFCF.insert(0, "PV of FCF")

        # Define the length of the array
        array_length = year

        # Create an array with the specified length and fill it with empty strings
        my_array = ['' for _ in range(array_length)]
        my_array.insert(0, "TV")
        my_array.append(resultTV)

        my_array2 = ['' for _ in range(array_length)]
        my_array2.insert(0, "PV of TV")
        my_array2.append(rPVTV)

        my_array3 = ['' for _ in range(array_length)]
        my_array3.insert(0, "Enterprise Value")
        my_array3[2] = EnterpriseValue

        my_array4 = ['' for _ in range(array_length)]
        my_array4.insert(0, "Cash")
        my_array4[2] = Cash

        my_array5 = ['' for _ in range(array_length)]
        my_array5.insert(0, "Marketable Securities")
        my_array5[2] = MS

        my_array6 = ['' for _ in range(array_length)]
        my_array6.insert(0, "Short term Debit")
        my_array6[2] = STD

        my_array7 = ['' for _ in range(array_length)]
        my_array7.insert(0, "Long term Debit")
        my_array7[2] = LTD

        my_array8 = ['' for _ in range(array_length)]
        my_array8.insert(0, "Equity Value")
        my_array8[2] = EquityValue

        my_array9 = ['' for _ in range(array_length)]
        my_array9.insert(0, "Outstanding Shares")
        my_array9[2] = OSH

        my_array10 = ['' for _ in range(array_length)]
        my_array10.insert(0, "Intrinsic Value")
        my_array10[2] = IntrinsicValue

        data2 = [
            arrayYear,
            arrayEBIT,
            arrayTax,
            arrayDA,
            arrayCapEx,
            arrayNonCashWC,
            arrayFCF,
            my_array,
            arrayDiscount,
            arrayPVFCF,
            my_array2,
            my_array3,
            [],
            my_array4,
            my_array5,
            my_array6,
            my_array7,
            my_array8,
            [],
            my_array9,
            my_array10
        ]

        # Create a response object with PDF content
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="DCF Calculation Result.pdf"'

        # Create PDF document
        p = canvas.Canvas(response, pagesize=letter)

        # Create a table
        table = Table(data)
        table2 = Table(data2)

        # Add style to the table1
        style = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), '#77D7E4'),
            ('TEXTCOLOR', (0, 0), (-1, 0), (0, 0, 0)),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), '#FFFFFF'),
            ('GRID', (0, 0), (-1, -1), 1, '#000000'),
            # Merge cells in the first row
            ('SPAN', (0, 0), (-1, 0)),
        ])

        # Add style to the table2
        style2 = TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), '#77D7E4'),
            ('TEXTCOLOR', (0, 0), (-1, 0), (0, 0, 0)),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), '#FFFFFF'),
            ('GRID', (0, 0), (-1, -1), 1, '#000000'),
        ])

        table.setStyle(style)
        table2.setStyle(style2)

        # Draw the table on the PDF
        table.wrapOn(p, 0, 0)
        table.drawOn(p, 50, 500)

        # Draw the table2 on the PDF
        table2.wrapOn(p, 0, 0)
        table2.drawOn(p, 50, 100)

        # Close the PDF document
        p.showPage()
        p.save()

        return response

        
        

    # Render html & passing data
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
            'WACC': result4,
            'year': year,
            'EBIT': EBIT,
            'DA': DA,
            "CapEx": CapEx,
            "NonCashWC": NonCashWC,
            'arrayYear': arrayYear,
            'arrayEBIT': arrayEBIT,
            'arrayTax': arrayTax,
            'arrayDA': arrayDA,
            'arrayCapEx': arrayCapEx,
            'arrayNonCashWC': arrayNonCashWC,
            'arrayFCF': arrayFCF,
            'TV': resultTV,
            'arrayDiscount': arrayDiscount,
            'arrayPVFCF': arrayPVFCF,
            'PVTV': rPVTV,
            "Cash": Cash,
            "MS": MS,
            "STD": STD,
            "LTD": LTD,
            "OSH": OSH,
            "EquityValue": EquityValue,
            "EnterpriseValue": EnterpriseValue,
            "IntrinsicValue": IntrinsicValue,
        })
