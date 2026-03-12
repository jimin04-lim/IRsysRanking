import cv2 as cv # OpenCV 라이브러리 임포트 
import sys # 프로그램 종료 기능을 위해 임포트

# 전역 변수 설정
brush_size = 5 # 초기 붓 크기는 5로 설정 
color = (255, 0, 0) # 초기 색상은 파란색 (BGR 형식) 
is_drawing = False # 마우스 클릭 상태를 저장하는 변수

# 마우스 이벤트 콜백 함수 정의
def draw_circle(event, x, y, flags, param):
    global is_drawing, brush_size, color # 전역 변수 사용 선언
    
    if event == cv.EVENT_LBUTTONDOWN: # 마우스 왼쪽 버튼 클릭 시 
        is_drawing = True # 그리기 모드 활성화
        color = (255, 0, 0) # 파란색으로 변경
        cv.circle(img, (x, y), brush_size, color, -1) # 현재 위치에 원 그리기 
        
    elif event == cv.EVENT_RBUTTONDOWN: # 마우스 오른쪽 버튼 클릭 시 
        is_drawing = True # 그리기 모드 활성화
        color = (0, 0, 255) # 빨간색으로 변경
        cv.circle(img, (x, y), brush_size, color, -1) # 현재 위치에 원 그리기
        
    elif event == cv.EVENT_MOUSEMOVE: # 마우스가 움직일 때 
        if is_drawing: # 버튼이 눌린 상태라면 드래그로 그리기 수행 
            cv.circle(img, (x, y), brush_size, color, -1) # 연속적으로 원 그리기 
            
    elif event == cv.EVENT_LBUTTONUP or event == cv.EVENT_RBUTTONUP: # 버튼을 뗄 때
        is_drawing = False # 그리기 모드 비활성화

# 배경이 될 이미지 로드 (경로 주의!)
img = cv.imread('girl_laughing.jpg') # 이미지 불러오기 
cv.namedWindow('Painting') # 창 이름 설정
cv.setMouseCallback('Painting', draw_circle) # 마우스 콜백 함수 등록 

while True: # 무한 루프 시작 
    cv.imshow('Painting', img) # 화면에 이미지 출력
    key = cv.waitKey(1) & 0xFF # 1ms 동안 키 입력 대기 
    
    if key == ord('+'): # '+' 입력 시 붓 크기 증가 
        brush_size = min(15, brush_size + 1) # 최대 15로 제한 
        print(f"현재 붓 크기: {brush_size}") # 터미널에 크기 출력
        
    elif key == ord('-'): # '-' 입력 시 붓 크기 감소 
        brush_size = max(1, brush_size - 1) # 최소 1로 제한
        print(f"현재 붓 크기: {brush_size}") # 터미널에 크기 출력
        
    elif key == ord('q'): # 'q' 입력 시 종료 
        break # 루프 탈출

cv.destroyAllWindows() # 모든 창 닫기