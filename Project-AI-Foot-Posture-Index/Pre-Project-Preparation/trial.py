
from tensorflow.keras.models import load_model
import cv2
import numpy as np


model = load_model(r'C:\Users\ozgur\Desktop\FinalProject\BitirmeProjesi\model\model_tflite.tflite')

cap = cv2.VideoCapture(0)
while True:
    # Kameradan bir kare alın
    ret, frame = cap.read()

    # Görüntüyü boyutlandırın ve normalize edin

    resized = cv2.resize(frame, (150,150))
    # rgb_image = cv2.cvtColor(resized,cv2.COLOR_RGB2GRAY)
    normalized = resized / 255.0

    # Görüntüyü modele girdi olarak sağlayın
    result = model.predict(np.array([normalized]))
    # En yüksek olasılığa sahip sınıfı bulun
    #predicted_class = np.argmax(result[0])
    # Sınıf etiketlerini yükleyin
    # class_labels = ["arka","yan"]
    # print(predicted_class)
    # Sınıf etiketini yazdırın
    #label = class_labels[predicted_class]
    if result[0][0] <= 0.50: 
        label = "arka"
    else:
        label = "yan"
    cv2.putText(frame, label, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    # Görüntüyü gösterin
    cv2.imshow("Kamera", frame)

    # Çıkış için 'q' tuşuna basın
    if cv2.waitKey(1) == ord('q'):
        break

# Kamerayı serbest bırakın ve pencereyi kapatın
cap.release()
cv2.destroyAllWindows()