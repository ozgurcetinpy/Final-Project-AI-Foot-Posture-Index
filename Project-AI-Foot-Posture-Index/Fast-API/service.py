from starlette.responses import JSONResponse
from ultralytics import YOLO
import json
import numpy as np

class Service():
    def __init__(self):
        self.model_yolov8x_2 = None
        self.model_yolov8x_3 = None
        self.model_yolov8x_4 = None
        self.model_yolov8x_5 = None
        self.model_yolov8x_6 = None
        self.model_yolov8x_heel = None
    
    def load_model_2(self):
        self.model_yolov8x_2 = YOLO(r"C:\Users\ozgur\Bitirme\models\weights_2_63.pt")
        
    def load_model_3(self):
        self.model_yolov8x_3 = YOLO(r"C:\Users\ozgur\Bitirme\models\weights_2_63.pt")
        
    def load_model_4(self):
        self.model_yolov8x_4 = YOLO(r"C:\Users\ozgur\Bitirme\models\weights_2_629.pt")
    
    def load_model_5(self):
        self.model_yolov8x_5 = YOLO(r"C:\Users\ozgur\Bitirme\models\weights_5_908.pt")
    
    def load_model_6(self):
        self.model_yolov8x_6 = YOLO(r"C:\Users\ozgur\Bitirme\models\weights_2_63.pt")
        self.model_yolov8x_seg = YOLO(r"C:\Users\ozgur\Bitirme\models\weights_seg.pt")
         
        
        
    async def predict_ic(self,image):
        
        if self.model_yolov8x_5 is None:
            self.load_model_5()
            
        results = self.model_yolov8x_5(image)
        result = results[0]
        class_name = str(int(result.boxes.cls[0])) 
        if class_name == '4':
            class_name = '-2'
        elif class_name == '3':
            class_name = '-1'   
        conf = str(round(float(result.boxes.conf[0]),2))
        
        if float(conf) >= 0.5:
            foot_number = class_name
        else:
            foot_number = "Unknown"
        
        result_ic = {"5":str(foot_number),"Conf":str(conf)}
        print(result_ic["5"])
        return JSONResponse(content=json.dumps(result_ic))
    
    
    async def predict_arka(self,image):
        
        if self.model_yolov8x_2 is None:
            self.load_model_2()
        if self.model_yolov8x_3 is None:
            self.load_model_3()
        if self.model_yolov8x_4 is None:
            self.load_model_4()
        if self.model_yolov8x_6 is None:
            self.load_model_6()
            
        results_2 = self.model_yolov8x_2(image)
        results_3 = self.model_yolov8x_3(image)
        results_4 = self.model_yolov8x_4(image)
        results_6 = self.model_yolov8x_6(image)
        results_seg = self.model_yolov8x_seg(image)
        result_2 = results_2[0]
        result_3 = results_3[0]
        result_4 = results_4[0]
        result_6 = results_6[0]
        result_seg = results_seg[0]
        cls2 = str(int(result_2.boxes.cls[0]))
        cls3 = str(int(result_3.boxes.cls[0]))
        cls4 = str(int(result_4.boxes.cls[0]))
        cls6 = str(int(result_6.boxes.cls[0]))
        conf2 = str(round(float(result_2.boxes.conf[0]),2))
        conf3 = str(round(float(result_3.boxes.conf[0]),2))
        conf4 = str(round(float(result_4.boxes.conf[0]),2))
        conf6 = str(round(float(result_6.boxes.conf[0]),2))
        masks = result_seg.masks.xy
        mask = masks[0]
        
        
        # Model 2
        if float(conf2) >= 0.4:
            if cls2 == '2':
                foot_number_2 = '2'
            elif cls2 == '4':
                foot_number_2 = '-2'
            elif cls2 == '1':
                foot_number_2 = '1'
            elif cls2 == '0':
                foot_number_2 = '0'
            elif cls2 == '3':
                foot_number_2 = '-1'
        else:
            foot_number2 = "Unknown"
        
        # Model 3
        if float(conf3) >= 0.4:
            if cls3 == '2':
                foot_number_3 = '2'
            elif cls3 == '4':
                foot_number_3 = '-2'
            elif cls3 == '1':
                foot_number_3 = '1'
            elif cls3 == '0':
                foot_number_3 = '0'
            elif cls3 == '3':
                foot_number_3 = '-1'
        else:
            foot_number_3 = "Unknown"
        
        # Model 4
        if float(conf4) >= 0.4:
            if cls4 == '2':
                foot_number_4 = '2'
            elif cls4 == '4':
                foot_number_4 = '-2'
            elif cls4 == '1':
                foot_number_4 = '1'
            elif cls4 == '0':
                foot_number_4 = '0'
            elif cls4 == '3':
                foot_number_4 = '-1'
        else:
            foot_number_4 = "Unknown"
        
        # Model 6
        poly = np.array(mask, np.int32)
        poly = poly.reshape((-1, 1, 2))
        
        points = poly.squeeze()
        highest_points = points[points[:, 1] == np.min(points[:, 1])]
        center_point = np.mean(highest_points, axis=0).astype(int)
        bottom_mask = mask[mask[:, 1] >= center_point[1]]
        bottom_left_pixels = len(bottom_mask[bottom_mask[:, 0] < center_point[0]])
        bottom_right_pixels = len(bottom_mask[bottom_mask[:, 0] >= center_point[0]])
        diff = bottom_right_pixels-bottom_left_pixels
        
        if cls6 == '2':
            foot_number_6 = '2'
        elif cls6 == '4':
            foot_number_6 = '-2'
        else:
            if diff > 40:
                foot_number_6 = '1'
            elif diff <= 40 and diff >= -40:
                foot_number_6 = '0'
            elif diff < -40:
                foot_number_6 = '-1'

        sum = int(foot_number_2) + int(foot_number_3) + int(foot_number_4) + int(foot_number_6)

        result_arka = {
            "2":foot_number_2,
            "3":foot_number_3,
            "4":foot_number_4,
            "6":foot_number_6,
            "Sum":str(sum),
            "conf2":str(conf2),
            "conf3":str(conf3),
            "conf4":str(conf4),
            "conf6":str(conf6),
        }
        
        return JSONResponse(content=json.dumps(result_arka))