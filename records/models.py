from django.contrib.auth import get_user_model
from django.core.validators import MinLengthValidator, MaxLengthValidator, MinValueValidator, MaxValueValidator
from django.db import models
from django.urls import reverse


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_published=Records.Status.PUBLISHED)


class Records(models.Model):
    class Status(models.IntegerChoices):
        PUBLISHED = 1, 'Активно'
        DRAFT = 0, 'В корзине'

    rating = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(10)],  # Ограничение от 1 до 10
        verbose_name="Рэйтинг"
    )
    title = models.CharField(max_length=255, verbose_name="Заголовок")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="Slug", validators=[
        MinLengthValidator(5, message="Минимум 5 символов"),
        MaxLengthValidator(100, message="Максимум 100 символов"),
    ])
    photo = models.ImageField(upload_to="photos/%Y/%m/%d/", default=None,
                              blank=True, null=True, verbose_name="Фото")
    content = models.TextField(blank=True, verbose_name="Текст статьи")
    time_create = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")
    time_update = models.DateTimeField(auto_now=True, verbose_name="Время последнего изменения")
    is_published = models.BooleanField(choices=tuple(map(lambda x: (bool(x[0]), x[1]), Status.choices)),
                                       default=Status.PUBLISHED, verbose_name="Статус")
    cat = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True, related_name='posts',
                            verbose_name="Категории")

    tags = models.ManyToManyField('TagPost', blank=True, related_name='tags', verbose_name="Тэги")
    author = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True, related_name='posts',
                               default=None)
    objects = models.Manager()
    published = PublishedManager()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "пост"
        verbose_name_plural = "посты"
        ordering = ['-rating', '-time_create']
        indexes = [
            models.Index(fields=['-time_create'])
        ]

    def get_absolute_url(self):
        return reverse('post', kwargs={'post_slug': self.slug})


class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True, verbose_name='Категория')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='Slug')
    author = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, null=True, related_name='tag_requests')

    class Meta:
        verbose_name = "категория"
        verbose_name_plural = "категории"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_slug': self.slug})


class TagPost(models.Model):
    tag = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)
    author = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL,null=True, related_name='tagposts')

    def __str__(self):
        return self.tag

    def get_absolute_url(self):
        return reverse('tag', kwargs={'tag_slug': self.slug})


class UploadFiles(models.Model):
    file = models.FileField(upload_to='uploads_model')
