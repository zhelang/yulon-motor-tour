import os
from django.db import models
from django.urls import reverse
from django.core.files.storage import FileSystemStorage
from django.core.validators import MinValueValidator, MaxValueValidator, validate_email
from django.conf import settings
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from reservation.models import Orders

bannerfs = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, 'banners_image'))


class Banner(models.Model):
    banner_image = models.ImageField(upload_to='banners_image')
    banner_description = models.CharField(max_length=255)
    banner_url = models.URLField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
    title = models.CharField(max_length=255)
    content = models.CharField(max_length=1024)
    star = models.DecimalField(max_digits=2,
                               decimal_places=1,
                               validators=[MinValueValidator(0.0), MaxValueValidator(5.0)])
    create_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    approve = models.BooleanField(default=False)
    active = models.BooleanField(default=False)

    def __unicode__(self):
        if(self.active):
            active = 'Active'
        else:
            active = 'Inactive'
        if len(self.content) > 20:
            content = self.content[0:20] + ' ...'
        else:
            content = self.content[:]
        return active + ' || ' + self.title + '-' + content


class FAQ(models.Model):
    question = models.CharField(max_length=1024)
    answer = RichTextField(max_length=1024)
    priority = models.DecimalField(max_digits=5, decimal_places=3)
    created_at = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)

    def __unicode__(self):
        if(self.active):
            active = 'Active'
        else:
            active = 'Inactive'
        if len(self.question) > 20:
            question = self.question[0:20] + '...'
        else:
            question = self.question[:]
        return active + ' || ' + question

    def get_absolute_url(self):
        return reverse('faq')


class SiteInfo(models.Model):
    site_info_content = RichTextField(max_length=1024)
    email = models.EmailField(validators=[validate_email])
    phone = models.CharField(max_length=16)
    address = models.CharField(max_length=255)


class Ticket(models.Model):
    assigned_by = models.ForeignKey(User, related_name='%(class)s_assigned_by', on_delete=models.CASCADE, null=True)
    assigned_to = models.ForeignKey(User, related_name='%(class)s_assigned_to', on_delete=models.CASCADE, null=True)
    order = models.ForeignKey(Orders, on_delete=models.CASCADE, null=True)
    finished = models.BooleanField(default=False)
    reported_customer_number = models.IntegerField(null=True, blank=True, validators=[MinValueValidator(0)])
    create_at = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    reminder = models.TextField(max_length=2048, blank=True, default='')


class SEO(models.Model):
    title = models.CharField(max_length=1024, blank=True, default='')
    url_address = models.URLField(null=True)
    description = models.CharField(max_length=1024, blank=True, default='')
    img = models.ImageField(upload_to='seo_image', blank=True, default='')
    type = models.CharField(default='website', max_length=1024)


class EmailTemplate(models.Model):
    from_email = models.EmailField()
    subject = models.CharField(max_length=1024)
    email_content = models.TextField(max_length=2048)
