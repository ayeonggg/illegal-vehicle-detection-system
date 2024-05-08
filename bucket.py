import boto3

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

try:
    s3.upload_file(r"C:\Users\USER\Desktop\수강과목\캡스톤\street-7583585_640.jpg","detectpath","street.jpg")
except Exception as e:
    print(e)