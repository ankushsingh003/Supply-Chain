import cv2
from ultralytics import YOLO

class FreightDetector:
    def __init__(self, model_path='yolo11n.pt'):
        """
        Initialize the YOLOv11 detector.
        Default to the nano model for speed.
        """
        self.model = YOLO(model_path)
        # Interested classes: truck (7), car (2), boat (8), train (6)
        # These are standard COCO classes that represent freight movement.
        self.target_classes = [2, 6, 7, 8] 

    def detect(self, frame):
        """
        Perform detection on a single frame.
        """
        results = self.model.predict(frame, classes=self.target_classes, verbose=False)
        return results[0]

    def draw_detections(self, frame, results):
        """
        Draw bounding boxes and labels on the frame.
        """
        return results.plot()

if __name__ == "__main__":
    # Test with a dummy frame if run directly
    import numpy as np
    detector = FreightDetector()
    dummy_frame = np.zeros((640, 640, 3), dtype=np.uint8)
    res = detector.detect(dummy_frame)
    print("Self-test complete. Objects detected:", len(res.boxes))
