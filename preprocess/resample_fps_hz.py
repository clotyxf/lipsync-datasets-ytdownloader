import os
import cv2
import subprocess


def get_video_fps(video_path: str):
    cam = cv2.VideoCapture(video_path)
    fps = cam.get(cv2.CAP_PROP_FPS)
    return fps


def resample_fps_hz(video_input, video_output):
    os.makedirs(os.path.dirname(video_output), exist_ok=True)

    if get_video_fps(video_input) == 25:
        command = f"ffmpeg -loglevel error -y -i {video_input} -c:v copy -ar 16000 -q:a 0 {video_output}"
    else:
        command = f"ffmpeg -loglevel error -y -i {video_input} -r 25 -ar 16000 -q:a 0 {video_output}"
    subprocess.run(command, shell=True)
