
# Impor Library dan Inisialisasi Video Feed
import cv2
import pickle
import cvzone
import numpy as np
import firebase_admin
from firebase_admin import db, credentials


cred = credentials.Certificate('tesmasuk-7230a-firebase-adminsdk-4u2fr-78b9fa4db8.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://tesmasuk-7230a-default-rtdb.asia-southeast1.firebasedatabase.app'
})


#pemetaan ID ke slot firebase
id_to_slot = {
    1: 'slot_1',
    2: 'slot_2',
    3: 'slot_3',
    4: 'slot_4',
    5: 'slot_5',
    6: 'slot_6'
    # 7: 'slot_7',
    # 8: 'slot_8',
    # 9: 'slot_9',
    # 10: 'slot_10',
    # 11: 'slot_11',
    # 12: 'slot_12',
    # 13: 'slot_13',
    # 14: 'slot_14',
    # 15: 'slot_15',
    # 16: 'slot_16',
    # 17: 'slot_17',
    # 18: 'slot_18',
    # 19: 'slot_19',
    # 20: 'slot_20'
}

cap = cv2.VideoCapture(0)

# Muat Posisi Slot Parkir dari File 
with open('file/mobil_pos', 'rb') as f:
    posList = pickle.load(f)

# Definisi dan Implementasi Fungsi checkParkingSpace
width, height = 40, 68

def checkParkingSpace(imgPro):
    spaceCounter = 0
    # parking_status = {}

    for id, x, y in posList:
        imgCrop = imgPro[y:y + height, x:x + width]
        count = cv2.countNonZero(imgCrop)

        if count < 300:
            color = (0, 255, 0)
            thickness = 5
            spaceCounter += 1
            status = False
        else:
            color = (0, 0, 255)
            thickness = 2
            status = True

        # Pemetaan ID ke slot Firebase dan update status
        slot_name = id_to_slot.get(id)
        if slot_name:
            db.reference(f'slot_parking/{slot_name}').set(status)

        # Menampilkan ID dan Total pixcel yang terbaca
        cv2.rectangle(img, (x, y), (x + width, y + height), color, thickness)
        cvzone.putTextRect(img, str(id), (x + 5, y + 15), scale=1, thickness=1, offset=0, colorR=color)
        cvzone.putTextRect(img, str(count), (x + 5, y + height - 10), scale=1, thickness=1, offset=0, colorR=color)

    # Tampilan Terisi/Total Slot Parkir
    cvzone.putTextRect(img, f'Free: {spaceCounter}/{len(posList)}', (100, 50), scale=3,
                       thickness=5, offset=20, colorR=(0, 200, 0))


# ukuran window saat dijalankan
cv2.namedWindow("Image", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Image", 800, 600)

# loop utama
while True:
    if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
    
    success, img = cap.read()
    if not success:
        break
    
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray, (3, 3), 1)
    imgThreshold = cv2.adaptiveThreshold(imgBlur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                         cv2.THRESH_BINARY_INV, 25, 16)
    imgMedian = cv2.medianBlur(imgThreshold, 5)
    kernel = np.ones((3, 3), np.uint8)
    imgDilate = cv2.dilate(imgMedian, kernel, iterations=1)

    checkParkingSpace(imgDilate)
    cv2.imshow("Image", img)
    # cv2.imshow("ImageBlur", imgBlur)
    # cv2.imshow("ImageThres", imgMedian)
    
    if cv2.waitKey(10) & 0xFF == 27:  # Press 'Esc' to exit
        break

# tutup videocapture
cap.release()
cv2.destroyAllWindows()
