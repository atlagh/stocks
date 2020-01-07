from django.shortcuts import render, redirect
from .models import Stock
from .forms import StockForm
from django.contrib import messages

def home(request):
    import requests
    import json
    if request.method == 'POST':
        ticker = request.POST['ticker']
        api_request = requests.get("https://cloud.iexapis.com/stable/stock/"+ticker+"/quote?token=pk_79903f20c8e5418582a9e05cd08c0148")
        try:

               api = json.loads(api_request.content)

        except Exception as e:

               api = "this quote is not available please check the spelling"

        return render (request, 'index.html', {'api': api})

    else:
        return render (request, 'index.html', {'ticker': "Enter sympol above"})




def about(request):
    return render (request, 'about.html', {})

def add_stock(request):
    import requests
    import json
    if request.method == 'POST':
        form = StockForm(request.POST or None)

        if form.is_valid():
                form.save()
                messages.success(request, ("stock has been added"))
                return redirect('add_stock')
    else:
        ticker = Stock.objects.all()
        output = []
        for ticker_item in ticker:
            api_request = requests.get("https://cloud.iexapis.com/stable/stock/"+str(ticker_item)+"/quote?token=pk_79903f20c8e5418582a9e05cd08c0148")
            try:
                           api = json.loads(api_request.content)
                           output.append(api)
            except Exception as e:
                           api = "this quote is not available please check the spelling"
        return render (request, 'add_stock.html', {'ticker': ticker, 'output': output})

def delete(request, stock_id):
    item = Stock.objects.get(pk= stock_id)
    item.delete()
    messages.success(request, ("stock has been deleted"))
    return redirect(delete_page)

def delete_page(request):
    ticker = Stock.objects.all()
    return render (request, 'delete_page.html', {'ticker': ticker})


#this is just a comment