# Lip Sync Youtube Video Downloader and Analysis Tool

Quickstart Example: [Google Colab](https://colab.research.google.com/drive/19STob2Ss9zHA_VDyP-PLsL6nw8BhFVH2?usp=sharing)

## Requirements

```text
python: >=3.10, <3.14
```

## Quick Install

```bash
git clone https://github.com/clotyxf/lipsync-datasets-ytdownloader.git

cd lipsync-datasets-ytdownloader

pip install -r requirements.txt
```

Requires ffmpeg/mkvmerge for video splitting support.

## Quick Start (Command Line)

```bash
python download_and_process.py --video_meta_file ./video_meta_examples.txt
```

You can get help about the main command using:

```bash
python download_and_process.py --help
```
