import os
import glob
import tqdm
from multiprocessing import Pool

from .face_detector import FaceDetector


def auto_crop(video_path: str, output_path: str):
    if not os.path.isfile(video_path):
        return
    face_detector = FaceDetector()
    has_face = face_detector.video_crop_face(video_path, output_path)
    if not has_face:
        os.remove(video_path)
        print(f"Removed: {video_path}")
    face_detector.close()


def multi_run_wrapper(args):
    return auto_crop(*args)


def auto_crop_handle(input_dir: str, output_dir: str, num_workers=4):
    video_paths = glob.glob(f"{input_dir}/*.mp4")
    video_paths = video_paths = [[_, os.path.join(output_dir, os.path.basename(_))] for _ in video_paths]
    print(f"Removing incorrect affined videos in {input_dir}, Total videos: {len(video_paths)} ...")

    with Pool(num_workers) as pool:
        for _ in tqdm.tqdm(pool.imap_unordered(multi_run_wrapper, video_paths), total=len(video_paths)):
            pass
