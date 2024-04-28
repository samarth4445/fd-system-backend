from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from django.http import JsonResponse


from .models import Restaurant
from .serializers import *

@api_view(['GET', 'POST'])
def index(request):
    coursers = None
    if request.method == "POST":      
        data = request.data
        print(data)
        coursers = {
            'course_name': 'POST',
            'learn': ["flask", 'django'],
            'course_provider': 'Scaler'
        }
    else:
        coursers = {
            'course_name': 'GET',
            'learn': ["flask", 'django'],
            'course_provider': 'Scaler'
        }

    return Response(coursers)

class OrderByUserView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def post(self, request):
        orders_list = []
        user = request.user

        orders = Order.objects.filter(user=user)
        
        for order in orders:
            order_items = OrderItems.objects.filter(orders=order)
            print(order_items)
            order_price = 0
            order_obj = []
            done = {}

            for order_item in order_items:
                if(order_item.item.id in done):
                    continue
                quant = 0
                done[order_item.item.id] = 1

                for od in order_items:
                    if od.item.id == order_item.item.id:
                        quant += 1

                order_obj.append({
                    "name": order_item.item.item_name, 
                    "quantity": quant
                    })
                order_price += order_item.item.item_price
            orders_list.append({"items": order_obj, "amount": order_price, "status": order.status})
        
        print(orders_list)
        return Response(orders_list)


class OrderView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    def post(self, request):
        restaurant_order = request.data
        order = Order.objects.create(
            user=request.user,
        )

        print(restaurant_order["order"])

        for item, quant in restaurant_order["order"].items():
            print(item, quant)
            res_item = RestaurantItems.objects.get(id=int(item))
            quant2 = quant

            while(quant2>0):
                order_items = OrderItems.objects.create(
                    user=request.user,
                    orders=order,
                    item=res_item
                )
                quant2 -= 1
    
        return JsonResponse({
            "success": True, 
            "message": "Order has been created!"
        })

class LoginAPI(APIView):
    def post(self, request):
        data = request.data
        serializer = LoginSerializer(data = data)
        
        if not serializer.is_valid():
            return Response({"mesdsage": serializer.errors}, 400)

        user = authenticate(username = serializer.data['username'], password = serializer.data['password'])
        if not user:
            return Response({"message": "Invalid Credentials"})

        token, _ = Token.objects.get_or_create(user=user)

        return Response({"success": True, "message": "Logged In", "token": str(token)}, 201)

class RegisterAPI(APIView):
    def post(self, request):
        data = request.data
        serializer = RegisterSerializer(data = data)

        if not serializer.is_valid():
            return Response({'success': False, "messsage": serializer.errors}, 400)

        serializer.save()

        return Response({'success': True, 'message': "user created"}, 201)

class ItemView(APIView):
    # permission_classes = [IsAuthenticated]
    # authentication_classes = [TokenAuthentication]
    def get(self, request):
        objs = RestaurantItems.objects.all()
        serializer = ItemSerializer(objs, many=True)

        return Response({"items": serializer.data})

class ItemByRestaurantIDView(APIView):
    def get(self, request, id):
        restaurant = Restaurant.objects.get(id=id)
        objs = RestaurantItems.objects.filter(restaurant=restaurant)
        serializer = ItemSerializer(objs, many=True)

        return Response({"items": serializer.data})

class RestaurantView(APIView):
    def get(self, request):
        objs = Restaurant.objects.all()
        serializer = RestaurantSerializer(objs, many=True)

        return Response({"restaurants": serializer.data})

    # def post(self, request):
    #     data = request.data
    #     serializer = RestaurantSerializer(data = data)

    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.validated_data)
    #     return Response(serializer.errors)
