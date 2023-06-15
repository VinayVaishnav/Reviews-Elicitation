from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_image = models.ImageField(upload_to='profile_images', blank=True, null=True)
    contact_number = models.CharField(max_length=10)

    def __str__(self):
        return f'{self.user.username}'


class Review(models.Model):
    to_user = models.CharField(max_length=100)
    from_user = models.CharField(max_length=100)
    review = models.TextField()
    is_anonymous = models.BooleanField(default=False)
    anonymous_from = models.CharField(max_length=100)

    upvotes = models.ManyToManyField(User, related_name='upvoted_reviews', blank=True)
    downvotes = models.ManyToManyField(User, related_name='downvoted_reviews', blank=True)

    class Meta:
        unique_together = ('to_user', 'from_user')

    def upvote(self, user):
        if user not in self.upvotes.all():
            self.upvotes.add(user)
            if user in self.downvotes.all():
                self.downvotes.remove(user)
        elif user in self.upvotes.all():
            self.upvotes.remove(user)

    def downvote(self, user):
        if user not in self.downvotes.all():
            self.downvotes.add(user)
            if user in self.upvotes.all():
                self.upvotes.remove(user)

        elif user in self.downvotes.all():
            self.downvotes.remove(user)

    def get_upvotes_count(self):
        return self.upvotes.count()

    def get_downvotes_count(self):
        return self.downvotes.count()
    
    def __str__(self):
        return f'{self.from_user} => {self.to_user} : {self.review}'
