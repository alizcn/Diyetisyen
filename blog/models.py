from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name=_('Kategori Adı'))
    slug = models.SlugField(max_length=100, unique=True, verbose_name=_('Slug'))
    description = models.TextField(blank=True, verbose_name=_('Açıklama'))

    class Meta:
        verbose_name = _('Kategori')
        verbose_name_plural = _('Kategoriler')
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name, allow_unicode=True)
        super().save(*args, **kwargs)


class Post(models.Model):
    title = models.CharField(max_length=200, verbose_name=_('Başlık'))
    slug = models.SlugField(max_length=200, unique=True, verbose_name=_('Slug'))
    content = models.TextField(verbose_name=_('İçerik'))
    excerpt = models.TextField(max_length=500, blank=True, verbose_name=_('Özet'))
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='blog_posts',
        limit_choices_to={'user_type': 'dietitian'},
        verbose_name=_('Yazar')
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='posts',
        verbose_name=_('Kategori')
    )
    featured_image = models.ImageField(
        upload_to='blog/',
        blank=True,
        null=True,
        verbose_name=_('Kapak Görseli')
    )
    is_published = models.BooleanField(default=False, verbose_name=_('Yayınlandı'))
    published_date = models.DateTimeField(null=True, blank=True, verbose_name=_('Yayın Tarihi'))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    views_count = models.PositiveIntegerField(default=0, verbose_name=_('Görüntüleme Sayısı'))

    class Meta:
        verbose_name = _('Blog Yazısı')
        verbose_name_plural = _('Blog Yazıları')
        ordering = ['-published_date', '-created_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title, allow_unicode=True)
        if self.is_published and not self.published_date:
            self.published_date = timezone.now()
        super().save(*args, **kwargs)

    @property
    def reading_time(self):
        """Tahmini okuma süresi (dakika)"""
        words = len(self.content.split())
        return max(1, round(words / 200))
