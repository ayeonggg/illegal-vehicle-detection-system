import boto3
import csv
import os

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

def carImage_up:
    file_path[] =" "
    i=0
    while Null:
        i=i+1
        file_path[i]= {여기에 엑셀파일에서 불러온 carImage경로}
    file_name1 = os.path.basename(file_path1)  # 파일 경로에서 파일 이름만 추출
    name1 = file_name1[-24:-5] 
    return name
file_path2 = "C:\\Users\\USER\\Desktop\\2024-05-13-11111.jpeg"
file_name2 = os.path.basename(file_path2)  # 파일 경로에서 파일 이름만 추출
name2 = file_name2[-24:-5]

try:
    s3.upload_file(file_path1, "detectpath", name1+".jpg")
    print("File1 uploaded successfully to S3 bucket.")
    s3.upload_file(file_path2, "detectpath", name2+"plate.jpg")
    print("File2 uploaded successfully to S3 bucket.")
except Exception as e:
    print(f"Error uploading file to S3: {e}")

