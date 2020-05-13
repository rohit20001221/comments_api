from django.db import models
from django.db.models import Q
from django.contrib.auth.models import User
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

from datetime import datetime
import uuid

def create_id():
    # pattern = '%Y%m%d%H%M%S%f'
    pattern = '%S%f'
    return datetime.now().strftime(pattern)+uuid.uuid1().hex
# Create your models here.


class WebSite(models.Model):
    name = models.CharField(max_length=200)
    site_url = models.CharField(max_length=1000)
    key = models.CharField(max_length=1000, default=create_id)

    def __str__(self):
        return f"{self.site_url}"


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments_set')
    website = models.ForeignKey(WebSite, on_delete=models.CASCADE, related_name='comments_set')
    comment = models.TextField()
    is_root = models.BooleanField(default=True)
    sub_comment = models.ForeignKey('self', on_delete=models.CASCADE, related_name='sub_comments_set', null=True)

    @property
    def total_likes(self):
        return self.likes_set.count()

    @property
    def total_dislikes(self):
        return self.dislikes_set.count()

    def __str__(self):
        return f"({self.user.username})[{self.comment}]"

class Like(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='likes_set')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes_set')

    def __str__(self):
        return f"Like - {self.comment}"

    def save(self):
        q1 = Q(user=self.user)
        q2 = Q(comment=self.comment)

        if not Like.objects.filter(q1&q2).exists():
            super(Like, self).save()
        else:
            return

class DisLike(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='dislikes_set')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='dislikes_set')

    def __str__(self):
        return f"DisLike - {self.comment}"

    def save(self):
        q1 = Q(user=self.user)
        q2 = Q(comment=self.comment)

        if not DisLike.objects.filter(q1&q2).exists():
            super(DisLike, self).save()
        else:
            return


@receiver(models.signals.post_save, sender=User)
def generate_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
