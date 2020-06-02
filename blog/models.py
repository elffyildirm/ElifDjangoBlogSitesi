from django.db import models
from django.utils.safestring import mark_safe
from ckeditor_uploader.fields import  RichTextUploadingField
from mptt.models import MPTTModel
from mptt.fields import TreeForeignKey
from django.contrib.auth.models import User
from django import forms
from django.urls import reverse
from django.forms.widgets import FileInput, Select, TextInput
from ckeditor.widgets import CKEditorWidget
from django.forms import ModelForm

class Category(MPTTModel):
    STATUS=(
        ('True', 'Evet'),
        ('False', 'Hayir')
    )
    title = models.CharField(max_length=150)
    description = models.CharField(max_length=255)
    keywords= models.CharField(max_length=255)
    image= models.ImageField(blank= True, upload_to ='images/' )
    status= models.CharField(max_length=10, choices=STATUS)
    creat_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    slug=models.SlugField(null=False, unique=True)
    detail= RichTextUploadingField()
    parent =TreeForeignKey('self', blank=True, null=True ,related_name='children', on_delete=models.CASCADE)
    class MPTTMeta:
        order_insertion_by = ['title']
    
    def __str__(self):
        full_path = [self.title]
        k = self.parent
        while k is not None:
            full_path.append(k.title)
            k = k.parent
        return ' ->'.join(full_path[::-1])

    def image_tag(self):
        return mark_safe('<img src="{}" height="50"/>'.format(self.image.url))
    image_tag.short_description = 'Image'

    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'slug': self.slug})


TYPE = (
    ('blog', 'blog'),
    ('haber', 'haber'),
    ('duyuru', 'duyuru'),
    ('etkinlik', 'etkinlik'),
)
class Blog(models.Model):
    STATUS=(
        ('True', 'Evet'),
        ('False', 'Hayir')
    )
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=150)
    description = models.CharField(max_length=255)
    keywords= models.CharField(max_length=255)
    image= models.ImageField(upload_to ='images/' )
    type = models.CharField(max_length=10, choices=TYPE)
    status= models.CharField(max_length=10, choices=STATUS)
    creat_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    detail= RichTextUploadingField()
    slug=models.SlugField(null=False, unique=True)
    parent =models.ForeignKey('self', blank=True, null=True ,related_name='children', on_delete=models.CASCADE)
    def __str__(self):
        return self.title
    def image_tag(self):
        return mark_safe('<img src="{}" height="50"/>'.format(self.image.url))
    image_tag.short_description = 'Image'

    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'slug': self.slug})

class Images(models.Model):
    blog=models.ForeignKey (Blog, on_delete=models.CASCADE)
    title = models.CharField(max_length=50,blank= True)
    image= models.ImageField(blank= True, upload_to ='images/' )
    def __str__(self):
        return self.title
    def image_tag(self):
        return mark_safe('<img src="{}" height="50"/>'.format(self.image.url))
    image_tag.short_description = 'Image'


class Comment(models.Model):
    STATUS =(
        ('New', 'Yeni'),
        ('True', 'Evet'),
        ('False', 'Hayır'),
    )
    blog = models.ForeignKey( Blog, on_delete=models.CASCADE)
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=50, blank=True)
    comment = models.TextField(max_length=200,blank=True)
    rate = models.IntegerField()
    status = models.CharField(max_length=10, choices=STATUS, default='New')
    ip = models.CharField(blank=True, max_length=20)
    create_at=models.DateTimeField(auto_now_add=True)
    update_at=models.DateTimeField(auto_now=True)

    def _str_(self):
        return self.subject

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['subject', 'comment', 'rate']


class ContentForm(ModelForm):
    class Meta:
        model = Blog
        fields = ['type','category' ,'title', 'slug', 'keywords',
                  'description', 'image', 'detail']
        widgets = {
            'title': TextInput(attrs={'class': 'input', 'placeholder': 'title'}),
            'slug': TextInput(attrs={'class': 'input', 'placeholder': 'slug'}),
            'keywords': TextInput(attrs={'class': 'input', 'placeholder': 'keywords'}),
            'description': TextInput(attrs={'class': 'input', 'placeholder': 'description'}),
            'type': Select(attrs={'class': 'input', 'placeholder': 'city'}, choices=TYPE),
            'image': FileInput(attrs={'class': 'input', 'placeholder': 'image', }),
            'detail': CKEditorWidget(),
        }


class ContentImageForm(ModelForm):
    class Meta:
        model = Images
        fields = ['title','image']
