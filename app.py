from flask import Flask, request, send_file, send_from_directory, jsonify
from moviepy.editor import VideoFileClip, AudioFileClip
import supervision as sv
# Ensure these modules are correctly implemented
from download_youtube import download_youtube_video
from p_image import prompt_image
import requests
import ssl
import os

ssl._create_default_https_context = ssl._create_unverified_context

app = Flask(__name__, static_url_path='', static_folder='static')

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/process-video', methods=['POST'])
def process_video():
    try:
        VIDEO_URL = request.json['videoUrl']
        commentator_key = request.json.get('commentator', 'marv_albert')  # default to 'marv_albert' if not provided

        OPENAI_API_KEY = os.environ.get('OPENAI_KEY', '')

        FRAME_EXTRACTION_FREQUENCY_SECONDS = 2

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
        
        duration = video_clip.duration / 1.5
        PROMPT = (
            f"The commmentry length should be maximum of {duration} seconds."
            f"For every 2 seconds, generate a MAXIMUM of 7 words, NEVER more (it can be less)."
            f"The uploaded series of images is from a single video."
            f"Don't describe litterally that frame 1, frame 2, etc. Do the commentary as if it's a live basketball match"
            f"The frames were sampled every{FRAME_EXTRACTION_FREQUENCY_SECONDS} seconds."
            f"Make sure it takes less than a second to voice the description of each frame."
            f"Make sure to use exclamation points and capital letters to express excitement. "
            f"Describe the video using {commentator_key} style as if he's doing for a Basketball game"
        )
        # Generate commentary based on video frames (ensure this function is implemented correctly)
        description = prompt_image(api_key=OPENAI_API_KEY, images=frames, prompt=PROMPT)

        commentators = {"marv_albert": "OIrVtz6eZY7taDTuddkW", "bob_rathbun": "lxJlkoJYiLlzsAncxcjz"}

        CHUNK_SIZE = 1024

        voice = commentators[commentator_key]
        url = "https://api.elevenlabs.io/v1/text-to-speech/" + voice

        headers = {
            "Accept": "audio/mpeg",
            "Content-Type": "application/json",
            "xi-api-key": os.environ.get('ELEVENLABS_KEY', ''),
        }


        data = {
            "text": description,
            "model_id": "eleven_multilingual_v2",
            "voice_settings": {
                "stability": 0.5,
                "similarity_boost": 0.75,
                "style": 0.4
            }
        }

        response = requests.post(url, json=data, headers=headers)
        with open('audio.mp3', 'wb') as f:
            for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
                if chunk:
                    f.write(chunk)


        # Load the generated audio
        audio_clip = AudioFileClip("audio.mp3")

        # Make sure the audio does not exceed the video length
        if audio_clip.duration > video_clip.duration:
            audio_clip = audio_clip.subclip(0, video_clip.duration)

        # Combine the video with the generated audio
        final_clip = video_clip.set_audio(audio_clip)
        output_file_path = 'final_video.mp4'
        final_clip.write_videofile(output_file_path, codec='libx264', audio_codec='aac')

        return send_file(output_file_path, as_attachment=True)
    except Exception as e:
        app.logger.error(f'Unexpected error: {e}', exc_info=True)
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=False)