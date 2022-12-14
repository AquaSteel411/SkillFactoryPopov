from django.db import models
from django.contrib.auth.models import User


class Author(models.Model):
    rating_user = models.IntegerField(default=0)

    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    def update_rating(self):
        post_rating = sum(Post.objects.filter(author=self).values_list('rating_news', flat=True)) * 3
        com_rating = sum(Comment.objects.filter(user__author=self).values_list('rating_com', flat=True))
        com_post_rating = sum(Comment.objects.filter(post__in=Post.objects.filter(author=self)).
                              values_list('rating_com', flat=True))
        self.rating_user = post_rating + com_rating + com_post_rating
        self.save()


class Category(models.Model):
    topic = models.CharField(max_length=255, unique=True)


class Post(models.Model):
    article = 'AR'
    news = 'NW'

    TYPES = [
        (article, 'Статья'),
        (news, 'Новость')
    ]

    time_post = models.DateTimeField(auto_now_add=True)
    type_post = models.CharField(max_length=2, choices=TYPES, default=news)
    author = models.ForeignKey(Author, models.CASCADE)
    category = models.ManyToManyField(Category, through='PostCategory')
    header = models.CharField(max_length=255)
    text = models.TextField()
    rating_news = models.IntegerField(default=0)

    def like(self):
        self.rating_news += 1
        self.save()

    def dislike(self):
        self.rating_news -= 1
        self.save()

    def preview(self):
        return f'{self.text[:124]}...'


class PostCategory(models.Model):
    post = models.ForeignKey(Post, models.CASCADE)
    category = models.ForeignKey(Category, models.CASCADE)


class Comment(models.Model):
    text_comment = models.TextField()
    time_com = models.DateTimeField(auto_now_add=True)
    rating_com = models.IntegerField(default=0)

    post = models.ForeignKey(Post, models.CASCADE)
    user = models.ForeignKey(User, models.CASCADE)

    def like(self):
        self.rating_com += 1
        self.save()

    def dislike(self):
        self.rating_com -= 1
        self.save()
