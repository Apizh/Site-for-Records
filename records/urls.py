from django.urls import path
from . import views


urlpatterns = [
    path('', views.RecordsHome.as_view(), name='home'),
    path('about/', views.AboutSite.as_view(), name='about'),
    path('contacts/', views.Contacts.as_view(), name='contacts'),
    path('addpost/', views.AddPost.as_view(), name='addpost'),
    path('post/<slug:post_slug>/', views.ShowPost.as_view(), name='post'),
    path('tag/<slug:tag_slug>/', views.TagPostList.as_view(), name='tag'),
    path('update/<slug:slug>/', views.UpdatePost.as_view(), name='update_post'),
    path('delete/<slug:slug>/',views.DeletePost.as_view() , name='delete_post'),
    path('toggle_flag/<slug:slug>/', views.ToggleFlagView.as_view(), name='toggle_flag'),
    path('category/<slug:cat_slug>/', views.RecordsCategory.as_view(), name='category'),
    path('addcategory/', views.AddCategory.as_view(), name='addcategory'),
    path('editcategory/<slug:slug>/', views.CategoryUpdateView.as_view(), name='editcategory'),
    path('addtag/', views.AddTag.as_view(), name='addtag'),
    path('edittag/<slug:slug>', views.TagUpdateView.as_view(), name='edittag'),
    path('deletecategory/<slug:slug>/', views.delete_object, {'model': 'category'}, name='deletecategory'),
    path('deletetag/<slug:slug>/', views.delete_object, {'model': 'tag'}, name='deletetag'),
]
