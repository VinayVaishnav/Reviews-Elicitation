from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
        ('N', 'Not specified'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_image = models.ImageField(upload_to='profile_images', blank=True, null=True)
    contact_number = models.CharField(max_length=10)
    bio = models.TextField(blank=True, null=True)
    gender = models.CharField(max_length=1, default='N', choices=GENDER_CHOICES)

    def __str__(self):
        return f'{self.user.username}'


class Review(models.Model):
    to_user = models.CharField(max_length=100)
    from_user = models.CharField(max_length=100)

    review_rating_1 = models.IntegerField(default=0)
    review_rating_2 = models.IntegerField(default=0)
    review_rating_3 = models.IntegerField(default=0)

    problem_solving = models.TextField(max_length=1000, default='')
    communication = models.TextField(max_length=1000, default='')
    sociability = models.TextField(max_length=1000, default='')
    
    problem_solving_bool = models.BooleanField(default=False)
    communication_bool = models.BooleanField(default=False)
    sociability_bool = models.BooleanField(default=False)

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
    
    def review_giver(self):
        if self.anonymous_from == 'Anonymous':
            return f'Anonymous'
        else:
            FromUser = User.objects.get(username=self.from_user)
            return f'{FromUser.first_name} {FromUser.last_name}'
        
    def review_receiver(self):
        ToUser = User.objects.get(username=self.to_user)
        return f'{ToUser.first_name} {ToUser.last_name}'
    
    def has_upvoted(self, user):
        return user in self.upvotes.all()
    
    def has_downvoted(self, user):
        return user in self.downvotes.all()

    def __str__(self):
        return f'{self.from_user} => {self.to_user}'
