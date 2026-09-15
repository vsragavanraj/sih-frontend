"""
Image Processing Utility Service for Package Label Compliance Scanner

Integrates OpenCV, NumPy, and Pillow (PIL) for image manipulation,
ROI bounding box cropping, OCR preprocessing, visual annotation, and color overlays.
"""

import os
import cv2
import numpy as np
from PIL import Image, ImageDraw
from typing import List, Dict, Any, Union
from pathlib import Path
from config import RESULTS_DIR

# Color palette for field bounding boxes (BGR format for OpenCV)
CLASS_COLORS = {
    "Brand Name": (255, 140, 0),        # Deep Blue / Cyan
    "MRP": (0, 165, 255),               # Bright Orange
    "Net Quantity": (50, 205, 50),       # Lime Green
    "Manufacturing Date": (255, 191, 0), # Deep Sky Blue
    "Expiry Date": (0, 0, 255),         # Red / Warning
    "Manufacturer Name": (147, 112, 219) # Purple
}

DEFAULT_COLOR = (0, 255, 255) # Yellow

class ImageProcessingService:
    @staticmethod
    def load_image_cv2(image_input: Union[str, np.ndarray]) -> np.ndarray:
        """
        Loads image input into an OpenCV BGR NumPy array.
        """
        if isinstance(image_input, np.ndarray):
            return image_input
        if not os.path.exists(image_input):
            raise FileNotFoundError(f"Image not found at {image_input}")
        img = cv2.imread(image_input)
        if img is None:
            raise ValueError(f"Failed to decode image at {image_input}")
        return img

    @staticmethod
    def crop_roi(image_input: Union[str, np.ndarray], bbox: List[int]) -> np.ndarray:
        """
        Crops Region of Interest (ROI) from an image based on bounding box [x1, y1, x2, y2].

        Args:
            image_input: File path string or OpenCV BGR image array
            bbox: [x1, y1, x2, y2] bounding box coordinates

        Returns:
            np.ndarray: Cropped ROI NumPy image array
        """
        img = ImageProcessingService.load_image_cv2(image_input)
        if img.size == 0 or len(bbox) != 4:
            return np.array([])

        h, w = img.shape[:2]
        x1, y1, x2, y2 = bbox

        # Clamp coordinates to image boundaries
        x1 = max(0, min(x1, w - 1))
        y1 = max(0, min(y1, h - 1))
        x2 = max(x1 + 1, min(x2, w))
        y2 = max(y1 + 1, min(y2, h))

        cropped = img[y1:y2, x1:x2]
        return cropped

    @staticmethod
    def preprocess_roi_for_ocr(roi_img: np.ndarray) -> np.ndarray:
        """
        Applies grayscale conversion and contrast enhancement to cropped ROI to boost OCR accuracy.
        """
        if roi_img.size == 0:
            return roi_img

        # Convert to Grayscale if 3 channels
        if len(roi_img.shape) == 3 and roi_img.shape[2] == 3:
            gray = cv2.cvtColor(roi_img, cv2.COLOR_BGR2GRAY)
        else:
            gray = roi_img.copy()

        # Resize ROI if very small to assist OCR reader
        h, w = gray.shape[:2]
        if h < 40 or w < 40:
            scale = max(2.0, 60.0 / max(h, 1))
            gray = cv2.resize(gray, (0, 0), fx=scale, fy=scale, interpolation=cv2.INTER_CUBIC)

        # Contrast Stretching / Histogram Equalization using CLAHE
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        enhanced = clahe.apply(gray)

        return enhanced

    @staticmethod
    def draw_bounding_boxes(
        image_path: str,
        detections: List[Dict[str, Any]],
        output_filename: str
    ) -> str:
        """
        Draws annotated bounding boxes and labels on detected package label fields.
        """
        img = cv2.imread(image_path)
        if img is None:
            pil_img = Image.open(image_path).convert("RGB")
            draw = ImageDraw.Draw(pil_img)
            for det in detections:
                box = det["bbox"]
                label = f"{det['class']} ({int(det['confidence']*100)}%)"
                draw.rectangle(box, outline="red", width=3)
                draw.text((box[0], max(0, box[1] - 15)), label, fill="red")
            save_path = RESULTS_DIR / output_filename
            pil_img.save(save_path)
            return str(save_path)

        for det in detections:
            bbox = det["bbox"]
            if len(bbox) == 4:
                x1, y1, x2, y2 = bbox
                class_name = det["class"]
                confidence = det["confidence"]
                color = CLASS_COLORS.get(class_name, DEFAULT_COLOR)

                cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)
                label_str = f"{class_name}: {int(confidence * 100)}%"
                (text_w, text_h), baseline = cv2.getTextSize(label_str, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)

                label_y1 = max(y1 - text_h - 8, 0)
                label_y2 = max(y1, text_h + 8)

                cv2.rectangle(img, (x1, label_y1), (x1 + text_w + 6, label_y2), color, -1)
                cv2.putText(
                    img,
                    label_str,
                    (x1 + 3, label_y2 - 4),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5,
                    (255, 255, 255),
                    1,
                    cv2.LINE_AA
                )

        output_path = RESULTS_DIR / output_filename
        cv2.imwrite(str(output_path), img)
        return str(output_path)

# Global Instance
image_processor = ImageProcessingService()
