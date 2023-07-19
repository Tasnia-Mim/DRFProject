from django.urls import path

from . import views

app_name = 'blog'


urlpatterns = [
    path('doctor/blogs/blog', views.BlogCreatView.as_view(), name='BlogCreatView'), 
    path('doctor/blogs', views.BlogList.as_view(), name='BloglistView'),     
    path('doctor/blogs/<uuid:uid>', views.BlogDetailView.as_view(), name='blog_detail'),
          
    
]
