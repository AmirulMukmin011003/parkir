import cv2
import pickle


width, height = 40,80
try:
    with open('file/mobil_pos', 'rb') as f:
        posList = pickle.load(f)
except:
    posList = []

# memberikan id pada tiap slot parkir
counter_id = max([item[0] for item in posList], default=0) + 1

def mouseClick(events, x, y, flags, params):
    global counter_id
    if events == cv2.EVENT_LBUTTONDOWN:
        posList.append((counter_id,x, y))
        counter_id += 1 
    elif events == cv2.EVENT_RBUTTONDOWN:
        for i, (id, x1, y1) in enumerate(posList):
            if x1 < x < x1 + width and y1 < y < y1 + height:
                posList.pop(i)
        

    with open('file/mobil_pos', 'wb') as f:
        pickle.dump(posList, f)

while True:
    img = cv2.imread('file/mobil.jpg')

    for id, x, y in posList:
        # Gambar kotak
        pt1 = (x, y)
        pt2 = (x + width, y + height)
        cv2.rectangle(img, pt1, pt2, (255, 0, 0), 2)
        # Gambar ID di dalam kotak
        cv2.putText(img, str(id), (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1, cv2.LINE_AA)

    cv2.imshow("Image", img)
    cv2.setMouseCallback("Image", mouseClick)
    cv2.waitKey(1)
