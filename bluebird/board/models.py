from django.db import models
from django.utils import timezone
from django.urls import reverse

# Create your models here.
class Post(models.Model):
    title = models.CharField(verbose_name='TITLE', max_length=200)
    content = models.TextField('CONTENT', default='')
    tent = models.TextField('TENT', default='')
    password = models.IntegerField(default='0000')
    writer = models.CharField(max_length=200, default='')
    pub_date = models.DateTimeField('PUBLISH DATE',default=timezone.now)
    mod_date = models.DateTimeField('MODIFY DATE', auto_now=True)
    filename = models.TextField('filename','' )
    key = models.TextField('key', default='')


class Meta:

    verbose_name ='post'
    verbose_name_plural ='posts'
    db_table='board+posts'
    ordering=('-mod_date',)


    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('board:post_detail', args=(self.id,))

    def get_previous(self):
        return self.get_previous_by_mod_date()

    def get_next(self):
        return self.get_next_bt_mod_date()

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, related_name='comments')
    comment_date = models.DateTimeField(auto_now=True)
    comment_contents = models.CharField(max_length=2000)
    comment_writer = models.CharField(max_length=200, default='회장님')

    class Meta:
        ordering = ['-id']