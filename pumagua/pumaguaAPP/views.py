from django.shortcuts import render
import folium
from pumaguaAPP.models import bebederos
from django.db.models import Q
from folium.plugins import LocateControl
import json

# Create your views here.
def index(request):

    datosBebederos = bebederos.objects.all()
    m = folium.Map(location = [19.32, -99.18], zoom_start = 13, height = 500)
    LocateControl().add_to(m)

    with open('rutas_pumabus.json') as json_file:
        parseo_rutas = json.load(json_file)

    # poner las otras rutas acá
    gr11 = folium.FeatureGroup(name='Ruta 11', show=False).add_to(m)
    folium.PolyLine(parseo_rutas[10]['coordenadas'], tooltip='Ruta 11', color='#680084', stroke=True).add_to(gr11)
    
    gr12 = folium.FeatureGroup(name='Ruta 12', show=False).add_to(m)
    folium.PolyLine(parseo_rutas[11]['coordenadas'], tooltip='Ruta 12', color='#BD7EB4', stroke=True).add_to(gr12)
    
    gr13 = folium.FeatureGroup(name='Ruta 13', show=False).add_to(m)
    folium.PolyLine(parseo_rutas[12]['coordenadas'], tooltip='Ruta 13', color='#8FD7D4', stroke=True).add_to(gr13)
    
    bicipuma = folium.FeatureGroup(name='Ruta Bicipuma', show=False).add_to(m)
    folium.PolyLine(parseo_rutas[13]['coordenadas'], tooltip="Ruta Bicipuma", color='#00C528', stroke=True).add_to(bicipuma)
    
    folium.LayerControl().add_to(m)

    mensaje = ''

    if 'q' in request.GET:
        q = request.GET['q']
        multiple_q = Q(Q(nombre__icontains=q) | Q(ubicacion__icontains=q) | Q(institucion__icontains=q) | Q(palabras_clave__icontains=q))
        data = bebederos.objects.filter(multiple_q)
        if data.count() == 0:
            mensaje = 'No se encontraron bebederos.'
        else:
            mensaje = 'Mostrando ' + str(data.count()) + ' bebederos.'
        for coordenada in data:
            datos = (coordenada.latitud, coordenada.longitud)
            folium.Marker(datos,
                          tooltip=coordenada.nombre,
                          popup='<h6>'+coordenada.nombre+'</h6>\n'+'<h5>Ubicación: '+coordenada.ubicacion+'</h5>',
                          icon=folium.Icon(icon='glyphicon glyphicon-tint')).add_to(m)
    else:
        mensaje = 'Mostrando todos los bebederos disponibles en CU.'
        for coordenada in datosBebederos:
            datos = (coordenada.latitud, coordenada.longitud)
            folium.Marker(datos,
                          tooltip=coordenada.nombre,
                          popup='<h6>'+coordenada.nombre+'</h6>\n'+'<h5>Ubicación: '+coordenada.ubicacion+'</h5>',
                          icon=folium.Icon(icon='glyphicon glyphicon-tint')).add_to(m)

    f = folium.Figure(height=500)
    f.add_child(m)
    contexto = {'map': m._repr_html_(),
                'feedback_resultados': mensaje}

    return render(request, "index.html", contexto)
