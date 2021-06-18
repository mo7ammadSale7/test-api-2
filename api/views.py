from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly, AllowAny
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model


from .models import Meal, Rating
from .serializers import MealSerializer, RatingSerializer, UserSerializer


User = get_user_model()


class MealViewSet(viewsets.ModelViewSet):
    queryset = Meal.objects.all()
    serializer_class = MealSerializer
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [IsAuthenticated, ]

    @action(methods=['POST'], detail=True)
    def rate_meal(self, request, pk=None):
        if 'stars' in request.data:
            '''
            Create Or Update
            '''
            meal = Meal.objects.get(id=pk)
            stars = request.data['stars']
            user = request.user
            try:
                # Update
                rating = Rating.objects.get(user=user.id, meal=meal.id)
                rating.stars = stars
                rating.save()
                serializer = RatingSerializer(rating, many=False)
                json = {
                    'message': 'Meal Rate Updated',
                    'result': serializer.data
                }
                return Response(json, status=status.HTTP_201_CREATED)

            except:
                # Create
                rating = Rating.objects.create(
                    stars=stars, meal=meal, user=user)
                serializer = RatingSerializer(rating, many=False)
                json = {
                    'message': 'Meal Rate Created',
                    'result': serializer.data
                }
                return Response(json, status=status.HTTP_201_CREATED)

        else:
            json = {
                'message': 'Stars Not Provided!'
            }
            return Response(json, status=status.HTTP_400_BAD_REQUEST)


class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [IsAuthenticated, ]

    def create(self, request, *args, **kwargs):
        response = {
            'message': 'This is not right way to create rating'
        }
        return Response(response, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        response = {
            'message': 'This is not right way to update rating'
        }
        return Response(response, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        token, created = Token.objects.get_or_create(user=serializer.instance)
        return Response({'token': token.key}, status=status.HTTP_201_CREATED)

    def list(self, request, *args, **kwargs):
        response = {'message': 'failed list'}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)
