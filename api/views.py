from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth import get_user_model

from .models import Meal, Rating
from .serializers import MealSerializer, RatingSerializer


User = get_user_model()


class MealViewSet(viewsets.ModelViewSet):
    queryset = Meal.objects.all()
    serializer_class = MealSerializer

    @action(methods=['POST'], detail=True)
    def rate_meal(self, request, pk=None):
        if 'stars' in request.data:
            '''
            Create Or Update
            '''
            meal = Meal.objects.get(id=pk)
            username = request.data['username']
            stars = request.data['stars']
            user = User.objects.get(username=username)
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
                return Response()

        else:
            json = {
                'message': 'Stars Not Provided!'
            }
            return Response(json, status=status.HTTP_400_BAD_REQUEST)


class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
