from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.template import loader
from django.utils.http import unquote, unquote_plus
from time import sleep
import os
import datetime
import subprocess

from .models import Video
from .forms import VideoForm
#from .forms import VideoForm
# Create your views here.
def index(request):
    videosDate = Video.objects.order_by('date').reverse()
    videosLikes = Video.objects.order_by('likes')
    videosSearched = Video.objects.order_by('searched')
    videosViews = Video.objects.order_by('views')
    if request.method == 'POST':
        action = request.POST.get('action', None)
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        email = request.POST.get('email', None)

        if action == 'registro':
            user = User.objects.create_user(username=username, password=password, email=email)
        elif action == 'inicio' or action == 'registro':
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('/')

    context = {
        'videos_by_date': videosDate,
        'videos_by_likes': videosLikes,
        'videos_by_searches': videosSearched,
        'videos_by_views': videosViews,
    }
    return render(request, 'index.html', context)

def video_details(request, pk):
    video = get_object_or_404(Video, pk=pk)
    video.views += 1
    video.save()
    context = {
        'video': video
    }
    return render(request, 'video.html', context)

def extraer_thumbnail(video):
    img_name = os.path.basename(unquote(video.video.url).replace(' ', '_')).split('.')[0]+'.jpg'
    date_url = str(datetime.datetime.now().year) + '/' + str(datetime.datetime.now().month) + '/'
    img_ruta = os.path.join(settings.BASE_DIR, 'media/img/')+date_url
    if not os.path.exists(img_ruta): os.makedirs(img_ruta)
    sleep(0.05)
    subprocess.call(['ffmpeg', '-i', os.path.join(settings.BASE_DIR, 'media/videos/' + date_url)+os.path.basename(unquote(video.video.url).replace(' ', '_')), '-ss', '00:00:00.000', '-vframes', '1', img_ruta+img_name])
    return 'img/'+date_url+img_name

@login_required
def subir(request):
    if request.method == 'POST':
        form = VideoForm(request.POST, request.FILES)
        if form.is_valid():
            video = form.save(commit=False)
            video.id_user = request.user
            video.thumbnail = extraer_thumbnail(video)
            video.save()
    else:
        form = VideoForm()
    template = loader.get_template('subir.html')
    context = {
        'form': form
    }
    return HttpResponse(template.render(context, request))
    

def quitar(request, pk):
    video = get_object_or_404(Video, pk=pk)
    context = {
        'video': video
    }
    return render(request, 'eliminarVideo.html', context)