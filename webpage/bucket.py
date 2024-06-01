import boto3
import os
import openpyxl as op

def s3_connection():
    try:
        # s3 클라이언트 생성
        s3 = boto3.client(
            service_name="s3",
            region_name="ap-northeast-2",
            aws_access_key_id="AKIA4NW3G43R5VOHSKPU",
            aws_secret_access_key="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"
        )
    except Exception as e:
        print(e)
    else:
        print("s3 bucket connected!")
        return s3

s3 = s3_connection()

def car_image_upload():
    car_path = []
    car_name = []
    plate_path = []
    plate_name = []

    try:
        # 엑셀 파일 읽기 시도
        print("엑셀 파일 읽기 시작...")
        wb = op.load_workbook(r"C:\\Users\\USER\\Desktop\\data.xlsx")
        ws = wb.active
        print("엑셀 파일 읽기 완료.")

        # 엑셀 파일의 각 행 순회 - 텍스트가 존재하는 행까지만 읽기
        for row in ws.iter_rows(min_row=1, values_only=True):
            car_image_path = row[0]  # A열
            plate_image_path = row[1]  # B열
            name = row[3]  # D열

            print(f"Read row: {row}")

            if not car_image_path or not plate_image_path:
                print("Empty row encountered, skipping row.")
                continue  # 텍스트가 존재하지 않는 행을 만나면 반복 종료

            if car_image_path and plate_image_path:
                # 경로를 정규화하여 이중 백슬래시 처리
                car_image_path = os.path.normpath(car_image_path)
                plate_image_path = os.path.normpath(plate_image_path)
                # 파일 경로와 이름 추가
                car_path.append(car_image_path)
                car_name.append(name + ".webp")
                plate_path.append(plate_image_path)
                plate_name.append(name + "plate.webp")

                # 각 경로가 제대로 추가되었는지 출력
                print(f"Car image path: {car_image_path}")
                print(f"Plate image path: {plate_image_path}")
                print(f"key is {name}")

        # 파일 업로드 시도
        for i in range(len(car_path)):
            try:
                print(f"Uploading car file: {car_path[i]} as {car_name[i]}")
                if os.path.exists(car_path[i]):
                    s3.upload_file(car_path[i], "detectpath", car_name[i])
                    print(f"Car file {car_name[i]} uploaded successfully to S3 bucket.")
                else:
                    print(f"Car file {car_path[i]} does not exist.")

                print(f"Uploading plate file: {plate_path[i]} as {plate_name[i]}")
                if os.path.exists(plate_path[i]):
                    s3.upload_file(plate_path[i], "detectpath", plate_name[i])
                    print(f"Plate file {plate_name[i]} uploaded successfully to S3 bucket.")
                else:
                    print(f"Plate file {plate_path[i]} does not exist.")

            except Exception as e:
                print(f"Error uploading file to S3: {e}")

    except Exception as e:
        print(f"Error processing Excel file: {e}")

car_image_upload()