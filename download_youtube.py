from pytube import YouTube
from format_video import format_video_title

def download_youtube_video(url: str, output_path: str = '.'):
    """
    Downloads a YouTube video to a specified output path.

    Args:
        url (str): URL of the YouTube video.
        output_path (str): Path where the video will be saved. Defaults to the current directory.
    """
    try:
        yt = YouTube(url)
        video_stream = yt.streams.filter(
            progressive=True,
            file_extension='mp4').order_by('resolution').desc().first()

        if video_stream:
            formatted_title = format_video_title(yt.title) + '.mp4'
            video_stream.download(output_path=output_path, filename=formatted_title)
            print(f"Video downloaded successfully: {formatted_title}")
            return formatted_title
        else:
            print("No suitable video stream found.")
    except Exception as e:
        print(f"An error occurred: {e}")