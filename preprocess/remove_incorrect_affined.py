import os
import glob
import tqdm
from multiprocessing import Pool

from .face_detector import FaceDetector


def remove_incorrect_affined(video_path: str):
    if not os.path.isfile(video_path):
        return
    face_detector = FaceDetector()
    has_face = face_detector.video_has_face(video_path)
    if not has_face:
        os.remove(video_path)
        print(f"Removed: {video_path}")
    face_detector.close()


def remove_incorrect_affined_handle(input_dir: str, num_workers: int = 1):
    video_paths = glob.glob(f"{input_dir}/*.mp4")
    print(f"Removing incorrect affined videos in {input_dir}, Total videos: {len(video_paths)} ...")

    with Pool(num_workers) as pool:
        for _ in tqdm.tqdm(pool.imap_unordered(remove_incorrect_affined, video_paths), total=len(video_paths)):
            pass
