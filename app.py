from flask import Flask, request, jsonify, send_file
from moviepy.editor import VideoFileClip, AudioFileClip
import os
import supervision as sv
import download_youtube_video
from openai import OpenAI
import prompt_image

app = Flask(__name__)

@app.route('/process-video', methods=['POST'])
def process_video():
    # Extract YouTube URL from the request
    VIDEO_URL = request.json['videoUrl']


    # fill in your openai api key
    OPENAI_API_KEY = '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'
    
    video_path = download_youtube_video(url=VIDEO_URL)
    
    video_info = sv.VideoInfo.from_video_path(video_path=video_path)
    
    # depending on your video, you may need to sample more or less frequently
    FRAME_EXTRACTION_FREQUENCY_SECONDS = 4

    video_clip = VideoFileClip(video_path)

    PROMPT = (
        f"The commmentry length should be maximum of {video_clip.duration} seconds."
        f"The uploaded series of images is from a single video."
        f"Don't describe litterally that frame 1, frame 2, etc. Do the commentry as if it's a live cricket match"
        f"The frames were sampled every {FRAME_EXTRACTION_FREQUENCY_SECONDS} seconds."
        f"Make sure it takes about {FRAME_EXTRACTION_FREQUENCY_SECONDS // 2} seconds to voice the description of each frame."
        f"Use exclamation points and capital letters to express excitement if necessary. "
        f"Describe the video using Ravi Shastri style as if he's doing for a Cricket game"
    )
    
    frame_extraction_frequency = FRAME_EXTRACTION_FREQUENCY_SECONDS * video_info.fps
    
    frame_generator = sv.get_video_frames_generator(
        source_path=video_path,
        stride=frame_extraction_frequency)

    frames = list(frame_generator)
    
    description = prompt_image(api_key=OPENAI_API_KEY, images=frames, prompt=PROMPT)
    
    client = OpenAI(api_key=OPENAI_API_KEY)

    response = client.audio.speech.create(
        model="tts-1",
        voice="echo",
        input=description,
    )

    response.stream_to_file("audio.mp3")
    
    # Path to your video file
    video_file_path = video_path

    # Path to your generated audio file
    audio_file_path = 'output.mp3'

    # Load the video file
    video_clip = VideoFileClip(video_file_path)

    # Mute the original audio of the video
    video_clip = video_clip.without_audio()

    # Load the audio file
    audio_clip = AudioFileClip('audio.mp3')

    # Set the audio of the video clip as the generated audio
    final_clip = video_clip.set_audio(audio_clip)

    # Output file path
    output_file_path = 'final_video.mp4'

    # Write the result to a file
    final_clip.write_videofile(output_file_path, codec='libx264', audio_codec='aac')

    print("Video combined with audio successfully saved as", output_file_path)
    
    final_video_path = 'final_video.mp4' # This should be replaced with actual processing logic
    
    return send_file(final_video_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)