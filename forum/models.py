from django.db import models
from django.contrib.auth.models import User
from django.db.models import Min

class Post(models.Model):
    caption = models.CharField(max_length = 200)
    category = models.IntegerField()
    pinned = models.BooleanField(default = False)
    def __str__(self):
        return self.caption
    #def find_first_message(self, id):
        #return Message.objects.annotate(Min('pk')).filter(pk=id)

class Message(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    text = models.TextField(max_length = 5000)
    author = models.ForeignKey(User, on_delete = models.CASCADE)
    date = models.DateTimeField(auto_now_add = True)
    def __str__(self):
        return self.text
    def count_messages(author_parameter):
        return Message.objects.filter(author=author_parameter).count()

'''class Direct(models.Model):
    sender = models.ForeignKey(User, on_delete = models.CASCADE)
    receiver = models.ForeignKey(User, on_delete = models.CASCADE)
    caption = models.CharField(max_length = 200)
    text = models.TextField(max_length = 5000)
    date = models.DateTimeField(auto_now_add = True)
    read = models.BooleanField(default = False)'''
