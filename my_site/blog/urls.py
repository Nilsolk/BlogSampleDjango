from django.urls import path
from . import views

app_name = 'blog'
urlpatterns = [
    # path('', views.post_list,name='post_list'),
    # path('<int:id>/', views.post_detail, name ='post_detail')
    path('', views.PostListView.as_view(), name="post_list"),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/', views.post_detail, name ='post_detail'),
    path('<int:post_id>/comment/',views.post_comment, name = 'post_comment'),
    path('new_list/', views.new_post_list , name = "new_post_list"),
    path('contact/', views.contact_us_form, name = 'contact'),
    path('contact/success/', views.contact_success, name ='contact_success'),

]
