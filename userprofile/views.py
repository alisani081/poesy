from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib.auth.decorators import login_required 
from django.contrib import messages
from django.http import JsonResponse, Http404
from django.core.mail import send_mail
from .forms import UserForm, ProfileForm, ContactForm
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from userprofile.models import Profile
from poems.models import Poem

from django.views.decorators.csrf import csrf_exempt
import cloudinary as cloudinary

# Welcome View
@login_required
def welcome_view(request):   
    if request.method == "POST": 
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        try:
            if user_form.is_valid and profile_form.is_valid:
                user_form.save()
                profile_form.save()
                messages.success(request, 'Your profile was updated successfully!')
                return redirect('profile', username=request.user.username)   
        except:       
            context = {
                'user_form': UserForm(request.POST, instance=request.user),
                'profile_form': ProfileForm(request.POST, instance=request.user.profile)
            }
            return render(request, "userprofile/welcome.html", context)

    context = {
        'user_form': UserForm(instance=request.user),
        'profile_form': ProfileForm(instance=request.user.profile)
    }
    return render(request, "userprofile/welcome.html", context)

# Profile view
def profile_view(request, username):     
    user_profile = get_object_or_404(User, username=username)    
    context = { 
        'user_profile': user_profile,
        "followers": user_profile.profile.followed_by.count(),
        "following": user_profile.profile.follows.count(),
    }
    return render(request, 'userprofile/profile.html', context)

@login_required
def edit_profile(request):
    if request.method == "POST":
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        try:
            if user_form.is_valid and profile_form.is_valid:                 
                user_form.save()
                profile_form.save()
                messages.success(request, 'Your profile was updated successfully!')
                return redirect('profile', username=request.user.username)
        except:       
            context = {                
                'user_form': UserForm(request.POST, instance=request.user),
                'profile_form': ProfileForm(request.POST, instance=request.user.profile)
            }
            return render(request, 'userprofile/edit_profile.html', context)
    context = {        
        'user_form': UserForm(instance=request.user),
        'profile_form': ProfileForm(instance=request.user.profile)
    }    
    return render(request, 'userprofile/edit_profile.html', context)

@login_required
def following_view(request, username):
    try:
        user_profile = User.objects.get(username=username)
        context = { 
            'my_followers': request.user.profile.followed_by.all(),
            'my_following': request.user.profile.follows.all(),
            'user_profile': user_profile,         
            'followers': user_profile.profile.followed_by.all(),
            'followings': user_profile.profile.follows.all()            
        }
        return render(request, 'userprofile/following.html', context)
    except User.DoesNotExist:
        return redirect('home')    

def follow(request, user):
    if request.is_ajax():
        followee = get_object_or_404(Profile, pk=user)
        data = dict()
        follower = request.user.profile

        # Checks user not following self or non-following
        if followee == follower or follower.is_following(followee):
            data = {
                'success': False            
            }
        else:  
            follower.follow(followee)    
            data = {
                'success': True   
            }
            send_mail(
                f'{follower.user.username} just followed you. Check out his profile.',
                f'''Hello {followee.user.first_name},
                    @{follower.user.username} just followed you. Click here to visit their profile.
                ''',
                'no-reply@localhost',
                [f'{followee.user.email}'],
                fail_silently=False,
            )
        return JsonResponse(data)

def unfollow(request, user):   
    if request.is_ajax():  
        followee = get_object_or_404(Profile, pk=user)
        data = dict()
        unfollower = request.user.profile

        # Checks user not unfollowing self or non-following
        if followee == unfollower or not unfollower.is_following(followee):
            data = {
                'success': False
            }
        else:  
            unfollower.unfollow(followee)      
            data = {
                'success': True   
            }
        return JsonResponse(data)

def bookmark(request, poem):
    if request.is_ajax():
        poem = get_object_or_404(Poem, pk=poem)
        data = dict()
        user_profile = request.user.profile

        # Checks user not following self or non-following
        if user_profile.has_bookmarked(poem):
            data = {
                'success': False            
            }
        else:  
            user_profile.bookmark(poem)  
            data = {
                'success': True   
            }
        return JsonResponse(data)

def unbookmark(request, poem):
    if request.is_ajax():
        poem = get_object_or_404(Poem, pk=poem)
        data = dict()
        user_profile = request.user.profile

        # Checks user not following self or non-following
        if user_profile.has_bookmarked(poem):
            user_profile.unbookmark(poem)  
            data = {
                'success': True            
            }
        else:  
            data = {
                'success': False   
            }
        return JsonResponse(data)

def like(request, poem):
    if request.is_ajax():
        poem = get_object_or_404(Poem, pk=poem)
        data = dict()
        user_profile = request.user.profile
        
        if user_profile.has_liked(poem):
            data = {
                'success': False            
            }
        else:  
            user_profile.like(poem) 
            data = {
                'success': True,
                'likes': poem.liked_by.count()
            }
            send_mail(
                f'@{user_profile.user.username} just liked your poem.',
                f'''Hello {poem.poet.user.first_name},
                    @{user_profile.user.username} just liked your poem. {poem.title}.
                ''',
                'no-reply@localhost',
                [f'{poem.poet.user.email}'],
                fail_silently=False,
            )
        return JsonResponse(data)

def unlike(request, poem):
    if request.is_ajax():
        poem = get_object_or_404(Poem, pk=poem)
        data = dict()
        user_profile = request.user.profile
        
        if user_profile.has_liked(poem):
            user_profile.unlike(poem)  
            data = {
                'success': True,
                'likes': poem.liked_by.count()            
            }
        else:  
            data = {
                'success': False   
            }
        return JsonResponse(data)

@csrf_exempt
def delete_picture(request):
    if request.is_ajax():
        user_profile = get_object_or_404(Profile, user=request.user)
        data = dict()    
        pub_id = f'userprofile/profile_pictures/{request.user.username}_avi'

        if user_profile.image is not None:
            user_profile.image = ''
            user_profile.save()
            cloudinary.uploader.destroy(pub_id)
            data = {
                'success': True
            }
        else:         
            data = {
                'success': False
            }
        return JsonResponse(data)
    else:
        raise Http404

def index_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    return render(request, 'landing/landing_page.html')

@login_required
def home_view(request):
    user_profile = request.user.profile
    followings = user_profile.follows.select_related().all()
    myFollowing = [following.id for following in followings]
    myFollowing.append(user_profile.id)
    mytl = Poem.objects.select_related().filter(poet__in=(myFollowing))

    paginator = Paginator(mytl, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'userprofile/home.html', {'page_obj': page_obj})

@csrf_exempt
def upload_picture(request):
    if request.is_ajax():
        user_profile = get_object_or_404(Profile, user=request.user)    
        data = dict()
        pub_id = f'userprofile/profile_pictures/{request.user.username}_avi'

        picture = request.POST.get('picture')
        file_ext =  request.POST.get('ext')
        
        accepted_ext = ['image/png', 'image/jpg', 'image/jpeg']
        if file_ext not in accepted_ext:        
            data = {
                    'success': False,
                    'error': 'Please, upload a valid picture.'
                }
        else:
            try:
                response =  cloudinary.uploader.upload(
                                picture,                    
                                public_id = pub_id,
                                width = 150,
                                height = 150,
                                crop = 'thumb',
                                overwrite = True,
                )                
                user_profile.image = response['secure_url']
                user_profile.save()
                data = {
                    'success': True,
                }
            except:
                data = {
                    'success': False,
                    'error': 'Error encountered while uploading your profile picture. Please, try again.'
                }                   
        return JsonResponse(data)
    raise Http404

def about_view(request):
    return render(request, 'landing/about.html')

def contact_view(request):
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            subject = form.cleaned_data['subject']
            from_email = form.cleaned_data['email']
            message = f""" Message from {name}, {form.cleaned_data['message']}

            Contact Form on Poesy.com.ng
            """
            try:
                send_mail(subject, message, from_email, ['admin@example.com'])
                message = 'Your message was sent successfully!'
            except:
                message = 'Invalid header found.'
            return render(request, 'landing/contact.html', {'message': message, 'form': ContactForm()})
        else:
            message = 'Please, fill out the form properly.'
            return render(request, 'landing/contact.html', {'message': message, 'form': ContactForm(request.POST)})
    form = ContactForm()

    return render(request, 'landing/contact.html', {'form': form})
