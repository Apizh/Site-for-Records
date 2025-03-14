from django.core.exceptions import ValidationError
from .models import Category, Records, TagPost
from django import forms


class AddPostForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Получаем текущего пользователя
        super().__init__(*args, **kwargs)

        if user:
            # Фильтруем категории и теги по текущему пользователю
            self.fields['cat'].queryset = Category.objects.filter(author=user)
            self.fields['tags'].queryset = TagPost.objects.filter(author=user)

            # Изменяем метку для поля tags
            self.fields['tags'].label = 'Выберите темы'

            # Применяем классы для полей
            self.fields['rating'].widget.attrs.update({
                'class': 'form-select rating',  # Добавляем класс для rating
            })

            self.fields['cat'].widget.attrs.update({
                'class': 'form-select cat',  # Добавляем класс для cat
            })

            self.fields['is_published'].widget.attrs.update({
                'class': 'form-select is-published',  # Добавляем класс для is_published
            })

            self.fields['tags'].widget.attrs.update({
                'class': 'form-select tags',  # Добавляем класс для tags
            })

    cat = forms.ModelChoiceField(queryset=Category.objects.all(), empty_label="Категория не выбрана", label="Категории")
    tags = forms.ModelMultipleChoiceField(queryset=TagPost.objects.all(), required=False)

    rating = forms.ChoiceField(
        choices=[(str(i), str(i)) for i in range(1, 11)],
        label="Рейтинг"
    )

    class Meta:
        model = Records
        fields = ['title', 'content', 'photo', 'rating', 'is_published', 'cat', 'tags']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'content': forms.Textarea(attrs={'cols': 50, 'rows': 5}),
        }

    def clean_rating(self):
        rating = int(self.cleaned_data.get('rating'))
        if rating < 1 or rating > 10:
            raise ValidationError("Рейтинг должен быть от 1 до 10")
        return rating

    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) > 50:
            raise ValidationError("Длина превышает 50 символов")
        return title

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get('title')
        user = self.instance.author  # assuming you have an 'author' field in your model, and it's set correctly
        if Records.objects.filter(title=title, author=user).exists():
            raise ValidationError("У вас уже есть запись с таким названием")
        return cleaned_data


class BaseCategoryTagForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def clean_field(self, field_name, model, user_field, error_message):
        value = self.cleaned_data[field_name]

        # Проверка длины
        if len(value) > 50:
            raise ValidationError("Длина превышает 50 символов")

        # Проверка уникальности для текущего пользователя
        if model.objects.filter(**{field_name: value, user_field: self.user}).exists():
            raise ValidationError(error_message)

        return value


from .models import Category, TagPost


class AddCategoryForm(BaseCategoryTagForm):
    class Meta:
        model = Category
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-input'}),
        }

    def clean_name(self):
        return self.clean_field('name', Category, 'author', "Категория с таким названием уже существует.")


class AddTagForm(BaseCategoryTagForm):
    class Meta:
        model = TagPost
        fields = ['tag']
        widgets = {
            'tag': forms.TextInput(attrs={'class': 'form-input'}),
        }

    def clean_tag(self):
        return self.clean_field('tag', TagPost, 'author', "Тег с таким названием уже существует.")


class UploadFileForm(forms.Form):
    file = forms.ImageField(label="Файл")
