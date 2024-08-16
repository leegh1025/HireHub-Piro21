from django.urls import path
from . import views


app_name = 'applicants'

urlpatterns = [
    path("interview", views.interview, name="interview"),
    path('interview/change_status/<str:status_zone_id>/<str:applicant_id>/', views.change_status, name='change_status'),
    path("document", views.document, name="document"),
    path('search_applicant/', views.search_applicant, name='search_applicant'),
    path("document/profile/<int:pk>", views.profile, name='profile'),
    path("pass_document/<int:applicant_id>/", views.pass_document, name='pass_document'),
    path("fail_document/<int:applicant_id>/", views.fail_document, name='fail_document'),
    path('apply/<int:pk>/', views.apply, name='apply'),
    path("schedule", views.schedule, name='schedule'),
    path("auto_schedule", views.auto_schedule, name='auto_schedule'),
    path("document/profile/<int:pk>/comment/", views.comment, name='comment'),
    path("document/profile/<int:pk>/comment/<int:comment_id>/delete/", views.delete_comment, name='delete_comment'),
    path('rankings/', views.applicant_rankings, name='rankings'),
    path("schedule/update/<int:pk>s", views.schedule_update, name="schedule_update"),
    # path('document/profile/<int:pk>/evaluate', views.evaluate, name='evaluate')
    path("applycheck/", views.apply_check, name='apply_check'),
    path("applyresult/", views.apply_result, name='apply_result'),
    path("timeover/", views.apply_timeover, name='timeover'),
    path("document/profile/<int:pk>/question/", views.question, name='question'),
    path('document/profile/<int:pk>/question/<int:question_id>/delete/', views.delete_question, name='delete_question'),
    path('document/profile/<int:pk>/question/<int:answer_id>/answer_delete/', views.delete_answer, name='delete_answer'),
    path('document/profile/<int:pk>/delete/', views.delete_recording, name='delete_recording'),
]