from django.shortcuts import render
import folium
from pumaguaAPP.models import bebederos
from django.db.models import Q
from folium.plugins import LocateControl

# Create your views here.
def index(request):

    datosBebederos = bebederos.objects.all()
    m = folium.Map(location = [19.32, -99.18], zoom_start = 13)
    LocateControl().add_to(m)

    if 'q' in request.GET:
        q = request.GET['q']
        multiple_q = Q(Q(nombre__icontains=q) | Q(ubicacion__icontains=q) | Q(institucion__icontains=q) | Q(palabras_clave__icontains=q))
        data = bebederos.objects.filter(multiple_q)
        for coordenada in data:
            datos = (coordenada.latitud, coordenada.longitud)
            folium.Marker(datos, tooltip='Click me!', popup=coordenada.nombre + ',' + coordenada.ubicacion + '\n').add_to(m)
    else:
        for coordenada in datosBebederos:
            datos = (coordenada.latitud, coordenada.longitud)
            folium.Marker(datos, tooltip='Click me!', popup=coordenada.nombre + ',' + coordenada.ubicacion + '\n').add_to(m)

    contexto = {'map': m._repr_html_()}

    return render(request, "index.html", contexto)
