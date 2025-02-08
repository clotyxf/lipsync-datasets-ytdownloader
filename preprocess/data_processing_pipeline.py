import os
import glob
import shutil
from preprocess.auto_crop import auto_crop_handle
from preprocess.detect_shot import split_video_into_scenes
from preprocess.remove_incorrect_affined import remove_incorrect_affined_handle
from preprocess.resample_fps_hz import resample_fps_hz


def data_processing_pipeline(
    video_file: str,
    output_dir: str,
    scene_threshold: float = 2.0,
    num_workers: int = 1,
    modes: str = "resample_fps,split_video,auto_crop",
):
    video_basename = os.path.basename(video_file).split(".")[0]
    output_dir = os.path.join(output_dir, video_basename)

    if os.path.isdir(output_dir):
        shutil.rmtree(output_dir)

    modes = modes.split(",")

    if "resample_fps" in modes:
        print("(1/4) Resampling FPS hz...")
        fps_dir = os.path.join(output_dir, "resample_fps")
        os.makedirs(fps_dir, exist_ok=True)
        fps_video_file = os.path.join(fps_dir, os.path.basename(video_file))
        resample_fps_hz(video_file, fps_video_file)
        video_file = fps_video_file
    else:
        print("(1/4) Skip Resampling FPS hz...")

    if "split_video" in modes:
        print("(2/4) Detecting shot...")
        detect_scene_output_dir = os.path.join(output_dir, "scenes")
        os.makedirs(detect_scene_output_dir, exist_ok=True)
        split_video_into_scenes(video_file, detect_scene_output_dir, scene_threshold)

        print("\n(3/4) Removing incorrect affined videos...")
        remove_incorrect_affined_handle(detect_scene_output_dir, num_workers=num_workers)
    else:
        print("(2/4) Skip Detecting shot...")
        print("(3/4) Skip Removing incorrect affined videos...")
        detect_scene_output_dir = os.path.dirname(video_file)

    if "auto_crop" in modes:
        print("\n(4/4) Auto crop videos...")
        auto_crop_op_output_dir = os.path.join(output_dir, "auto_crop")
        os.makedirs(auto_crop_op_output_dir, exist_ok=True)
        auto_crop_handle(detect_scene_output_dir, auto_crop_op_output_dir, num_workers=num_workers)
        video_paths = glob.glob(f"{auto_crop_op_output_dir}/*.mp4")
    else:
        print("\n(4/4) Skip Auto crop videos...")
        video_paths = glob.glob(f"{detect_scene_output_dir}/*.mp4")

    return video_paths


if __name__ == "__main__":
    video_file = "./examples/video/PFBrK7pbqCU.mp4"
    output_dir = "./examples/shot"
    data_processing_pipeline(video_file=video_file, output_dir=output_dir, scene_threshold=2.5)
