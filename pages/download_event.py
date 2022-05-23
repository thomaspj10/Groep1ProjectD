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
            attribution_control=False,
            zoom_control=False,
            search_control=False,
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
    img.save("./media/images/temp_map_img.png", format="PNG")
    
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
    # pdf.line_width
    pdf.rotate(270)
   
    # Adding custom fonts
    pdf.add_font("Montserrat", "", r"./media/fonts/Montserrat-Regular.ttf", uni=True)
    pdf.add_font("Montserrat", "B", r"./media/fonts/Montserrat-Bold.ttf", uni=True)
    pdf.add_font("Montserrat", "I", r"./media/fonts/Montserrat-Italic.ttf", uni=True)
    pdf.add_font("Montserrat", "BI", r"./media/fonts/Montserrat-BoldItalic.ttf", uni=True)
   
    # PDF dimensions
    # pixel : milimeter
    #   1   : 0.264583
    PDF_WIDTH_IN_MM = 297
    PDF_HEIGHT_IN_MM = 210
    
    # Text box
    text_box_x_margin = 35
    text_box_width = PDF_WIDTH_IN_MM - text_box_x_margin * 2
    pdf.image('./media/images/text_box_background.png', x=35, y=-177.5, w=text_box_width, h=40, type='', link='')
    
    # Logos
    pdf.image('./media/images/alten_logo.png', x=12.5, y=-180, w=15, h=15*1.68, type='', link='')
    pdf.image('./media/images/chengeta_wildlife_logo.jpg', x=12.5, y=-150, w=15, h=15, type='', link='')

    col_1_x = 42.5
    col_1_y = -155
    
    # Header text
    pdf.set_font('Montserrat', 'B', 20)
    pdf.set_text_color(160, 68, 44)
    pdf.text(col_1_x, y=col_1_y-10, txt=f"Information about Event #{event_id}")

    # Collumn 1 text
    pdf.set_font('Montserrat', "", 12)
    pdf.set_text_color(255, 255, 255)
    pdf.text(col_1_x, y=col_1_y, txt=f"Node ID: {node_id}")
    pdf.text(col_1_x, y=col_1_y+5, txt=f"Type: {sound_type}")
    pdf.text(col_1_x, y=col_1_y+10, txt=f"Probability: {probability}%")

    # Collumn 2 text
    col_2_x = 100
    col_2_y = col_1_x
    pdf.text(x=col_2_x, y=col_2_y, txt=f"Time: {time}")
    pdf.text(x=col_2_x, y=col_2_y+5, txt=f"Latitude: {latitude}")
    pdf.text(x=col_2_x, y=col_2_y+10, txt=f"Longitude: {longitude}")
    
    
    # Map and background image
    img_width = PDF_WIDTH_IN_MM
    
    # Map-Background
    img_width_height_ratio = 2.0237037037
    img_height = img_width / img_width_height_ratio + 5
    pdf.image('./media/images/text_box_background.png', x=0, y=-127, w=img_width, h=img_height, type = '', link = '')
    
    # Map
    img_width -= 20
    img_height = img_width / img_width_height_ratio
    pdf.image("./media/images/temp_map_img.png", x=0+10, y=-127+5, w=img_width, h=img_height)
    
    pdf_bytes = pdf.output(dest='S').encode('latin-1')
    
    # Create the download button.
    st.download_button(
        label="Download the summary", 
        data=pdf_bytes, 
        file_name="summary.pdf", 
        on_click=on_download
    )