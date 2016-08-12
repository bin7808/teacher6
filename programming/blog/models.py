import os
import uuid
import re
from django.core.files import File
from django.core.urlresolvers import reverse
from django.conf import settings
from django.db import models
from django.db.models.signals import pre_save
from django.utils import timezone
from .validators import MinLengthValidator, lnglat_validator, ZipCodeValidator
from .fields import PhoneNumberField
from programming.pil_image import thumbnail


# min_length_4_validator = MinLengthValidator(4)
# min_length_4_validator = min_length_validator(4)


def myupload_to(instance, filename):
    extension = os.path.splitext(filename)[-1]
    name = uuid.uuid4().hex
    return os.path.join(name[:3], name[3:6], name[6:] + extension)


class Post(models.Model):
    author = models.CharField(max_length=20)
    title = models.CharField(max_length=100,
            validators=[MinLengthValidator(4)],
            verbose_name='제목')
    content = models.TextField(help_text='Markdown 문법을 써주세요.',
            validators=[MinLengthValidator(10)])
    # tags = models.CharField(max_length=100, blank=True)
    photo = models.ImageField(upload_to=myupload_to)
    tag_set = models.ManyToManyField('Tag', blank=True)
    lnglat = models.CharField(max_length=50, validators=[lnglat_validator], help_text='경도,위도 포맷으로 입력')
    created_at = models.DateTimeField(default=timezone.now)
    test_field = models.IntegerField(default=10)

    def get_absolute_url(self):
        return reverse('blog:post_detail', args=[self.pk])

    @property
    def lat(self):
        return self.lnglat.split(',')[1]

    @property
    def lng(self):
        return self.lnglat.split(',')[0]

def on_pre_save(sender, **kwargs):
    post = kwargs['instance']
    if post.photo:
        # post.photo        : 이미지 저장 경로
        # post.photo.name   : 이미지 파일명
        # post.photo.path   : 이미지 저장 absolute path
        # post.photo.url    : 이미지 URL
        # post.photo.file   : 지정 경로에 대한 file-object
        # post.photo.width   (ImageField only)
        # post.photo.height  (ImageField only)

        max_size = 300
        if post.photo.width > max_size or post.photo.height > max_size:
            processed_file = thumbnail(post.photo.file, max_size, max_size)
            post.photo.save(post.photo.name, File(processed_file))

pre_save.connect(on_pre_save, sender=Post)


class Comment(models.Model):
    post = models.ForeignKey(Post)
    message = models.TextField()
    jjal = models.ImageField(blank=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL)


class Tag(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Contact(models.Model):
    name = models.CharField(max_length=20)
    phone_number = PhoneNumberField()


class ZipCode(models.Model):
    city = models.CharField(max_length=20)
    road = models.CharField(max_length=20)
    dong = models.CharField(max_length=20)
    gu = models.CharField(max_length=20)
    code = models.CharField(max_length=7)
