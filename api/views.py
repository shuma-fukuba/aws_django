from functools import partial
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Sale, Stock
from .serializer import SaleSerializer, StockSerializer


@api_view(['GET', 'POST', 'DELETE'])
def read_all(request):
    if request.method == 'GET':


        items = Stock.objects.order_by('name')
        serializer = StockSerializer(items, many=True)
        items = []
        for item in serializer.data:
            items.append({item['name']: item['amount']})
        return Response(items)
    elif request.method == 'POST':
        name = request.data['name']
        amount = request.data['amount']
        if request.data['amount'] is None:
            amount = 0
        serializer = StockSerializer(data={"name": name, "amount": amount})
        if serializer.is_valid():
            serializer.save()
        return Response(request.data)

    else:  # case delete
        Stock.objects.all().delete()
        return Response({'message': 'Successfully deleted.'})


@api_view(['GET'])
def read_one(request, name):

    try:
        item = Stock.objects.filter(name=name).get()
    except Stock.DoesNotExist:
        item = Stock()
        item.name = name
        item.amount = 0

    serializer = StockSerializer(item, many=False)

    return Response({serializer.data['name']: serializer.data['amount']})


@api_view(['GET', 'POST'])
def sales(request):
    if request.method == 'GET':
        try:
            sale = Sale.objects.all().get()
        except Sale.DoesNotExist:
            sale = Sale.objects.create(sale=0)
            serializer = SaleSerializer(sale, many=False)
            return Response(serializer.data)
        serializer = SaleSerializer(sale, many=False)
        return Response({"sales": round(serializer.data['sale'], 2)})
    elif request.method == 'POST':
        '''
        request.dataからname、amount、priceを取得する
        nameからレコードを取得し、その値からamountを引く
        salesレコードをとってきて、price * amountを加算する
        '''
        name = request.data['name']
        amount = request.data['amount']
        if amount is None:
            amount = 1
        if 'price' in request.data.keys():
            price = request.data['price']
            try:
                sale = Sale.objects.all().get()
            except Sale.DoesNotExist:
                serializer = SaleSerializer(data={"sale": 0})
                if serializer.is_valid():
                    sale = serializer.save()
            # sale.sale += amount * price
            serializer = SaleSerializer(sale, data={"sale": sale.sale+ amount * price}, partial=True)
            if serializer.is_valid():
                serializer.save()
        try:
            stock = Stock.objects.filter(name=name).get()
        except Stock.DoesNotExist:
            return Response(request.data)
        if stock.amount < amount:
            amount = stock.amount
        stock_serializer = StockSerializer(stock, data={"amount": stock.amount - amount}, partial=True)
        if stock_serializer.is_valid():
            stock_serializer.save()
        return Response(request.data)
