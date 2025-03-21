import openpyxl as op
from flask import Flask, render_template
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    try:
        wb = op.load_workbook(r"C:/Users/USER/Desktop/detect_result.xlsx")
        ws = wb.active

        car_images = [] 
        plate_texts = [] 
        plate_images = []
        latitude_degs = []
        longitude_degs = []
        capture_times = []

        for row in ws.iter_rows(min_row=2, values_only=True):  # 첫 번째 행은 헤더로 가정
            plate_text = row[2]
            latitude_deg = row[4]
            longitude_deg = row[5]
            capture_time = row[3]
            if plate_text is None or latitude_deg is None or longitude_deg is None or capture_time is None:
                print("Empty row encountered, skipping row.")
                continue  # 텍스트가 존재하지 않는 행을 만나면 반복 종료
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
