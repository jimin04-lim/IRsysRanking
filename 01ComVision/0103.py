import cv2 as cv # OpenCV 라이브러리 임포트 
import numpy as np
import sys # 프로그램 종료 기능을 위해 임포트

# 전역 변수 설정
is_dragging = False # 마우스 드래그 상태 확인 
x_start, y_start = -1, -1 # 드래그 시작 좌표 
roi_img = None # 잘라낸 이미지 저장 변수

def on_mouse(event, x, y, flags, param):
    global is_dragging, x_start, y_start, img_copy, roi_img # 전역 변수 사용

    if event == cv.EVENT_LBUTTONDOWN: # 왼쪽 버튼 클릭 시 시작 
        is_dragging = True
        x_start, y_start = x, y
        
    elif event == cv.EVENT_MOUSEMOVE: # 마우스 이동 중 
        if is_dragging:
            img_draw = img_copy.copy() # 원본 복사본 위에 사각형 그림
            cv.rectangle(img_draw, (x_start, y_start), (x, y), (0, 255, 0), 2) # 초록색 사각형 시각화
            cv.imshow('ROI Selection', img_draw)
            
    elif event == cv.EVENT_LBUTTONUP: # 마우스 버튼을 떼면 완료 
        is_dragging = False
        # 드래그 방향에 상관없이 좌표 설정 (슬라이싱을 위해)
        x_min, x_max = min(x_start, x), max(x_start, x)
        y_min, y_max = min(y_start, y), max(y_start, y)
        
        if x_max - x_min > 0 and y_max - y_min > 0:
            roi_img = img_copy[y_min:y_max, x_min:x_max] # numpy 슬라이싱으로 ROI 추출 
            cv.imshow('Cropped ROI', roi_img) # 추출된 영역 별도 창 표시

# 이미지 로드 (경로 주의!) 
img = cv.imread("girl_laughing.jpg")
img_copy = img.copy() # 수정을 위한 이미지 복사본

cv.imshow('ROI Selection', img_copy) # 초기 화면 출력 
cv.setMouseCallback('ROI Selection', on_mouse) # 마우스 이벤트 처리 등록 

while True:
    key = cv.waitKey(1) & 0xFF # 키 입력 대기
    
    if key == ord('r'): # 'r' 키: 초기화 
        img_copy = img.copy()
        cv.imshow('ROI Selection', img_copy)
        print("영역 선택 리셋")
        
    elif key == ord('s'): # 's' 키: ROI 저장
        if roi_img is not None:
            cv.imwrite('cropped_result.jpg', roi_img) # 파일로 저장
            print("ROI 이미지가 성공적으로 저장되었습니다.")
            
    elif key == ord('q'): # 'q' 키: 종료
        break

cv.destroyAllWindows()