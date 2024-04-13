
 #### 라즈베리파이와 컴퓨터 데스크탑 사이에 양방향 통신 소켓으로 구현

echo기능을 통하여 일단, 클라이언트에서 입력한 텍스트를 터미널에서 출력하도록 성공
![스크린샷 2024-04-11 225122](https://github.com/ayeonggg/illegal-vehicle-detection-system/assets/101121988/e15bd3bd-a74b-48e2-b844-eb0c3cdba2c3)

VSC터미널 바로 왼쪽 옆에 뜨 주소의 웹페이지에 텍스트가 뜨는줄 알았는데 그게 아니래 Port오른쪽에 커서를 갖다대면 나오는 htttps://localhost같은 주소의 웹페이지에 텍스트가 뜨는줄 알았는데 그게 아니래.

직면했던 오류
1.
![스크린샷 2024-04-11 225148](https://github.com/ayeonggg/illegal-vehicle-detection-system/assets/101121988/17767af2-3876-4ce7-a68f-e960bd2adcb7)

2. aws에서 포트 열어둔게 ssh로 접근하는 22밖에 없어서 인바운드 규칙으로 8888포트를 추가해줌. 그래야 된대. 똑같은 코드를 22포트로 하면 안됨.
![스크린샷 2024-04-11 225210](https://github.com/ayeonggg/illegal-vehicle-detection-system/assets/101121988/6fcddf4d-529a-43bc-878f-7f577a3cf81f)
