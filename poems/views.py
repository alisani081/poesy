import random
from django.shortcuts import render, redirect, get_object_or_404
from django.template import loader
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.http import HttpResponse, Http404, JsonResponse
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Count
from django.db.models import Q
from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector
from .forms import PoemForm
from django.contrib.auth.models import User
from poems.models import Poem, Topic
from userprofile.models import Profile
   
@login_required()
def add_poem_view(request):
    if request.method == "POST":
        form = PoemForm(request.POST)
        if form.is_valid():
            poem = form.save(commit=False)
            poem.poet = request.user.profile
            poem.save()
            messages.success(request, 'New poem added successfully!')
            return redirect('poem', username=request.user.username, slug=poem.slug)
    else:
        form = PoemForm()
    return render(request, 'poems/new_poem.html', {'form': form})

def poem_view(request, username, slug):
    poem = get_object_or_404(Poem, slug=slug)
    if str(poem.poet) == str(username):
        return render(request, 'poems/poem.html', {'poem': poem})
    else:
        raise Http404('Page not found!')

@login_required
def edit_poem_view(request, slug):
    poem = get_object_or_404(Poem, slug=slug)
    owner = request.user.profile
    if poem.poet != owner:
        raise Http404('Resource Not Found')

    if request.method == "POST":
        form = PoemForm(request.POST, instance=poem)
        if form.is_valid():
            poem = form.save(commit=False)
            poem.poet = request.user.profile
            poem.updated_at = timezone.now()
            poem.save()
            messages.success(request, 'Poem updated successfully!')
            return redirect('poem', username=owner.user.username, slug=poem.slug)
    else:  
        form = PoemForm(instance=poem)      
    return render(request, 'poems/edit_poem.html', {'form': form})

@login_required
def explore_view(request):
    # explore
    context = {
        'topics': Topic.objects.all(),
        'top_poems':  Poem.objects.select_related().annotate(num_likes=Count('liked_by')).order_by('-num_likes')[:20],
        'new_poems': Poem.objects.select_related().all().order_by('-published_at')[:20]
    }
    return render(request, 'poems/explore.html', context)

def poems_view(request, topic):
    topic = get_object_or_404(Topic, topic=topic)
    poems = topic.poems.all()[:20]
    context = {
        'topic': topic,
        'poems': poems
    }
    return render(request, 'poems/poems.html', context)

@login_required
def bookmarks_view(request, username):      
    return render(request, 'poems/bookmarks.html')

@login_required
def search_view(request):    
    return render(request,'poems/search.html')   

def search_engine(request):
    search_query = request.GET.get('q')
    template = loader.get_template('poems/search_results.html')
    data = dict()
    if request.is_ajax():
        user_profiles = User.objects.filter(
                            Q(username__istartswith=search_query) | Q(first_name__istartswith=search_query)
                        ).exclude(is_staff=True)[:10]        
        html_view = template.render({'results': user_profiles}, request)
        data = {            
            'html_view': html_view
        }
        return JsonResponse(data, safe=False)
