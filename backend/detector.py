"""
Legacy Detector Module Re-exporting from YoloDetectionService
"""

from services.yolo_service import yolo_service, YoloDetectionService

class YoloDetector:
    def detect_objects(self, image_path: str):
        result = yolo_service.detect_fields(image_path)
        # Adapt format for legacy calls
        legacy_list = []
        for det in result["detections"]:
            legacy_list.append({
                "object_name": det["class"],
                "confidence": det["confidence"],
                "bbox": det["bbox"]
            })
        return legacy_list

detector = YoloDetector()
