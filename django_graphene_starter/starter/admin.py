from django.contrib import admin

from .models import Article, Publication, Reporter


@admin.register(Reporter)
class ReporterAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'last_login',
        'is_superuser',
        'username',
        'first_name',
        'last_name',
        'email',
        'is_staff',
        'is_active',
        'date_joined',
    )
    list_filter = (
        'last_login',
        'is_superuser',
        'is_staff',
        'is_active',
        'date_joined',
    )


@admin.register(Publication)
class PublicationAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('id', 'headline', 'pub_date', 'reporter')
    list_filter = ('pub_date',)
    raw_id_fields = ('reporter',)
