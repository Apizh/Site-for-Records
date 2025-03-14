from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseNotFound, Http404, HttpResponseRedirect, HttpResponsePermanentRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, FormView, CreateView, UpdateView, DeleteView
from .forms import AddPostForm, UploadFileForm, AddCategoryForm, AddTagForm
from .models import Records, Category, TagPost, UploadFiles
from .utils import DataMixin
from django.utils.text import slugify
from unidecode import unidecode
from django.contrib.auth.decorators import login_required


def generate_slug(text):
    """Функция генерации слага на основе переданного ей текста."""
    return slugify(unidecode(text))


class RecordsHome(LoginRequiredMixin, DataMixin, ListView):
    template_name = 'records/index.html'
    context_object_name = 'posts'
    cat_selected = 0
    extra_context = {'title': 'Главная страница'}

    def get_queryset(self):
        return Records.objects.filter(author=self.request.user).select_related('cat')


# Краткое описание о возможностях сайта.
class AboutSite(TemplateView):
    template_name = 'records/about.html'
    extra_context = {'title': 'О сайте'}


class ShowPost(DataMixin, DetailView):
    template_name = 'records/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context, title=context['post'].title)

    def get_object(self, queryset=None):
        return get_object_or_404(Records.objects, slug=self.kwargs[self.slug_url_kwarg])


class AddPost(LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddPostForm
    template_name = 'records/addpost.html'
    extra_context = {'title': 'Добавить статью'}

    def form_valid(self, form):
        w = form.save(commit=False)
        w.author = self.request.user
        w.slug = generate_slug(w.title)
        return super().form_valid(form)


class UpdatePost(DataMixin, UpdateView):
    model = Records
    fields = ['title', 'content', 'rating', 'photo', 'is_published', 'cat', 'tags', ]
    template_name = 'records/addpost.html'
    success_url = reverse_lazy('home')
    extra_context = {'title': 'Редактировать запись'}


class Contacts(TemplateView):
    template_name = 'records/contacts.html'
    extra_context = {
        'title': 'Контакты',
        'phone_number': 'Впишите сюда номер телефона',
        'email': 'Впишите сюда e-mail адрес',
        'address': 'Впишите сюда адрес',
    }


class RecordsCategory(DataMixin, ListView):
    template_name = 'records/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_queryset(self):
        return Records.objects.filter(cat__slug=self.kwargs['cat_slug']).select_related("cat")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cat = context['posts'][0].cat
        return self.get_mixin_context(context,
                                      title=cat.name,
                                      cat_selected=cat.pk,
                                      )


class TagPostList(DataMixin, ListView):
    template_name = 'records/index.html'
    context_object_name = 'posts'
    allow_empty = True

    def get_queryset(self):
        # Фильтруем записи по категории и текущему пользователю
        queryset = Records.objects.filter(
            cat__slug=self.kwargs['cat_slug'],
            author=self.request.user  # Фильтрация по текущему пользователю
        ).select_related("cat")
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        tag = TagPost.objects.get(slug=self.kwargs['tag_slug'])
        return self.get_mixin_context(context, title=tag.tag)

    def get_queryset(self):
        return Records.published.filter(tags__slug=self.kwargs['tag_slug']).select_related('cat')


# Для удаления записи из таблицы
class DeletePost(View):
    def post(self, request, slug):
        post = get_object_or_404(Records, slug=slug)

        # Проверка на подтверждение
        if request.POST.get('confirm_delete') == 'yes':
            post.delete()
            return redirect('home')  # Перенаправление на список постов (или на нужную вам страницу)

        return redirect('post', post_slug=post.slug)


# Измменение поля "is_published"
class ToggleFlagView(View):
    def post(self, request, slug):
        record = get_object_or_404(Records, slug=slug)
        status = not record.is_published
        record.is_published = status
        record.save()
        title = ["Переместили в корзину", "Убрали из корзины"][status]
        return render(request, 'records/post.html', {'post': record, 'title': title})


class AddCategory(LoginRequiredMixin, CreateView):
    form_class = AddCategoryForm
    template_name = 'records/addcategory.html'
    extra_context = {'title': 'Добавить категорию'}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Передаем категорию и форму с текущим пользователем
        context['categories'] = Category.objects.filter(author=self.request.user)
        context['form'] = self.get_form()
        return context

    def get_form_kwargs(self):
        """Передаем пользователя в форму."""
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user  # передаем пользователя в форму
        return kwargs

    def form_valid(self, form):
        category = form.save(commit=False)
        category.author = self.request.user
        base_slug = generate_slug(category.name)
        slug = slugify(base_slug)
        counter = 1
        while Category.objects.filter(slug=slug).exists():
            slug = f"{base_slug}{counter}"
            counter += 1
        category.slug = slug

        category.save()
        return redirect(reverse('addcategory'))


class CategoryUpdateView(LoginRequiredMixin, UpdateView):
    model = Category
    form_class = AddCategoryForm
    template_name = 'records/addcategory.html'

    def get_object(self):
        return get_object_or_404(Category, slug=self.kwargs['slug'], author=self.request.user)

    def get_success_url(self):
        return reverse('addcategory')


class AddTag(LoginRequiredMixin, CreateView):
    form_class = AddTagForm
    template_name = 'records/addtag.html'
    extra_context = {'title': 'Добавить тему'}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Передаем категорию и форму с текущим пользователем
        context['data'] = TagPost.objects.filter(author=self.request.user)
        context['form'] = self.get_form()
        return context

    def get_form_kwargs(self):
        """Передаем пользователя в форму."""
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user  # передаем пользователя в форму
        return kwargs

    def form_valid(self, form):
        tag = form.save(commit=False)
        tag.author = self.request.user
        base_slug = generate_slug(tag.tag)
        slug = slugify(base_slug)
        counter = 1
        while TagPost.objects.filter(slug=slug).exists():
            slug = f"{base_slug}{counter}"
            counter += 1
        tag.slug = slug

        tag.save()
        return redirect(reverse('addtag'))


class TagUpdateView(LoginRequiredMixin, UpdateView):
    model = TagPost
    form_class = AddTagForm
    template_name = 'records/addtag.html'

    def get_object(self):
        return get_object_or_404(TagPost, slug=self.kwargs['slug'], author=self.request.user)

    def get_success_url(self):
        return reverse('addtag')


@login_required
def delete_object(request, slug, model):
    if model == 'category':
        obj = get_object_or_404(Category, slug=slug, author=request.user)
        obj.delete()
        return redirect('addcategory')
    elif model == 'tag':
        obj = get_object_or_404(TagPost, slug=slug, author=request.user)
        obj.delete()
        return redirect('addtag')
    else:
        # Возвращаем ошибку или делаем что-то, если передана неизвестная модель
        return redirect('home')
