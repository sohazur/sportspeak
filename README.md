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

### Running the Application
To run the application, use the following command:
```bash
python app.py
```

The application will be available at http://127.0.0.1:5000 in your web browser.

## Usage
Enter a YouTube video URL and select a commentator from the dropdown menu. Click on the "Process Video" button to start the processing. A loading spinner will appear, indicating that the video is being processed. Once done, the processed video with commentary will be automatically downloaded.

### License
This project is licensed under the MIT License - see the LICENSE file for details.

### Acknowledgments
Thanks to all the contributors who participated in this project.
Special thanks to OpenAI for the GPT-3 API and ElevenLabs for the text-to-speech service.


