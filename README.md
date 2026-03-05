# ComVision 01주차 실습
# OpenCV 실습 과제

## 0101. 이미지 불러오기 및 그레이스케일 변환
- **설명**: 이미지를 불러오고 흑백으로 변환 후 나란히 출력
- **요구사항**:
  - cv.imread()              :이미지 로드
  - cv.cvtColor()            :이미지를 그레이스케일로 변환
  - np.hstack()              :원본 이미지와 그레이스케일 이미지를 가로로 연결하여 출력
  - cv.imshow(), cv.waitKey():결과를 화면에표시, 아무 키나 누르면 창이 닫히도록
- **코드**
  ```python
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
  ```
- **주요코드**
  ```python
  ```
- **결과물**:
<img width="2845" height="1675" alt="image" src="https://github.com/user-attachments/assets/52f65b68-9aee-4d6a-98fc-d148ec49061e" />



## 0102. 페인팅 붓 크기 조절
- **설명**: 마우스 클릭으로 그림을 그리고, `+`, `-` 키로 붓 크기를 1~15까지(초기 5) 조절
- **요구사항**:
  - 좌클릭(B)
  - 우클릭(R)
  - 드래그로 연속 그리기
  - 창 종료(q)
- **코드**
  ```python
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
  ```
- **주요코드**
  ```python
  ```
- **결과물**: 
<img width="2835" height="1799" alt="image" src="https://github.com/user-attachments/assets/88470528-8b0f-4e0d-b065-94e54aa3b6f1" />
<img width="1015" height="388" alt="image" src="https://github.com/user-attachments/assets/74258ccc-b7f6-4b61-bf13-6fba43118472" />


## 0103. ROI(관심영역) 추출
- **설명**: 마우스 드래그로 영역을 선택하고 영역만 저장 혹은 표시
- **요구사항**:
  - cv.setMouseCallback()을사용하여마우스이벤트를처리
  - 사용자가클릭한시작점에서드래그하여사각형을그리며영역을선택
  - 마우스를놓으면해당영역을잘라내서별도의창에출력
  - r :선택을리셋하고처음부터다시선택
  - s :선택한영역을이미지파일로저장
- **코드**
  ```python
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
  img = cv.imread('girl_laughing.jpg')
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
  ```
- **주요코드**
  ```python
  ```
- **결과물**:
<img width="2807" height="1651" alt="image" src="https://github.com/user-attachments/assets/464e49c5-f099-4f86-aa9b-882522d9c916" />
<img width="1805" height="1474" alt="image" src="https://github.com/user-attachments/assets/269e71c5-7c22-4fef-bc4a-26165a52e88b" />



