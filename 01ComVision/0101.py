import cv2 as cv # OpenCV 라이브러리 임포트
import numpy as np # 영상 결합(hstack)을 위해 numpy 임포트
import sys # 프로그램 종료 기능을 위해 임포트

# 1. 이미지 로드
img_color = cv.imread('girl_laughing.jpg')

# 이미지를 불러오지 못했을 경우 프로그램 종료
if img_color is None:
    sys.exit('그림 없음')

# 2. 화면에 잘 보이도록 이미지 크기 조절 (Resize)
img_color_resized = cv.resize(img_color, dsize=(0, 0), fx=0.5, fy=0.5)

# 3. 크기가 조절된 이미지를 그레이스케일(흑백)로 변환
img_gray = cv.cvtColor(img_color_resized, cv.COLOR_BGR2GRAY)

# 4. 중요: 흑백 이미지(1채널)를 컬러와 합치기 위해 3채널로 변환
# hstack을 쓰려면 이미지의 높이와 채널 수가 같아야함
img_gray_3ch = cv.cvtColor(img_gray, cv.COLOR_GRAY2BGR)

# 5. numpy의 hstack 함수를 사용하여 가로로 연결
# [컬러 이미지, 3채널 흑백 이미지] 순서로 배열에 담아 합침
combined = np.hstack((img_color_resized, img_gray_3ch))

# 6. 결과 화면 출력
cv.imshow('Color and Gray (Resized)', combined)

# 아무 키나 누를 때까지 대기 후 창 닫기
cv.waitKey(0)
cv.destroyAllWindows()