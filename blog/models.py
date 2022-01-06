from django.db import models

# Create your models here.
from django.db import models
from django.db.models.fields import AutoField
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils.text import slugify
from random import randint

User = get_user_model()

class GeneralModel(models.Model):

    create_at = models.DateTimeField(
        verbose_name=_('Created Time'),
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        verbose_name=_('Updated Time'),
        auto_now=True
    )

    class Meta:
        abstract = True


class Category(GeneralModel):

    title = models.CharField(
        verbose_name=_("Category Title"),
        max_length=250
    )
    parent = models.ForeignKey(
        "self",
        verbose_name="Category Parent",
        related_name='post_category',
        on_delete=models.PROTECT,
        null=True,
        blank=True
    )

    author = models.ForeignKey(
        User,
        verbose_name=_('Category Author'),
        null=True,
        on_delete=models.SET_NULL,
    )

    def get_absolute_url(self):
        return reverse('category_list')

    def __str__(self):
        return self.title


class Tag(GeneralModel):

    title = models.CharField(
        verbose_name=_("Tag Title"),
        max_length=250,
        null=True,
        blank=True
    )

    def __str__(self):
        return self.title


class Post(GeneralModel):

    title = models.CharField(
        verbose_name=_('Post Title'),
        max_length=255,
    )

    content = models.TextField()
    image = models.ImageField(
        upload_to='uploads',
        null=True,
        blank=True
    )
    category = models.ManyToManyField(Category)

    author = models.ForeignKey(
        User,
        verbose_name=_('Post Author'),
        on_delete=models.CASCADE,
    )
    slug = models.SlugField(
        unique=True,
        blank=True,

    )

    def save(self, *args, **kwargs):
        if not self.slug:
            if Post.objects.filter(title=self.title).exists() or Post.objects.filter(slug=self.title).exists():
                add_rand = str(randint(1, 10000))
                self.slug = slugify(self.title) + "-" + add_rand
            else:
                self.slug = slugify(self.title)
        super(Post, self).save(*args, **kwargs)

    class Meta:
        ordering = ('-create_at', )

    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'slug': self.slug})

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(
        Post,
        related_name='comments',
        on_delete=models.CASCADE
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE)
    text = models.TextField()

    def __str__(self):
        return f'{self.author.username} {self.post}'
