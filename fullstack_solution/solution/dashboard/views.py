from django.shortcuts import render
from django.views.generic import TemplateView
import folium
from folium.plugins import HeatMap
import openpyxl
import requests

# Create your views here.

# View for eventmap / heatmap (Heatmap should be able to get toggled on/off (not implemented yet))

class FoliumView(TemplateView):
    template_name = "dashboard/map.html"

    def get_context_data(self, **kwargs):
        data = [
            [51.83658, 4.67769, 2.78],
            [51.83644, 4.71662, 0.78],
            [51.82701, 4.65555, 0.65],
            [51.9228, 4.3192, 0.65],
            [51.95931, 4.57049, 0.65]
        ]

        figure = folium.Figure()
        m = folium.Map(
            location=[52.147, 6.152],
            zoom_start=8,
            tiles='Stamen Terrain'
        )
        m.add_to(figure)
        figure.render()
        folium.Marker(
            location=[51.917218, 4.4840498],
            popup='School',
            icon=folium.Icon(icon='cloud')
            ).add_to(m)
        m.add_to(figure)

        folium.Marker(
            location=[51.83658, 4.67769],
            popup='Arjans huis',
            icon=folium.Icon(color='green')
        ).add_to(m)
        folium.Marker(
            location=[52.37058, 4.89683],
            popup='Amsterdam is niet mijn favoriete stad',
            icon=folium.Icon(color='red', icon='info-sign')
        ).add_to(m)

        # Toggle option to toggle on/off heatmap? 
        heatmapon = True
        if heatmapon:
            HeatMap(data).add_to(m)

        figure.render()
        return {"map": figure}

def load_excel(request):
    if "GET" == request.method:
        return render(request, 'dashboard/load_excel.html', {})
    else:
        excel_file = request.FILES["excel_file"]

        # you may put validations here to check extension or file size

        wb = openpyxl.load_workbook(excel_file)

        worksheet = wb["NodeData"]
        excel_data = list()
        # iterating over the rows and
        # getting value from each cell in row
        for row in worksheet.iter_rows():
            row_data = list()
            for cell in row:
                row_data.append(str(cell.value))
            excel_data.append(row_data)
        return render(request, 'dashboard/load_excel.html', {"excel_data":excel_data})

def load_api_data(request):
    response = requests.get('https://api.covid19api.com/countries').json()
    return render(request,'dashboard/load_api_data.html',{'response':response})



def graphs(request):
    return render(request, 'dashboard/graphs.html', {})

def index(request):
    return render(request, 'dashboard/index.html', {})

def diagrams(request):
    return render(request, 'dashboard/diagrams.html', {})

def filter_data(request):
    return render(request, 'dashboard/filter_data.html', {})

def load_db(request):
    return render(request, 'dashboard/load_db_data.html', {})