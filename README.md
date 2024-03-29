# Video Commentary Generator (SportSpeak)

This project is a Flask-based web application that processes YouTube videos by adding generated commentaries with selected commentators' voices.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

You will need Python installed on your system. This project was built with Python 3.9.

### Installing

First, clone the repository to your local machine:

```bash
git clone https://github.com/sohazur/sportspeak.git
```

Navigate to the project directory:

```bash
cd sportspeak
```

Install the required packages using pip:

```bash
pip install -r requirements.txt
```

### Setting Up Environment Variables

To keep your API keys secure, you'll need to set up environment variables. This prevents sensitive information from being hard-coded into your application, which is a security risk.

1. Create a file named `.env` in the root directory of your project.
2. Add your API keys to the `.env` file with the following format:

```env
OPENAI_API_KEY='your_openai_api_key_here'
ELEVENLABS_API_KEY='your_elevenlabs_api_key_here'
```

```bash
pip install python-dotenv
```

### Running the Application

To run the application, use the following command:

```bash
python app.py
```

The application will be available at http://127.0.0.1:5000 in your web browser.

## Usage

Enter a YouTube video URL and select a commentator from the dropdown menu. Click on the "Process Video" button to start the processing. A loading spinner will appear, indicating that the video is being processed. Once done, the processed video with commentary will be automatically downloaded.

### Contributors

1. Sohazur Islam - m80008603@zu.ac.ae
2. Arthur Diniz - m80008599@zu.ac.ae
3. Shanzila Ahmed - m80008600@zu.ac.ae
4. Maryam Alabbar - 202120508@zu.ac.ae

### Acknowledgments

- OpenAI API - https://platform.openai.com/docs/introduction
- ElevenLabs API - https://elevenlabs.io/docs/api-reference/text-to-speech
- Roboflow - https://github.com/roboflow/awesome-openai-vision-api-experiments/tree/main/experiments/automated-voiceover-of-nba-game
