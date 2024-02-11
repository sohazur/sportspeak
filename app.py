from flask import Flask, request, send_file, send_from_directory, jsonify
from moviepy.editor import VideoFileClip, AudioFileClip
import os
import supervision as sv
# Ensure these modules are correctly implemented
from download_youtube import download_youtube_video
from p_image import prompt_image
from openai import OpenAI

app = Flask(__name__, static_url_path='', static_folder='static')

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/process-video', methods=['POST'])
def process_video():
    try:
        VIDEO_URL = request.json['videoUrl']
        OPENAI_API_KEY = 'private-key'  # Use your actual OpenAI API key

        FRAME_EXTRACTION_FREQUENCY_SECONDS = 4

        # Assuming download_youtube_video correctly downloads the video and returns its local path
        video_path = download_youtube_video(url=VIDEO_URL)
        
        video_info = sv.VideoInfo.from_video_path(video_path=video_path)
        
        frame_extraction_frequency = FRAME_EXTRACTION_FREQUENCY_SECONDS * video_info.fps
        
        frame_generator = sv.get_video_frames_generator(
        source_path=video_path,
        stride=frame_extraction_frequency)

        frames = list(frame_generator)
        # Load the video and mute its original audio
        video_clip = VideoFileClip(video_path).without_audio()
        
        PROMPT = (
            f"The commmentry length should be maximum of {video_clip.duration} seconds."
            f"The uploaded series of images is from a single video."
            f"Don't describe litterally that frame 1, frame 2, etc. Do the commentry as if it's a live cricket match"
            f"The frames were sampled every {FRAME_EXTRACTION_FREQUENCY_SECONDS} seconds."
            f"Make sure it takes about {FRAME_EXTRACTION_FREQUENCY_SECONDS // 2} seconds to voice the description of each frame."
            f"Use exclamation points and capital letters to express excitement if necessary. "
            f"Describe the video using Ravi Shastri style as if he's doing for a Cricket game"
        )
        # Generate commentary based on video frames (ensure this function is implemented correctly)
        description = prompt_image(api_key=OPENAI_API_KEY, images=frames, prompt=PROMPT)

        # Assuming OpenAI's client is set up correctly and prompt_image returns a valid description
        client = OpenAI(api_key=OPENAI_API_KEY)
        response = client.audio.speech.create(
            model="tts-1",
            voice="echo",
            input=description,
        )
        response.stream_to_file("audio.mp3")  # Save the generated audio as audio.mp3

        

        # Load the generated audio
        audio_clip = AudioFileClip("audio.mp3")

        # Combine the video with the generated audio
        final_clip = video_clip.set_audio(audio_clip)
        output_file_path = 'final_video.mp4'
        final_clip.write_videofile(output_file_path, codec='libx264', audio_codec='aac')

        return send_file(output_file_path, as_attachment=True)
    except Exception as e:
        app.logger.error(f'Unexpected error: {e}', exc_info=True)
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)