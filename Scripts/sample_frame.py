import os
from concurrent import futures
import argparse

def trim_video(video_name, out_folder, duration_time: str, interval_time=30):
    if os.path.exists(out_folder):
        os.system('rm -rf ' + out_folder + '/*')
        os.system('rm -rf ' + out_folder)
    os.makedirs(out_folder)
    cmd = 'ffmpeg -i %s -c copy -map 0 -segment_time %d -f segment %s/%s.mp4' % (video_name, interval_time, out_folder, '%08d')
    os.system(cmd)

def extract_frames(video_name, out_folder, fps=3):
    if os.path.exists(out_folder):
        os.system('rm -rf ' + out_folder + '/*')
        os.system('rm -rf ' + out_folder)
    os.makedirs(out_folder)
    cmd = 'ffmpeg -v 0 -i %s -r %d -q 0 %s/%s.jpg' % (video_name, fps, out_folder, '%08d')
    os.system(cmd)

def process(line):
    print(line)
    mp4_name, folder_frame = line
    extract_frames(mp4_name, folder_frame)

def process_trim(line):
    print(line)
    mp4_name, folder_video = line
    trim_video(mp4_name, folder_video, '18:29', 30)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Get frames from video')
    parser.add_argument('--input_path', type=str, default='Videos', help='input directory of videos')
    parser.add_argument('--output_trim_path', type=str, default='Trim', help='output directory of trimed videos')
    parser.add_argument('--output_frame_path', type=str, default='Frames', help='output directory of sampled frames')
    args = parser.parse_args()

    if not os.path.exists(args.output_trim_path):
        os.mkdir(args.output_trim_path)
    if not os.path.exists(args.output_frame_path):
        os.mkdir(args.output_frame_path)

    mp4_file = os.listdir(args.input_path)
    lines = [(os.path.join(args.input_path, mp4), 
              os.path.join(args.output_trim_path, mp4.split(".")[0])) for mp4 in mp4_file]
    
    with futures.ProcessPoolExecutor(max_workers=10) as executer:
        fs = [executer.submit(process_trim, line) for line in lines]

    for mp4 in mp4_file:
        mp4_trim_files = os.listdir(os.path.join(args.output_trim_path, mp4.split(".")[0]))

        lines = [(os.path.join(args.output_trim_path, mp4.split(".")[0], mp4_trim), 
                  os.path.join(args.output_frame_path, mp4.split(".")[0], mp4_trim.split(".")[0])) for mp4_trim in mp4_trim_files]

        # multi thread
        with futures.ProcessPoolExecutor(max_workers=10) as executer:
            fs = [executer.submit(process, line) for line in lines]
    print("done")