from django.db import models
from django.contrib.auth.models import User
from multiselectfield import MultiSelectField

from . import polls

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
    
    RATING_CHOICES1 = [
        (1, 'Option 1'),
        (2, 'Option 2'),
        (3, 'Option 3'),
        (4, 'Option 4'),
        (5, 'Option 5'),
    ]
    RATING_CHOICES2 = [
        (1, 'Option 1'),
        (2, 'Option 2'),
        (3, 'Option 3'),
        (4, 'Option 4'),
        (5, 'Option 5'),
    ]
    RATING_CHOICES3 = [
        (1, 'Option 1'),
        (2, 'Option 2'),
        (3, 'Option 3'),
        (4, 'Option 4'),
        (5, 'Option 5'),
    ]

    problem_solving = MultiSelectField(choices=RATING_CHOICES1, max_length=255)
    communication = MultiSelectField(choices=RATING_CHOICES2, max_length=255)
    sociability = MultiSelectField(choices=RATING_CHOICES3, max_length=255)

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

class Poll(models.Model):
    username = models.CharField(max_length=100)
    options = polls.poll_dict

    def vote(self, question, option, username):
        user = User.objects.get(username=username)
        question_field = getattr(self, f'{question}{option}')
        other_options = [o for o in self.options[question] if o != option]

        for other_option in other_options:
            other_field = getattr(self, f'{question}{other_option}')
            other_field.remove(user)

        if user not in question_field.all():
            question_field.add(user)
        else:
            question_field.remove(user)

    def get_counts(self, question, option):
        field = getattr(self, f'{question}{option}')
        count = field.count()
        return count
    
    def get_percentage(self, question, option):
        total = 0
        for opt in self.options[question]:
            total += self.get_counts(question, opt)
        if total == 0:
            return 0
        else:
            # return int(self.get_counts(question, option) / total * 100)
            return round(self.get_counts(question, option) / total * 100)
        
    def get_total_votes(self, question):
        total = 0
        for opt in self.options[question]:
            total += self.get_counts(question, opt)
        return total

    def has_voted(self, question, option, username):
        user = User.objects.get(username=username)
        field = getattr(self, f'{question}{option}')
        return user in field.all()
    
    def has_voted_question(self, question, username):
        user = User.objects.get(username=username)
        for opt in self.options[question]:
            field = getattr(self, f'{question}{opt}')
            if user in field.all():
                return True
        return False

    def __str__(self):
        return f'{self.username}'
    
for question, options in Poll.options.items():
    for option in options:
        field_name = f'{question}{option}'
        field = models.ManyToManyField(User, related_name=field_name, blank=True)
        Poll.add_to_class(field_name, field)