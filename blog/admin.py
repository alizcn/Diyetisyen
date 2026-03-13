from django.contrib import admin
from .models import Category, Post


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'is_published', 'published_date', 'views_count')
    list_filter = ('is_published', 'category', 'published_date')
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'published_date'
    ordering = ('-published_date', '-created_at')

    fieldsets = (
        ('Genel Bilgiler', {
            'fields': ('title', 'slug', 'author', 'category')
        }),
        ('İçerik', {
            'fields': ('excerpt', 'content', 'featured_image')
        }),
        ('Yayın Ayarları', {
            'fields': ('is_published', 'published_date')
        }),
        ('İstatistikler', {
            'fields': ('views_count',),
            'classes': ('collapse',)
        }),
    )

    readonly_fields = ()

    def save_model(self, request, obj, form, change):
        if not change:
            obj.author = request.user
        super().save_model(request, obj, form, change)
