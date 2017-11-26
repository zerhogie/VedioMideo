from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.db.models import Q
from django.contrib.auth import authenticate, login
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.template import loader
from django.utils.http import unquote, unquote_plus
from django.views.generic import ListView
from django.views.generic import DetailView
from itertools import chain
from time import sleep
import os
import datetime
import subprocess

from .models import Video
from .forms import VideoForm
# Create your views here.

#def video_details(request, pk):
#    video = get_object_or_404(Video, pk=pk)
#    video.views += 1
#    video.save()
#    context = {
#        'video': video
#    }
#    return render(request, 'video.html', context)

def busqueda(request):
    query = request.GET.get('q', '')
    if query:
        qset = (
            Q(title__icontains=query) |
            Q(sumary__icontains=query) |
            Q(id_user__username__icontains=query)
        )
        results = Video.objects.filter(qset).distinct()
    else:
        results = []
    return render_to_response("search.html" ,{
        "results": results,
        "query": query
    })
    

def extraer_thumbnail(video):
    img_name = os.path.basename(unquote(video.video.url).replace(' ', '_')).split('.')[0]+'.jpg'
    date_url = str(datetime.datetime.now().year) + '/' + str(datetime.datetime.now().month) + '/'
    img_ruta = os.path.join(settings.BASE_DIR, 'media/img/')+date_url
    if not os.path.exists(img_ruta): os.makedirs(img_ruta)
    sleep(0.05)
    subprocess.call(['ffmpeg', '-i', os.path.join(settings.BASE_DIR, 'media/videos/' + date_url)+os.path.basename(unquote(video.video.url).replace(' ', '_')), '-ss', '00:00:00.000', '-vframes', '1', img_ruta+img_name, '-y'])
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

class VideoListView(ListView):
    model = Video
    template_name = "index.html"

    def post(self, request, *args, **kwargs):
        action = request.POST.get('action', None)
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        email = request.POST.get('email', None)
        orden = request.POST.get('orden', None)
        if action == 'registro':
            user = User.objects.create_user(username=username, password=password, email=email)
        if action == 'inicio' or action == 'registro':
            aut = authenticate(username=username, password=password)
            if aut is not None:
                login(request, aut)
                return redirect('/')
        def get_ordering(self):
            ordering = self.GET.get('ordering', 'date').reverse()
            return ordering

def mostrar(request, orden):
    if orden in ("date", "views", "searched", "likes"):
        ordenados = Video.objects.order_by(orden)
        if orden == 'date' or orden == 'views': ordenados = ordenados.reverse()
        template = loader.get_template("mostrando.html")
        return HttpResponse(template.render({'lista_videos': ordenados}, request))
    else:
        porTitulo = Video.objects.filter(title__icontains=orden)
        print('AQUI!!!:  -->>',orden)
        #buscados = list(chain(porTitulo, article_list, post_list))
        template = loader.get_template("mostrando.html")
        return HttpResponse(template.render({'lista_videos': porTitulo}, request))

class VideoDetailView(DetailView):
    model = Video
    template_name = "video.html"

    def get_object(self):
        video = super(VideoDetailView, self).get_object() # LLama a la superclase
        video.views += 1 
        video.save()
        return video # Retorna el objeto
