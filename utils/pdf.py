import os
import uuid
import pandas as pd
import utils.database as database
import leafmap.foliumap as leafmap
import io
import datetime
from PIL import Image
from fpdf import FPDF

__TEMP_IMG_PATH = "./media/images/temp-maps/"

def get_pdf_bytes(df: pd.DataFrame):
    # Create a map.
    m = leafmap.Map(
            draw_control=False,
            measure_control=False,
            fullscreen_control=False,
            attribution_control=False,
            zoom_control=False,
            search_control=False,
            location=[df.at[0, "latitude"], df.at[0, "longitude"]],
            zoom_start=12.5) # 11.5=3km 12.5=1km
    m.add_basemap("Stamen.Terrain")
    m.add_circle_markers_from_xy(
        df, x="longitude", y="latitude", radius=10, color="blue", fill_color="black")
    
    # Convert the map to png. 
    # NOTE: This requires geckodriver which can be installed by using the following command:
    # conda install -c conda-forge geckodriver
    img_data = m._to_png(2)
    img = Image.open(io.BytesIO(img_data))
    img_uuid = uuid.uuid4()
    img.save(f"{__TEMP_IMG_PATH}{img_uuid}.png", format="PNG")
    
    # Get some general information.
    event = df.head(1)
        
    pdf_bytes = __create_pdf(event, img_uuid)
    
    return pdf_bytes

def __create_pdf(event: pd.DataFrame, map_img_uuid):
    # Splits and converts data
    event_id = int(event["event_id"])
    node_id = int(event["nodeId"])
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
    col_2_y = col_1_y
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
    # pdf.image("./media/images/temp_map_img.png", x=0+10, y=-127+5, w=img_width, h=img_height)
    pdf.image(f"{__TEMP_IMG_PATH}{map_img_uuid}.png", x=0+10, y=-127+5, w=img_width, h=img_height)

    pdf_bytes = pdf.output(dest='S').encode('latin-1')
    
    os.remove(f"{__TEMP_IMG_PATH}{map_img_uuid}.png")  
    
    return pdf_bytes

"""
conn = database.get_connection()
df = pd.read_sql("SELECT * FROM event", conn)
event = df.head(1)

print(get_pdf_bytes(event))
"""