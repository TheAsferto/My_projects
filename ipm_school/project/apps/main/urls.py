from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .forms import LoginForm
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path('registration_teacher/', views.TeacherSignUpView.as_view(), name='registration_teacher'),
    path('registration_student/', views.StudentSignUpView.as_view(), name='registration_student'),
    path('authorization/', views.LoginView.as_view(template_name="authorization/authorization.html",
                                                   authentication_form=LoginForm
                                                   ),
         name='authorization'),
    path('update_authorization/', views.update_authorization, name='update_authorization'),
    path('page_student_lk/', views.page_student_lk, name='page_student_lk'),
    path('page_teacher_lk/', views.page_teacher_lk, name='page_teacher_lk'),
    path('page_teach_settings/', views.page_teach_settings, name='page_teach_settings'),
    path('page_student_class/', views.page_student_class, name='page_student_class'),
    path('page_teacher_class/', views.page_teacher_class, name='page_teacher_class'),
    path('logout/', auth_views.LogoutView.as_view(), {'next_page':settings.LOGOUT_REDIRECT_URL}, name='logout'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
