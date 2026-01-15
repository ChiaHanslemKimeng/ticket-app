from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from dashboardApp.form import TicketForm, ReviewForm, profilform
from django.utils import timezone
from dashboardApp.models import Ticket, Review, UserFollows, profilemodel
from django.db.models import CharField, Value
from itertools import chain
from django.contrib.auth.models import User


# to create a ticket ==============================================================
def createTicket(request):
    if request.method == "POST":
        form = TicketForm(request.POST, request.FILES)
        if form.is_valid():
            Ticket.objects.create(user=request.user, 
                                title = form.cleaned_data['title'],
                                description = form.cleaned_data['description'],
                                image = form.cleaned_data['image'])
            return redirect('dashboardApp:homepage')
    else:
        form = TicketForm()
        return render(request, 'dashboardTemplate/createTicket.html', {'form':form})
    
# to create a review ==============================================================
def createReview(request):
    if request.method == "POST":
        ticketform = TicketForm(request.POST, request.FILES)
        reviewform = ReviewForm(request.POST)
        if ticketform.is_valid() and reviewform.is_valid():
            Ticket.objects.create(user=request.user, 
                                title = ticketform.cleaned_data['title'],
                                description = ticketform.cleaned_data['description'],
                                image = ticketform.cleaned_data['image'])
            Review.objects.create(user=request.user, 
                                ticket = Ticket.objects.last(), #to take the last ticket created 
                                headline = reviewform.cleaned_data['headline'],
                                rating = reviewform.cleaned_data['rating'],
                                body = reviewform.cleaned_data['body'])
            return redirect('dashboardApp:homepage')
    else:
        form = TicketForm()
        reviewform = ReviewForm()
        return render(request, 'dashboardTemplate/createReview.html', {'form':form, 'reviewform':reviewform})


# to display only my post (logged in user)
def mypost(request):
    posts = []
    ticket = Ticket.objects.filter(user=request.user)
    ticket = ticket.annotate(content_type= Value('TICKET', CharField()))

    user_review = Review.objects.filter(user=request.user)
    user_review = user_review.annotate(content_type= Value('REVIEW', CharField()))

    sort_post = sorted(chain(user_review, ticket), key=lambda post:
                       post.time_created, reverse=True)
    for post in sort_post:
        if post.content_type=='TICKET':
            post_dict = {'is_ticket': True,
                         'tick_title': post.title,
                         'tick_description': post.description,
                         'tick_datecreated': post.time_created,
                         'tick_timecreated': post.time_created,
                         'tick_image': post.image,
                         'tick_id': post.id}
        else:
            tick=post.ticket
            post_dict={'is_ticket': False,
                        'tick_title': tick.title,
                        'tick_description': tick.description,
                        'tick_timecreated': tick.time_created,
                        'tick_image': tick.image,
                        'rev_time': post.time_created,
                        'rev_headline': post.headline,
                        'rev_body': post.body,
                        'yellow_star': range(post.rating),
                        'empty_star': range(5-post.rating),
                        'rev_answer_to':  post.ticket.user.username,
                        'rev_id': post.id}
        posts.append(post_dict)
    return render(request, "dashboardTemplate/yourPost.html", {"posts":posts}) 

# edit ticket button =============================================
def editbtn(request, id):
    try:
        ticket = Ticket.objects.get(pk=id)
        if ticket.user != request.user:
            return redirect('dashboardApp:mypost')
    except Ticket.DoesNotExist:
        return redirect('dashboardApp:mypost')

    if request.method == "POST":
        form = TicketForm(request.POST, request.FILES)
        if form.is_valid():
            pers = form.save(commit=False)
            pers.id = ticket.id
            pers.user = ticket.user
            pers.time_created = ticket.time_created
            pers.save()
            return redirect('dashboardApp:mypost')
    else:
        form = TicketForm(instance = ticket)
        return render(request, 'dashboardTemplate/editpost.html', {"form":form})

# delete ticket button =========================================
def deletebtn(request, id):
    try:
        ticket = Ticket.objects.get(pk=id)
        if ticket.user != request.user:
            return redirect('dashboardApp:mypost')
    except Ticket.DoesNotExist:
        return redirect('dashboardApp:mypost')
    
    post = Ticket.objects.get(id = id)
    if request.method == "POST":
        post.delete()
        return redirect('dashboardApp:mypost')
    return render(request, 'dashboardTemplate/deletepost.html', {"post":post})

# edit review button =====================================================
def revEdit(request, id):
    try:
        review = Review.objects.get(pk=id)
        if review.user != request.user:
            return redirect('dashboardApp:mypost')
    except Review.DoesNotExist:
        return redirect('dashboardApp:mypost')

    if request.method == "POST":
        reviewform = ReviewForm(request.POST)
        if reviewform.is_valid():
            rev_pers = reviewform.save(commit=False) 
            rev_pers.id = review.id
            rev_pers.ticket = review.ticket
            rev_pers.user = review.user
            rev_pers.time_created = review.time_created
            rev_pers.save()
            return redirect('dashboardApp:mypost')
    else:
        reviewform = ReviewForm(instance = review)
        return render(request, 'dashboardTemplate/editRev.html', {"reviewform":reviewform})
    
# delete review button =========================================
def revDel(request, id):
    try:
        review = Review.objects.get(pk=id)
        if review.user != request.user:
            return redirect('dashboardApp:mypost')
    except Review.DoesNotExist:
        return redirect('dashboardApp:mypost')
    
    post = Review.objects.get(id = id)
    if request.method == "POST":
        post.delete()
        return redirect('dashboardApp:mypost')
    return render(request, 'dashboardTemplate/deletepost.html', {"post":post})

# display feed ===============================================================
@login_required
def feed(request):
    try:
        profilePhoto = profilemodel.objects.get(user=request.user)
    except:
        profilePhoto = None
    
    reviews = Review.objects.all()
    ticketUser = Ticket.objects.filter(user=request.user)
    ticketId = [tick.id for tick in ticketUser]
    review_ticket_id = [review.ticket.id for review in reviews]
    review_from_ticket = Review.objects.filter(ticket__in=list(set(ticketId) & set(review_ticket_id)))
    review_user = Review.objects.filter(user=request.user).exclude(pk__in=review_from_ticket)
    review_user = review_user.annotate(content_type=Value('REVIEW', CharField()))
    
    users_followed = UserFollows.objects.filter(user_id=request.user)
    review_from_followers = Review.objects.filter(user__in=[userfollow.followed_user for userfollow in users_followed])
    review_from_followers = review_from_followers.annotate(content_type=Value('REVIEW', CharField()))
    review_from_ticket = review_from_ticket.annotate(content_type=Value('REVIEW', CharField()))
    
    
    ticket_from_followers = Ticket.objects.filter(user__in=[userfollow.followed_user for userfollow in users_followed])
    ticket_from_followers = ticket_from_followers.annotate(content_type=Value('TICKET', CharField()))
    ticketUser = ticketUser.annotate(content_type=Value('TICKET', CharField()))

    posts = sorted(chain(review_user, review_from_followers, review_from_ticket, ticket_from_followers, ticketUser), key=lambda post: post.time_created, reverse=True)
    ticket_response = Ticket.objects.filter(pk__in=review_ticket_id)
    
    return render(request, 'dashboardTemplate/dashboard.html', {'posts': posts, 'ticket_response': ticket_response, 'profilePhoto':profilePhoto})


def follow_user(request):
    user_follow_you = [user_follow.user.username for user_follow in UserFollows.objects.filter(followed_user=request.user.id)]
    users_follow = UserFollows.objects.filter(user_id=request.user)
    user_to_exclude = [user_exclude.followed_user.username for user_exclude in users_follow]
    user_to_exclude.append(request.user.username)
    user_to_follow = User.objects.exclude(username__in = user_to_exclude)
    if request.method == 'POST':
        follow_user = User.objects.get(pk=request.POST["follow_user"])
        if follow_user in user_to_follow:
            UserFollows(user=request.user, followed_user=follow_user).save()
    users_follow = UserFollows.objects.filter(user_id=request.user)
    return render(request, 'dashboardTemplate/followers.html', {'user_to_follow': user_to_follow, 'user_follow_you': user_follow_you, 'users_follow':users_follow})

# unfollow user ========================================================
def unfollow(request, id):
    try:
        unfollow_user = UserFollows.objects.get(user = request.user, followed_user = id)
    except:
        UserFollows.DoesNotExist
        return redirect("dashboardApp:followers")
    if request.method == 'POST':
        unfollow_user.delete()
        return redirect("dashboardApp:followers")
    
# post ticket review =====================================================================
def post_ticket_review(request, id):
        ticket_to_review = Ticket.objects.get(pk=id)
        if request.method == "POST":
                reviewform = ReviewForm(request.POST)
                if reviewform.is_valid():
                    Review.objects.create(user=request.user, 
                                ticket = ticket_to_review,
                                headline = reviewform.cleaned_data['headline'],
                                rating = reviewform.cleaned_data['rating'],
                                body = reviewform.cleaned_data['body'])
                    return redirect('dashboardApp:mypost')
        else:
            reviewform = ReviewForm()
        return render(request, 'dashboardTemplate/review_in_response.html', {"ticket_to_review":ticket_to_review, "reviewform":reviewform})

def profile(request):
    if request.method=="POST":
        form=profilform(request.POST,request.FILES)
        if form.is_valid():
            prof=form.save(commit=False)
            prof.user=request.user
            if profilemodel.objects.filter(user_id=request.user.id).exists():
                for i in profilemodel.objects.filter(user_id=request.user.id):
                    i.image=prof.image
                    i.gender=prof.gender
                    i.date_profile=timezone.now
                    i.save()
                    return redirect('dashboardApp:homepage')
            else:
                prof.date_profile=timezone.now
                prof.save()
                return redirect('dashboardApp:homepage')
            
    else:
        form=profilform()
        return render(request,'dashboardTemplate/profile.html',{'form':form})

