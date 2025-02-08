from scenedetect import open_video, SceneManager, split_video_ffmpeg
from scenedetect.detectors import ContentDetector
from scenedetect.video_splitter import split_video_ffmpeg


def split_video_into_scenes(video_path: str, output_dir: str, threshold=2.0):
    video = open_video(video_path)
    scene_manager = SceneManager()
    scene_manager.add_detector(ContentDetector(threshold=threshold, min_scene_len=15))
    scene_manager.detect_scenes(video, show_progress=True)
    scene_list = scene_manager.get_scene_list()
    split_video_ffmpeg(
        video_path,
        scene_list,
        output_dir=output_dir,
        show_progress=True,
        arg_override="-map 0:v:0 -map 0:a? -map 0:s? -c:v libx264 -preset slow -crf 0 -c:a aac",
    )
