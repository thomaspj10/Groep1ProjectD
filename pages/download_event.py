from turtle import width
import streamlit as st
import pandas as pd
import numpy as np
import utils.database as database
import leafmap.foliumap as leafmap
import io
import datetime
from PIL import Image
from fpdf import FPDF

def create_page():
    event_id = st.experimental_get_query_params()["event"][0]
    if not event_id.isnumeric():
        return
    
    conn = database.get_connection()
    
    # Search for the specific event.
    df = pd.read_sql("SELECT * FROM event", conn)    
    df = df[df["event_id"] == int(event_id)] 
    
    if df.size == 0:
        st.write(f"An event with the id '{event_id}' does not exist!")
        return
    
    # Create a map.
    m = leafmap.Map(
            draw_control=False,
            measure_control=False,
            fullscreen_control=False,
            attribution_control=True,
            location=[df.at[0, "latitude"], df.at[0, "longitude"]],
            zoom_start=10)
    m.add_basemap("Stamen.Terrain")
    m.add_circle_markers_from_xy(
        df, x="longitude", y="latitude", radius=10, color="blue", fill_color="black")
    
    def on_download():
        st.experimental_set_query_params(
            event=None
        )
    
    # Convert the map to png. 
    # NOTE: This requires geckodriver which can be installed by using the following command:
    # conda install -c conda-forge geckodriver
    img_data = m._to_png(2)
    img = Image.open(io.BytesIO(img_data))
    img.save("./images/temp_map_img.png", format="PNG")
    
    # Get some general information.
    event = df.head(1)
    
    node_id = int(event["node_id"])
    time = datetime.datetime.utcfromtimestamp(float(event["time"])).strftime("%Y/%m/%d %H:%M")
    sound_type = event["sound_type"][0]
    probability = int(event["probability"])
    latitude = float(event["latitude"])
    longitude = float(event["longitude"])
        
    # Create the pdf
    pdf = FPDF()
    pdf.add_page()
    pdf.rotate(270)
    
    img = Image.new('RGB', (297,297), "#242424" )
    img.save('./images/text_box_background.png')

    pdf.image('./images/text_box_background.png', x = 35, y = -185, w = 140, h = 40, type = '', link = '')
    pdf.image('./images/alten_logo.png', x = 12.5, y = -180, w = 15, h = 15*1.68, type = '', link = '')
    pdf.image('./images/chengeta_wildlife_logo.jpg', x = 12.5, y = -150, w = 15, h = 15, type = '', link = '')
    
    pdf.set_font('Arial', 'B', 20)
    pdf.set_text_color(160, 68, 44)
    pdf.text(x=40, y=-175, txt=f"Information about Event #{event_id}")
    pdf.set_font('Arial', "", 12)
    pdf.set_text_color(255, 255, 255)
    pdf.text(x=40, y=-165, txt=f"Node ID: {node_id}")
    pdf.text(x=40, y=-160, txt=f"Time: {time}")
    pdf.text(x=40, y=-155, txt=f"Type: {sound_type}")
    pdf.text(x=40, y=-150, txt=f"Probability: {probability}%")

    pdf.text(x=100, y=-165, txt=f"Latitude: {latitude}")
    pdf.text(x=100, y=-160, txt=f"Longitude: {longitude}")
    
    img_width = 297
    img_height_width_ratio = 2.0237037037
    img_height = img_width / img_height_width_ratio
    pdf.image("./images/temp_map_img.png", x=0, y=-127, w=img_width, h=img_height)
    
    
    pdf_bytes = pdf.output(dest='S').encode('latin-1')
    
    # Create the download button.
    st.download_button(
        label="Download the summary", 
        data=pdf_bytes, 
        file_name="summary.pdf", 
        on_click=on_download
    )