from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.urls import reverse


class Author(models.Model):
    authorUser = models.OneToOneField(User, on_delete=models.CASCADE)
    ratingAutor = models.SmallIntegerField(default=0)

    def update_rating(self):
        postRat = self.post_set.aggregate(postRating=Sum('rating'))
        pRat = 0
        pRat += postRat.get('postRating')

        commentRat = self.authorUser.comment_set.aggregate(commentRating=Sum('rating'))
        cRat = 0
        cRat += commentRat.get('commentRating')

        self.ratingAutor = pRat * 3 + cRat
        self.save()

    def __str__(self):
        return f'{self.authorUser}'

    class Meta:
        verbose_name = 'Автор'
        verbose_name_plural = 'Автор'
class Category(models.Model):
    name = models.CharField(max_length=64, unique=True)
    # subscribers = models.ManyToManyField(User, related_name='categories')

    def __str__(self):
        return f'{self.name}'


class Post (models.Model):
    postAuthor = models.ForeignKey('Author', on_delete=models.CASCADE)

    NEWS ='NW'
    ARTICLE = 'AR'
    CATEGORY_CHOICES = (
        (NEWS,'Новость'),
        (ARTICLE, 'Статья'),
    )
    categoryType =  models.CharField(max_length=2, choices=CATEGORY_CHOICES, default=ARTICLE)
    dataCreation = models.DateTimeField(auto_now_add=True)
    postCategory = models.ManyToManyField(Category, through='PostCategory')
    title = models.CharField(max_length=128)
    text = models.TextField(max_length=128)
    rating = models.SmallIntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return self.text[0:123] + '...'

    def __str__(self):
        return f'{self.title}, {self.postCategory}'

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])


class PostCategory(models.Model):
    postPost = models.ForeignKey('Post', on_delete=models.CASCADE)
    postCategory = models.ForeignKey('Category', on_delete=models.CASCADE)

class Comment(models.Model):
    commentPost = models.ForeignKey('Post', on_delete=models.CASCADE)
    commentUser = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    dataTimeComment = models.DateTimeField(auto_now_add=True)
    ratingComments = models.SmallIntegerField(default=0)

    def like(self):
        self.ratingComments += 1
        self.save()

    def dislike(self):
        self.ratingComments -= 1
        self.save()


class Subscription(models.Model):
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='subscriptions',
    )
    category = models.ForeignKey(
        to='Category',
        on_delete=models.CASCADE,
        related_name='subscriptions',
    )


