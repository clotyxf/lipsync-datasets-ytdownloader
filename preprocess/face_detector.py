import cv2
import shutil
import subprocess

import numpy as np
import mediapipe as mp


class FaceDetector:
    def __init__(self):
        self.face_detection = mp.solutions.face_detection.FaceDetection(model_selection=0, min_detection_confidence=0.5)

    def detect_face(self, image: np.ndarray):
        # Process the image and detect faces.
        results = self.face_detection.process(image)

        if not results.detections:  # Face not detected
            return False

        if len(results.detections) != 1:
            return False
        return True

    def get_video_info(self, video_path: str) -> dict:
        info = {}

        try:
            cap = cv2.VideoCapture(video_path)

            if not cap.isOpened():
                cap.release()
                return info
        except:
            return info

        info["fps"] = cap.get(cv2.CAP_PROP_FPS)
        info["frame_count"] = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        info["width"] = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        info["height"] = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        cap.release()
        return info

    def get_video_frames(self, video_path: str):
        # Open the video file
        cap = cv2.VideoCapture(video_path)

        # Check if the video was opened successfully
        if not cap.isOpened():
            print("Error: Could not open video.")
            return np.array([])

        frames = []

        while True:
            # Read a frame
            ret, frame = cap.read()

            # If frame is read correctly ret is True
            if not ret:
                break

            # Convert BGR to RGB
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            frames.append(frame_rgb)

        # Release the video capture object
        cap.release()

        return np.array(frames)

    def get_face_box(self, image: np.ndarray) -> tuple:
        h, w, _ = image.shape
        results = self.face_detection.process(image)

        x1, y1, x2, y2 = -1, -1, -1, -1

        for detection in results.detections:
            # 获取人脸边界框
            bbox = detection.location_data.relative_bounding_box
            x = int(bbox.xmin * w)
            y = int(bbox.ymin * h)
            w = int(bbox.width * w)
            h = int(bbox.height * h)
            x1, y1, x2, y2 = x, y, x + w, y + h

        return x1, y1, x2, y2

    def video_has_face(self, video_path: str):
        try:
            video_info = self.get_video_info(video_path)

            if (video_info["frame_count"] / video_info["fps"]) < 3:
                return False

            video_frames = self.get_video_frames(video_path)
        except Exception as e:
            print(f"Exception: {e} - {video_path}")
            return False

        if len(video_frames) == 0:
            return False

        for frame in video_frames:
            if not self.detect_face(frame):
                return False

        return True

    def video_crop_face(self, video_path: str, output_path: str):
        try:
            video_info = self.get_video_info(video_path)
            video_frames = self.get_video_frames(video_path)
        except Exception as e:
            print(f"Exception: {e} - {video_path}")
            return False
        if len(video_frames) == 0:
            return False

        x1, y1, x2, y2 = 9999, 9999, -1, -1

        for frame in video_frames[::15]:
            f = self.get_face_box(frame)
            x1 = min(f[0], x1)
            y1 = min(f[1], y1)
            x2 = max(f[2], x2)
            y2 = max(f[3], y2)

        x1 = max(0, x1 - 200)
        y1 = max(0, y1 - 200)
        x2 = min(video_info["width"], x2 + 200)
        y2 = min(video_info["height"], y2 + 200)
        command = f"ffmpeg -y -loglevel quiet -i {video_path} -vf crop={x2-x1}:{y2-y1}:{x1}:{y1} -c:a aac -shortest -async 1 -qscale:v 2 {output_path}"
        subprocess.run(command, shell=True)

        new_video_info = self.get_video_info(output_path)

        if new_video_info.get("width", 0) == 0:
            shutil.copyfile(video_path, output_path)

        return True

    def close(self):
        self.face_detection.close()
