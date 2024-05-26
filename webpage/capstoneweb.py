import openpyxl as op
from flask import Flask, render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    try:
        wb = op.load_workbook(r"C:\\Users\\USER\\Desktop\\data.xlsx")
        ws = wb.active

        car_images = [] 
        plate_texts = [] 
        plate_images = []
        latitude_degs = []
        longitude_degs = []
        capture_times = []

        for row in ws.iter_rows(min_row=0, values_only=True):
            plate_text = row[1]
            latitude_deg = row[3]
            longitude_deg = row[4]
            capture_time = row[5]

            car_images.append(f"https://detectpath.s3.ap-northeast-2.amazonaws.com/{capture_time}.webp")
            plate_images.append(f"https://detectpath.s3.ap-northeast-2.amazonaws.com/{capture_time}plate.webp")
            plate_texts.append(plate_text)
            latitude_degs.append(latitude_deg)
            longitude_degs.append(longitude_deg)
            capture_times.append(capture_time)

        return render_template(
            'index.html',
            car_images=car_images,
            plate_texts=plate_texts,
            plate_images=plate_images,
            latitude_degs=latitude_degs,
            longitude_degs=longitude_degs,
            capture_times=capture_times
        )
    except Exception as e:
        return str(e)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8080)


