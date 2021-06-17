from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator

User = get_user_model()


class Meal(models.Model):
    title = models.CharField(max_length=150)
    description = models.TextField()

    def num_of_rating(self):
        rating = Rating.objects.filter(meal=self)
        return len(rating)

    def avg_rating(self):
        sum = 0
        ratings = Rating.objects.filter(meal=self)
        for r in ratings:
            sum += r.stars

        if len(ratings):
            return sum / len(ratings)
        else:
            return 0

    def __str__(self):
        return self.title


class Rating(models.Model):
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    stars = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)])

    def __str__(self):
        return str(self.meal)

    class Meta:
        unique_together = (('user', 'meal'),)
        index_together = (('user', 'meal'),)
