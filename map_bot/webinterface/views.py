# -*- coding: utf-8 -*-
import json
from django.shortcuts import render, redirect, reverse
from bot.models import Point
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

        for i in range(len(points)):
            folium.Marker(
                location=[points[i].latitude, points[i].longitude],
                popup=points[i].description,
                tooltip=points[i].name,
                icon=folium.CustomIcon("icons/geo2.png", icon_size=(35, 30), icon_anchor=(25, 50))).add_to(cmap)

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


# $(document).ready(function () {
#   {map}.on("click", addMarker);
#
#   function addMarker(e) {
#     // ustawiamy aby marker był przesuwalny
#     const marker = new L.marker(e.latlng, {
#       draggable: true,
#     }).addTo({map});
#   }
# });
#


#         window.addEventListener('load', () => {
#             navigator.geolocation.getCurrentPosition(function (position) {
#             const lat = position.coords.latitude;
#             const lon = position.coords.longitude;
#             const pos = L.latLng(lat, lng);
#             const marker = new L.marker(pos, {draggable: false, }).addTo({map});
#             });
#         });

