from moviepy.editor import VideoClip, concatenate_videoclips, ImageClip, AudioFileClip, CompositeVideoClip
from moviepy.video.fx.all import fadein, fadeout, resize, rotate
from backend import *


def images_to_video(images, output_video, audio_file, transition_list, duration_list, resolution):
    resolutions = {
        360: (480, 360),
        480: (854, 480),
        720: (1280, 720),
        1080: (1920, 1080)
    }
    width, height = resolutions[resolution]

    available_transitions = {
        "crossfadein": lambda clip, start_time: clip.set_start(start_time).crossfadein(0.5),
        "fadein": lambda clip, start_time: clip.set_start(start_time).fadein(0.5),
        "fadeout": lambda clip, start_time: clip.set_start(start_time).fadeout(0.5),
        "crossfadeout": lambda clip, start_time: clip.set_start(start_time).crossfadeout(0.5),
        "rotate_clockwise": lambda clip, start_time: clip.set_start(start_time).crossfadein(0.5).fl_time(lambda t: 90*t),
        "rotate_anticlockwise": lambda clip, start_time: clip.set_start(start_time).crossfadein(0.5).fl_time(lambda t: -90*t),
        # Add more transitions as needed
    }



    image_files = [cv2.cvtColor(img, cv2.COLOR_BGR2RGB) for img in images]
    clips = []
    total_video_duration = sum(duration_list)

    # Trim audio to match total video duration
    audio = AudioFileClip(audio_file)
    if audio.duration > total_video_duration:
        audio = audio.subclip(0, total_video_duration)

    for idx, image_file in enumerate(image_files):
        transition_func = available_transitions.get(transition_list[idx], available_transitions["crossfadein"])  # Default to crossfadein if invalid option provided
        # Load the image
        img = image_files[idx]

        # Calculate the start and end times for the current image clip
        clip_start_time = idx * duration_list[idx]
        clip_end_time = (idx + 1) * duration_list[idx]

        # Create a clip for the current image
        img_clip = VideoClip(make_frame=lambda t, img=img: img, duration=duration_list[idx])

        # Apply transition if not the first clip
        if idx > 0:
            img_clip = transition_func(img_clip, clip_start_time)

        # Resize the clip to the specified resolution
        resized_clip = img_clip.resize(width=width, height=height)

        # Set the start and end times for the clip
        resized_clip = resized_clip.set_start(clip_start_time).set_end(clip_end_time)

        # Append the resized clip to the list of clips
        clips.append(resized_clip)

    # Concatenate all clips into the final video
    final_clip = concatenate_videoclips(clips, method="compose")

    # Set the audio for the final video
    final_clip = final_clip.set_audio(audio)

    # Write the final video file
    final_clip.write_videofile(output_video, fps=24)  # Adjust fps as needed

# Usage example
# images = fetch_images(1)
# transition_list = ["crossfadein","fadeout","rotate_clockwise","crossfadeout","fadein","rotate_anticlockwise"]
# duration_list = [1, 2, 3, 4, 5, 6] # Duration for each image in seconds
# output_file = './static/videos/output.mp4'
# transition_duration = 1  # in seconds
# background_audio = "/home/vishal/ug1/ISS/course-project-edgarallanpoopoo/yourNewHome.mp3"
# images_to_video(images, output_file, background_audio, transition_list=transition_list, duration_list=duration_list, resolution=360)
