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
from io import StringIO
from lxml import etree
from time import sleep
import datetime
import os
import subprocess

from .models import Video, New
from .forms import VideoForm, XMLForm
# Create your views here.

#def video_details(request, pk):
#    video = get_object_or_404(Video, pk=pk)
#    video.views += 1
#    video.save()
#    context = {
#        'video': video
#    }
#    return render(request, 'video.html', context)

def addusers(xml):
    tree= etree.parse(xml)
    users = tree.getroot()
    for us in users:
        user = User.objects.create_user(username=us[0].text, password=us[1].text, email=us[2].text)

def is_validXML_user(xml):
    xsd = 'static/scripts/users.xsd'
    treexsd = etree.parse(os.path.join(settings.BASE_DIR, xsd))
    treexml = etree.parse(xml)
    xsdCad = etree.tostring(treexsd, pretty_print=True, encoding='utf-8')
    xmlCad = etree.tostring(treexml, pretty_print=True, encoding='utf-8')
    decXSD = xsdCad.decode("utf-8")
    decXML = xmlCad.decode("utf-8")

    f = StringIO(decXSD)
    xmlschema_doc = etree.parse(f)
    xmlschema = etree.XMLSchema(xmlschema_doc)

    validar = StringIO(decXML)
    xmlSimple_doc = etree.parse(validar)
    return xmlschema.validate(xmlSimple_doc)

def extraer_thumbnail(video):
    img_name = os.path.basename(unquote(video.video.url).replace(' ', '_')).split('.')[0]+'.jpg'
    date_url = str(datetime.datetime.now().year) + '/' + str(datetime.datetime.now().month) + '/'
    img_ruta = os.path.join(settings.BASE_DIR, 'media/img/')+date_url
    if not os.path.exists(img_ruta): os.makedirs(img_ruta)
    sleep(0.05)
    subprocess.call(['ffmpeg', '-i', os.path.join(settings.BASE_DIR, 'media/videos/' + date_url)+os.path.basename(unquote(video.video.url).replace(' ', '_')), '-ss', '00:00:00.000', '-vframes', '1', img_ruta+img_name, '-y'])
    return 'img/'+date_url+img_name

def transcoding(video):
    print("Iniciando transcoding...")
    original = os.path.basename(unquote(video.video.url).replace(' ', '_'))
    date_url = str(datetime.datetime.now().year) + '/' + str(datetime.datetime.now().month) + '/'
    convertido = original.split('.')[0]+'.mp4'
    ruta = os.path.join(settings.BASE_DIR, 'media/videos/') + date_url
    subprocess.call(['ffmpeg', '-i', ruta + original, ruta + convertido,],)
    os.remove(ruta + original)
    return ruta + convertido

@login_required
def subir(request):
    if request.method == 'POST':
        form = VideoForm(request.POST, request.FILES)
        if form.is_valid():
            video = form.save(commit=False)
            video.id_user = request.user
            video.save()
            if not video.video.url.endswith(".mp4"):
                video.video = transcoding(video)
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
        form = XMLForm(request.POST, request.FILES)

        if action == 'registro':
            user = User.objects.create_user(username=username, password=password, email=email)
        if action == 'inicio' or action == 'registro':
            aut = authenticate(username=username, password=password)
            if aut is not None:
                login(request, aut)
                return redirect('/')
        if action == 'importar':
            if form.is_valid():
                handle_uploaded_file(request.FILES['xml'])
                xml = os.path.join(settings.MEDIA_ROOT, 'tmp/users.xml')
                if form.password == request.user.password:
                    if is_validXML_user(xml):
                        addusers(xml)
                    return redirect('/')
                else:
                    return HttpResponse("No fue válida la autenticación, no puedes subir archivos!<p></p> <a href='/' class='btn btn-info'>Regresar</a>")
            else:
                print("Problemas con el archivo")
                alert = New(alert="El XML no es válido", 
                    sumary="Al revisar la validez del XML enviado encontramos errores en su archivo. Recuerde que para registrar un usuario solo se requiere nombre, contraseña y su correo electrónico",
                    id_user=request.user)
                return redirect('/')

        def get_ordering(self):
            ordering = self.GET.get('ordering', 'date').reverse()
            return ordering

def handle_uploaded_file(f):
    with open(os.path.join(settings.BASE_DIR, 'media/tmp/users.xml'), 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

def mostrar(request, orden):
    if orden in ("date", "views", "searched", "likes"):
        ordenados = Video.objects.order_by(orden)
        if orden == 'date' or orden == 'views': ordenados = ordenados.reverse()
        template = loader.get_template("mostrando.html")
        return HttpResponse(template.render({'lista_videos': ordenados}, request))
    else:
        porTitulo = Video.objects.filter(title__icontains=orden)
        for video in porTitulo:
            video.searched += 1
            video.save()
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
