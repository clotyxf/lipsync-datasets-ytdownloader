import os
import shutil
import argparse
import subprocess

from preprocess.data_processing_pipeline import data_processing_pipeline


def download_youtube_video(video_url: str, output_path: str, proxy_url=None, cookie_file=None):
    try:
        if not os.path.exists(os.path.dirname(output_path)):
            os.makedirs(os.path.dirname(output_path), exist_ok=True)

        command = [
            "yt-dlp",
            "-f",
            "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]",
            "--merge-output-format",
            "mp4",
            "--output",
            output_path,
        ]

        if proxy_url:
            command.extend(["--proxy", proxy_url])

        if cookie_file:
            command.extend(["--cookies", cookie_file])

        command.extend([video_url])
        print(f"Downloading video: {video_url} ...")
        result = subprocess.run(command, capture_output=True, text=True, encoding="utf-8")

        if result.returncode == 0:
            print(f"Download {video_url} successfully!")
            return True
        else:
            print(f"Fail to download {video_url}, error info:\n{result.stderr}")
    except Exception as e:
        print(f"error: {e}")

    return False


def load_data(file_path):
    with open(file_path, encoding="utf-8", mode="r") as f:
        youtube_ids = f.readlines()
        youtube_ids = [_.strip() for _ in youtube_ids]

    return youtube_ids


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--proxy_url",
        type=str,
        default="",
        help=(
            "Use the specified HTTP/HTTPS/SOCKS proxy. To enable SOCKS proxy, specify a proper scheme,",
            "e.g. socks5://user:pass@127.0.0.1:1080/.Pass in an empty string (--proxy " ") for direct connection",
        ),
    )
    parser.add_argument("--video_data", type=str, help="Netscape formatted file to read youtube_id")
    parser.add_argument("--output_dir", type=str, default="./datasets", help="output directory")
    parser.add_argument("--threshold", type=float, default=2.0, help="scenedetect threshold")
    parser.add_argument("--workers", type=int, default=1, help="proccessing workers")

    args = parser.parse_args()
    processing_vid_root = os.path.join(args.output_dir, "tmp")
    processed_vid_root = os.path.join(args.output_dir, "split_data")  # processed video path
    raw_vid_root = os.path.join(args.output_dir, "origin_data")  # downloaded raw video path

    os.makedirs(processed_vid_root, exist_ok=True)
    os.makedirs(raw_vid_root, exist_ok=True)

    video_data = load_data(args.video_data)

    for youtube_id in video_data:
        video_url = "https://www.youtube.com/watch?v=" + youtube_id
        print(f"Downloading video url: {video_url} ...")

        raw_vid_path = os.path.join(raw_vid_root, youtube_id + ".mp4")
        result = False

        if not os.path.isfile(raw_vid_path):
            retries = 10
            while retries > 0:
                retries -= 1

                try:
                    result = download_youtube_video(
                        video_url=video_url, output_path=raw_vid_path, proxy_url=args.proxy_url
                    )
                    break
                except:
                    continue
        else:
            result = True

        if result:
            os.makedirs(processing_vid_root, exist_ok=True)

            video_paths = data_processing_pipeline(
                video_file=raw_vid_path,
                output_dir=processing_vid_root,
                secene_threshold=args.threshold,
                num_workers=args.workers,
            )

            for video_path in video_paths:
                video_base_path = os.path.join(processed_vid_root, youtube_id)
                os.makedirs(video_base_path, exist_ok=True)
                shutil.move(video_path, os.path.join(video_base_path, os.path.basename(video_path)))

            shutil.rmtree(processing_vid_root)
