from django.contrib import admin, messages
from .models import Records, Category, TagPost


@admin.register(Records)
class RecordsAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'time_create', 'cat', 'is_published', 'breaf_info')
    list_display_links = ('id', 'time_create')
    ordering = ('id', 'time_create', 'is_published')
    list_editable = ['is_published', 'title']
    list_per_page = 10
    actions = ['set_published', 'set_delete', ]
    search_fields = ['title', 'cat__name', ]
    list_filter = ['cat__name', 'is_published']

    @admin.display(description='Длина поста')
    def breaf_info(self, record: Records):
        return f"{len(record.content)} символов"

    @admin.action(description='Убрать из корзины')
    def set_published(self, request, queryset):
        queryset.update(is_published=Records.Status.PUBLISHED)
        self.message_user(request, f"{queryset.count()} постов возвращено из корзины.")

    @admin.action(description='Переместить в корзину')
    def set_delete(self, request, queryset):
        queryset.update(is_published=Records.Status.DRAFT)
        self.message_user(request, f"{queryset.count()} постов помещено в корзину.", messages.WARNING)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')
    list_display_links = ('id', 'name')



@admin.register(TagPost)
class TagPostAdmin(admin.ModelAdmin):
    list_display = ('id', 'tag', 'slug')
    # list_display_links = ('id', 'tag')
    # list_editable = ('tag', 'slug')