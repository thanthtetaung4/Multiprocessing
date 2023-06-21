import cv2
import pathlib
import multiprocessing as mp
import time
from tqdm import tqdm
from termcolor import colored

def frame_to_img(video_path):
    # Open the video file
    video = cv2.VideoCapture(video_path)

    # Check if the video file was opened successfully
    if not video.isOpened():
        print("Error opening video file")
        exit()

    # Initialize variables
    frame_count = 0
    image_count = 0

    # Creating a folder to store the images
    current_path = pathlib.Path.cwd() / "parallel_outputs/"
    # print(current_path)
    file_count = len(list(current_path.glob('*/')))
    pathlib.Path(current_path / f"output_{file_count+1}").mkdir(parents=True, exist_ok=True)
    output_folder = current_path / f"output_{file_count+1}/"
    
    video_name = video_path.split("\\")[-1]
    print(colored(f"\nExtracting frames from {video_name}", 'white', 'on_green'))

    # Get the total number of frames in the video
    total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))

    # Create a progress bar
    progress_bar = tqdm(total=total_frames, unit='frames')

    # Read and save frames as images
    while True:
        # Read a frame from the video
        ret, frame = video.read()

        # Break the loop if there are no more frames
        if not ret:
            break

        # Save the frame as an image file
        image_path = f"{output_folder}/frame_{image_count}.jpg"  # Replace with your desired image file name
        cv2.imwrite(image_path, frame)

        # Increment counters
        frame_count += 1
        image_count += 1

        # Update the progress bar
        progress_bar.update(1)

    # Release the video file and close windows
    video.release()
    cv2.destroyAllWindows()

    # Close the progress bar
    progress_bar.close()
    
    pid_print = colored(f"Process ID: {mp.current_process().pid}", 'white', 'on_red')
    print(colored(f"\nExtracted {image_count} frames from {video_name} done by {pid_print}", 'white', 'on_green'))

def parallel():
    start = time.time()
    video_path = pathlib.Path.cwd() / "input_set_2/"
    pool = mp.Pool(mp.cpu_count())
    pool.map(frame_to_img, [str(video) for video in video_path.iterdir()])
    print(colored(f"Time taken by Parallel Function: {time.time() - start} seconds",'white', 'on_yellow'))

if __name__ == "__main__":
    print(colored("Parallel Started", 'white', 'on_yellow'))
    parallel()
    