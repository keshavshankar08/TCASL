import cv2 as cv
import numpy as np
import time
from collections import deque
from typing import Tuple, Optional
from tcasl import TCASL

class GameEngine:
    def __init__(self) -> None:
        """Initializes the engine, downloading the model if necessary."""
        self.tcasl = TCASL()
        self.camera: Optional[cv.VideoCapture] = None
        self.pred_buffer: deque = deque(maxlen=30)
        self.last_pred_time: float = 0.0
        self.pred_interval: float = 1.0 / 30.0
        self.prev_frame: Optional[np.ndarray] = None

    def start_camera(self, device_id: int = 0) -> bool:
        """
        Initiali zes the video capture device.
        
        :param device_id: The index of the camera.
        :return: True if successful, False otherwise.
        """
        self.camera = cv.VideoCapture(device_id)
        self.prev_frame = None
        return self.camera.isOpened()

    def stop_camera(self) -> None:
        """Releases the video capture device."""
        if self.camera:
            self.camera.release()
            self.camera = None

    def process_frame(self) -> Tuple[Optional[np.ndarray], Optional[np.ndarray], str]:
        """
        Reads a frame, computes temporal contrast, and generates a prediction.
        
        :return: A tuple containing the original resized frame, the temporal contrast frame, and the predicted character.
        """
        if not self.camera or not self.camera.isOpened():
            return None, None, "-"

        ret, frame = self.camera.read()
        if not ret:
            return None, None, "-"

        frame = cv.flip(frame, 1)
        frame_gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        current_frame = self.tcasl.preprocess_frame(frame_gray)

        if self.prev_frame is None:
            self.prev_frame = current_frame

        tc_frame = self.tcasl.compute_temporal_contrast(self.prev_frame, current_frame)
        self.prev_frame = current_frame

        current_time = time.time()
        if current_time - self.last_pred_time >= self.pred_interval:
            self.last_pred_time = current_time
            raw_pred = self.tcasl.predict(tc_frame, top_k=1)
            if raw_pred:
                self.pred_buffer.append(raw_pred[0])

        prediction = self._get_majority_vote()
        return current_frame, tc_frame, prediction

    def _get_majority_vote(self) -> str:
        """
        Calculates the most frequent prediction in the buffer.
        
        :return: The most common predicted character string.
        """
        if not self.pred_buffer:
            return "-"
        labels_only = [item[0] for item in self.pred_buffer]
        return max(set(labels_only), key=labels_only.count)
    
    def get_target_confidence(self, target_char: str) -> float:
        """
        Calculates average confidence of the target character in the buffer.

        :param target_char: Target prediction character.

        :return: The confidence of the target prediction character.
        """
        if not self.pred_buffer:
            return 0.0
        target_confs = [item[1] for item in self.pred_buffer if item[0] == target_char]
        
        if not target_confs:
            return 0.0
            
        return sum(target_confs) / len(target_confs)

    def clear_buffer(self) -> None:
        """Empties the prediction buffer to reset state between words."""
        self.pred_buffer.clear()