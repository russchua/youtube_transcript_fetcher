from pathlib import Path
from bs4 import BeautifulSoup
import requests, sys, re
from youtube_transcript_api import YouTubeTranscriptApi

def get_title(sample_url):
    # Get the title
    # Extracting HTML Code of the Video Page:
    response = requests.get(sample_url)
    html_content = response.text

    # Processing the HTML Code with BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')

    # Extracting <title> tag's content
    title_tag = soup.find('meta', property='og:title')
    video_title = title_tag['content'] if title_tag else 'Title not found'

    # Replace invalid filename characters
    video_title = re.sub(r'[\\/*?:"<>|]', "", video_title)

    return video_title

def extract_video_id(url):
    # Match all common formats
    pattern = r"(?:v=|\/)([0-9A-Za-z_-]{11})(?:\?|&|$)"
    match = re.search(pattern, url)
    return match.group(1) if match else None


def extract_transcript(
    video_id,
    transcript_folder: Path,
    transcript_save_path: Path
):
    # Fetch transcript
    try:
        ytt_api = YouTubeTranscriptApi()
        transcript = ytt_api.fetch(video_id)

        # Combine transcript into a single string
        full_text = "\n".join([entry.text for entry in transcript])
        # save the full text
        transcript_folder.mkdir(parents=True, exist_ok=True)  # Create folder if it doesn't exist
        with open(transcript_save_path, "w", encoding="utf-8") as f:
            f.write(full_text)

    except Exception as e:
        print("An error occurred:", e)


if __name__ == "__main__":
    # Assert that an input string (url) is provided

    if len(sys.argv) == 2:
        sample_url = sys.argv[1]

        # Get the video title
        video_title = get_title(sample_url)

        transcript_folder = Path("./transcripts")
        transcript_save_path = transcript_folder / f"{video_title}.txt"

        # Extract the video ID
        video_id = extract_video_id(sample_url)

        # Extract the transcript
        extract_transcript(video_id, transcript_folder, transcript_save_path)

        print("----------------------------------")
        print("Completed")
        print("----------------------------------")
    else:
        print("Error: No input url provided.")