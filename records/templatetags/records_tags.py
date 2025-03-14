from django import template
from django.db.models import Count
import records.views as views
from records.models import Category, TagPost, Records

register = template.Library()


@register.inclusion_tag('records/list_categories.html')
def show_categories(cat_selected=0, request=None):
    # Убедитесь, что request передан в тег
    if not request or not hasattr(request, 'user'):
        raise ValueError("request не содержит атрибута 'user'")

    # Если пользователь не авторизован, не фильтруем по автору
    if request.user.is_authenticated:
        # Получаем посты текущего пользователя
        user_posts = Records.objects.filter(author=request.user)

        if user_posts.exists():
            # Получаем категории, связанные с постами текущего пользователя
            cats = Category.objects.annotate(total=Count("posts")).filter(
                total__gt=0, posts__in=user_posts
            ).distinct()
        else:
            # Если нет постов, то не выводим категории
            cats = Category.objects.none()
    else:
        # Если пользователь не авторизован, возвращаем пустой набор категорий
        cats = Category.objects.none()

    return {'cats': cats, 'cat_selected': cat_selected}


@register.inclusion_tag('records/list_tags.html')
def show_all_tags():
    return {'tags': TagPost.objects.annotate(total=Count("tags")).filter(total__gt=0)}
