from rest_framework import serializers

from .models import Meal, Rating


class MealSerializer(serializers.ModelSerializer):
    class Meta:
        model = Meal
        fields = ('url', 'id', 'title', 'description')


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ('url', 'id', 'stars', 'user', 'meal')
