from moviepy.editor import VideoFileClip

def trim_video(input_video, start_time = 5, end_time = 15):
    
    # Load the video file
    video = VideoFileClip(input_video)

    # Trim the video
    trimmed_video = video.subclip(start_time, end_time)

    # Save the trimmed video to a new file
    if '_result' not in input_video:
        output_video = input_video.replace('.mp4', '_result.mp4')
    else:
        output_video = input_video
    trimmed_video.write_videofile(output_video)

    # Close the clips to release video files (Optional)
    video.close()
    trimmed_video.close()
    return True