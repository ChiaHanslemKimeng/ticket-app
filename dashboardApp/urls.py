from django.urls import path
from dashboardApp import views

app_name = "dashboardApp"

urlpatterns = [
    path("homepage/", views.feed, name="homepage"),
    path("followers/", views.follow_user, name="followers"),
    path("createReview/", views.createReview, name="createReview"),
    path("createReviewInResponse/<int:id>/", views.post_ticket_review, name="createReviewInResponse"),
    path("createTicket/", views.createTicket, name="createTicket"),
    path("mypost/", views.mypost, name="mypost"),
    path("editpost/<int:id>/", views.editbtn, name="editbtn"),
    path("deletepost/<int:id>/", views.deletebtn, name="deletebtn"),
    path("editreview/<int:id>/", views.revEdit, name="revEdit"),
    path("deletereview/<int:id>/", views.revDel, name="revDel"),
    path("unfollowUser/<int:id>/", views.unfollow, name="unfollow"),
    path("prof/",views.profile,name="profilepage"),
]
