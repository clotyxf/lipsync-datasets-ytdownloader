import os
import glob
import shutil
from preprocess.auto_crop import auto_crop_handle
from preprocess.detect_shot import split_video_into_scenes
from preprocess.remove_incorrect_affined import remove_incorrect_affined_handle
from preprocess.resample_fps_hz import resample_fps_hz


def data_processing_pipeline(video_file: str, output_dir: str, secene_threshold: float = 2.0, num_workers: int = 1):
    video_basename = os.path.basename(video_file).split(".")[0]
    output_dir = os.path.join(output_dir, video_basename)

    if os.path.isdir(output_dir):
        shutil.rmtree(output_dir)

    print("(1/4) Resampling FPS hz...")
    fps_dir = os.path.join(output_dir, "resample_fps")
    os.makedirs(fps_dir, exist_ok=True)
    fps_video_file = os.path.join(fps_dir, os.path.basename(video_file))
    fps_video_file = video_file
    # resample_fps_hz(video_file, fps_video_file)
    print("(2/4) Detecting shot...")
    detect_scene_output_dir = os.path.join(output_dir, "scenes")
    os.makedirs(detect_scene_output_dir, exist_ok=True)
    split_video_into_scenes(fps_video_file, detect_scene_output_dir, secene_threshold)

    print("(3/4) Removing incorrect affined videos...")
    remove_incorrect_affined_handle(detect_scene_output_dir, num_workers=num_workers)

    print("(4/4) Auto crop videos...")
    auto_crop_op_output_dir = os.path.join(output_dir, "auto_crop")
    os.makedirs(auto_crop_op_output_dir, exist_ok=True)
    auto_crop_handle(detect_scene_output_dir, auto_crop_op_output_dir, num_workers=num_workers)

    return glob.glob(f"{auto_crop_op_output_dir}/*.mp4")


if __name__ == "__main__":
    video_file = "./examples/video/PFBrK7pbqCU.mp4"
    output_dir = "./examples/shot"
    data_processing_pipeline(video_file=video_file, output_dir=output_dir, secene_threshold=2.5)
