import subprocess
import os
import sys

def create_video_from_images(fps, start_frame, end_frame=None, output_file="output_video.mp4"):
    # Check if ffmpeg is installed
    try:
        subprocess.run(['ffmpeg', '-version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
    except FileNotFoundError:
        print("Error: ffmpeg not found. Please install ffmpeg first.")
        return
    
    images_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "kepek")
    # Determine the end frame number
    if end_frame is None:
        # Get the total number of PNG files in the directory
        images_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "kepek")
        files = [f for f in os.listdir(images_dir) if os.path.isfile(os.path.join(images_dir, f)) and f.lower().endswith('.png')]
        total_frames = len(files)
        end_frame = total_frames - 1  # Index starts from 0
    
    # Define the input image pattern
    input_pattern = os.path.join(images_dir, 'output%d.png')
   
    # Construct the ffmpeg command
    ffmpeg_cmd = [
        'ffmpeg',
        '-framerate', str(fps),
        '-start_number', str(start_frame),
        '-i', input_pattern,
        '-c:v', 'libx264',
        '-pix_fmt', 'yuv420p',
        '-crf', '23',  # Adjust quality here (lower is better quality)
        '-frames:v', str(end_frame - start_frame + 1),  # Number of frames to process
        '-y',  # Overwrite output file if it already exists
        output_file
    ]
    
    # Execute ffmpeg command
    subprocess.run(ffmpeg_cmd, check=True)

if __name__ == "__main__":
    # Check if the correct number of command-line arguments is provided
    if len(sys.argv) < 4 or len(sys.argv) > 5:
        print("Usage: python script.py <fps> <start_frame> [<end_frame>] <output_file>")
        sys.exit(1)
    
    # Parse command-line arguments
    fps = int(sys.argv[1])
    start_frame = int(sys.argv[2])
    end_frame = None
    if len(sys.argv) == 5:
        end_frame = int(sys.argv[3])
        output_file = sys.argv[4]
    else:
        output_file = sys.argv[3]
    
    # Call the function to create the video
    create_video_from_images(fps, start_frame, end_frame, output_file)
