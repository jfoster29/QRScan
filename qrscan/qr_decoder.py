"""
qr_decoder.py

Detects and decodes QR codes from images using OpenCV.
"""

from typing import List, Dict, Any
import numpy as np
import cv2


def extract_qr_codes(images: List[np.ndarray]) -> List[Dict[str, Any]]:
    """
    Detect and decode QR codes from a list of images using OpenCV.

    Args:
        images: List of page images as NumPy arrays.

    Returns:
        List of dictionaries with 'page', 'qr_text', and 'bbox' (bounding box).
    """
    results = []
    qr_detector = cv2.QRCodeDetector()
    
    for idx, img in enumerate(images):
        # Convert to grayscale for better QR detection
        if len(img.shape) == 3:
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        else:
            gray = img
            
        # Detect and decode QR code
        data, bbox, _ = qr_detector.detectAndDecode(gray)
        
        if data and bbox is not None:
            # Convert bbox to the expected format
            bbox = bbox.astype(int)
            x_coords = bbox[:, 0]
            y_coords = bbox[:, 1]
            
            results.append({
                "page": idx + 1,
                "qr_text": data,
                "bbox": {
                    "x": int(np.min(x_coords)),
                    "y": int(np.min(y_coords)),
                    "width": int(np.max(x_coords) - np.min(x_coords)),
                    "height": int(np.max(y_coords) - np.min(y_coords))
                }
            })
    
    return results 