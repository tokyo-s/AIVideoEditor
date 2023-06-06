import config
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip

def second_to_timecode(x: float) -> str:
    hour, x = divmod(x, 3600)
    minute, x = divmod(x, 60)
    second, x = divmod(x, 1)
    millisecond = int(x * 1000.)

    return '%.2d:%.2d:%.2d,%.3d' % (hour, minute, second, millisecond)

def _helper(end: int, lines, section, words, start) -> None:
    lines.append("%d" % section)
    lines.append(f"{second_to_timecode(words[start]['start_sec'])} --> {second_to_timecode(words[end]['end_sec'])}")
    lines.append(' '.join(x['word'] for x in words[start:(end + 1)]))
    lines.append('')

def to_srt(words: list, endpoint_sec: float = 1., length_limit: int = 16) -> str:

    lines = list()
    section = 0
    start = 0
    for k in range(1, len(words)):
        _helper(k - 1, lines, section, words, start)
        start = k
        section += 1
    _helper(len(words) - 1, lines, section, words, start)

    return '\n'.join(lines)


# Function to convert subtitle timestamp to seconds
def timestamp_to_seconds(timestamp):
    hours, minutes, seconds = map(float, timestamp.replace(',','.').split(':'))
    return hours * 3600 + minutes * 60 + seconds
    
def combine_subtitles_on_video(subtitles, filename_video):
    # Load the video file
    video = VideoFileClip(filename_video)

    # Parse the subtitles
    subtitle_clips = []
    for i in range(0, len(subtitles), 4):
        start_time = timestamp_to_seconds(subtitles[i + 1].split("-->")[0].strip())
        end_time = timestamp_to_seconds(subtitles[i + 1].split("-->")[1].strip())
        text = subtitles[i + 2].strip()

        # Create a TextClip for each subtitle
        text_clip = TextClip(text, fontsize=24, color='white', bg_color='black', size=(video.size[0], None), method='caption')
        text_clip = text_clip.set_start(start_time).set_duration(end_time - start_time)
        text_clip = text_clip.set_position(('center', video.size[1] - text_clip.size[1] * 2 - 10)).set_start(start_time).set_duration(end_time - start_time)
        subtitle_clips.append(text_clip)

    # Add the subtitles to the video
    final_video = CompositeVideoClip([video] + subtitle_clips)

    # Save the video with subtitles
    final_video_path = filename_video.replace('.mp4', '_result.mp4').replace('files','App/static')
    final_video.write_videofile(final_video_path)

    return final_video_path

def add_subtitles_on_video(text, filename_video):

    lines = []
    for segment in text['segments']:
        sub = {}
        sub['start_sec'] = segment['start']
        sub['end_sec'] = segment['end']
        sub['word'] = segment['text']
        lines.append(sub)

    subtitles = to_srt(lines)
    subtitles = subtitles.splitlines(True)

    return combine_subtitles_on_video(subtitles, filename_video)

