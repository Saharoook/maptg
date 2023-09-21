# -*- coding: utf-8 -*-
import json
from django.shortcuts import render, redirect, reverse
from bot.models import Point, PlacePhoto
from folium.plugins import Fullscreen
import folium


def popup_generate():
    pass


def description_generate():
    pass


def icon_generate():
    pass


def custom_map(request):

    if request.method == 'GET':
        f = folium.Figure(width='100%', height=3000)
        cmap = folium.Map(location=[59.936520, 30.319714], zoom_start=14).add_to(f)
        Fullscreen(force_separate_button=True).add_to(cmap)

        points = Point.objects.all()

        styles = """
                    <style>
                        hr {
                            color: black;
                            background-color: black;
                            height: 3px;
                        }
                        img {
                            height: 80px;
                            object-fit: fill;
                            margin: 2px;
                            margin-top: 5px;
                        }
                        a {
                            font-size: 14px;
                        }
                    </style>
                    
                 """

        for i in range(len(points)):
            photos = PlacePhoto.objects.filter(point=points[i])
            photos_front = ""
            for photo in photos:
                photos_front += f'<img src={photo.image.url}>\n'
            popup = f"""
                    {styles}
                    <div style="width: 450px; height: 322px;">
                        <h4 style="text-align: center; overflow: auto; height: 100px"> {points[i].description}</h4>
                        <hr>
                        <div style="overflow-x: scroll; display: flex; height: 110px">
                            {photos_front}
                        </div>
                        <hr>
                        <div style="text-align: center; height: 40px">
                            <a style="margin-right: 30px">ЯНДЕКС КАРТЫ</a>
                            <a>2GIS</a>
                            <a style="margin-left: 30px">GOOGLE MAPS</a>
                        </div>
                    """

            tooltip = f"""<h6>{points[i].name}</h6>"""

            folium.Marker(
                location=[points[i].latitude, points[i].longitude],
                popup=popup,
                tooltip=tooltip,
                icon=folium.Icon(color='green')).add_to(cmap)

        mapJsVar = cmap.get_name()

        cmap.get_root().html.add_child(folium.Element("""
        <script type="text/javascript">
        
         window.addEventListener('load', () => {
             navigator.geolocation.getCurrentPosition(function (position) {
             const lat = position.coords.latitude;
             const lon = position.coords.longitude;
             const pos = L.latLng(lat, lon);
             const marker = new L.marker(pos, {draggable: false, }).addTo({map});
             });
         }); 
        
        </script>
        """.replace("{map}", mapJsVar)))

        context = {'map': cmap._repr_html_()}
        return render(request, 'webinterface/maps.html', context)

