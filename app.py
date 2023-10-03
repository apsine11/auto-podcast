# import os
# import openai
# from elevenlabs import set_api_key, voices, generate, play, Voice, VoiceSettings, save
# from flask import Flask, request, jsonify
# from dotenv import load_dotenv
# load_dotenv()

# app = Flask(__name__)


# @app.route('/generate-audio', methods=['POST'])
# def generate_audio():
#     data = request.get_json()
#     topic = data.get('topic')
#     tone1 = data.get('tone1')
#     tone2 = data.get('tone2')

#     openai.api_key = os.getenv("OPENAI_API_KEY")

#     elevenlabs_api_key = os.getenv("ELEVENLABS_API_KEY")
#     set_api_key(elevenlabs_api_key)

#     # Define your prompt and input variables
#     prompt = """
#     Compose a monologue on the topic of [topic].
#     Create an engaging and upbeat educational content piece that not only explains the key differences between [topic] but also injects personality into the presentation.
#     Keep the tone [tone1] and [tone2] throughout.
#     The transcript must have a minimum of 4,800 words, with the option to extend it up to 6,000 words if necessary to provide comprehensive coverage.
#     """

#     # Input variables
#     topic = "4-3-3 vs 4-4-2 Diamond football formations"
#     tone1 = "upbeat"
#     tone2 = "informative"

#     # Combine input variables into the prompt
#     prompt = prompt.replace("[topic]", topic)
#     prompt = prompt.replace("[tone1]", tone1)
#     prompt = prompt.replace("[tone2]", tone2)

#     # Generate podcast transcript
#     response = openai.ChatCompletion.create(
#         model="gpt-4",
#         messages=[{"role": "system", "content": prompt}],
#         max_tokens=100,  # Adjust the length as needed
#         temperature=0.7,  # Adjust the creativity of the response
#         stop=None  # You can specify custom stop words to control response length
#     )

#     transcript = response["choices"][0]["message"]["content"]

#     audio = generate(
#         text=transcript,
#         voice=Voice(
#             voice_id='cqBE7vlHJ0tmLldYtRXM',
#             settings=VoiceSettings(
#                 stability=0.50, similarity_boost=0.50, style=0.0, use_speaker_boost=True)
#         ),
#         model='eleven_multilingual_v2'
#     )

#     file = save(
#         audio=audio,
#         filename="test.wav")

#     return file

# if __name__ == '__main__':
#     app.run(debug=True)

import os
import logging
from flask import Flask, request, jsonify
import openai
from elevenlabs import set_api_key, generate, Voice, VoiceSettings
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)


# Setup logging
app.logger.setLevel(logging.INFO)


def save(audio, filename):
    app.logger.info(f"Saving audio to {filename}")
    with open(filename, 'wb') as f:
        f.write(audio)


@app.route('/generate-audio', methods=['POST'])
def generate_audio():
    app.logger.info("Received request to generate audio")

    data = request.get_json()
    app.logger.info(f"Data received: {data}")

    # Default values added
    topic = data.get('topic', "4-3-3 vs 4-4-2 Diamond football formations")
    tone1 = data.get('tone1', "upbeat")
    tone2 = data.get('tone2', "informative")

    app.logger.info(f"Using topic: {topic}, tone1: {tone1}, tone2: {tone2}")

    openai.api_key = os.getenv("OPENAI_API_KEY")
    elevenlabs_api_key = os.getenv("ELEVENLABS_API_KEY")
    set_api_key(elevenlabs_api_key)

    # Define your prompt
    prompt = """
    Compose a monologue on the topic of [topic]. 
    Create an engaging and upbeat educational content piece that thoroughly explores and explains the various aspects, features, or elements of [topic], injecting personality into the presentation. 
    Keep the tone [tone1] and [tone2] throughout. 
    The transcript must have a minimum of 4,800 words, with the option to extend it up to 6,000 words if necessary to provide comprehensive coverage.
    """

    # Combine input variables into the prompt
    prompt = prompt.replace("[topic]", topic)
    prompt = prompt.replace("[tone1]", tone1)
    prompt = prompt.replace("[tone2]", tone2)

    app.logger.info("Generating podcast transcript")
    # Generate podcast transcript
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "system", "content": prompt}],
        max_tokens=100,  # Adjust the length as needed
        temperature=0.7,
        stop=None
    )

    transcript = response["choices"][0]["message"]["content"]
    app.logger.info("Transcript generated")

    app.logger.info("Generating audio")
    audio = generate(
        text=transcript,
        voice=Voice(
            voice_id='cqBE7vlHJ0tmLldYtRXM',
            settings=VoiceSettings(
                stability=0.50, similarity_boost=0.50, style=0.0, use_speaker_boost=True)
        ),
        model='eleven_multilingual_v2'
    )
    app.logger.info("Audio generated")

    save(audio, "test.wav")

    app.logger.info("Sending response")
    # Assuming the audio variable contains the link or data to the audio
    return jsonify({
        "audio": audio
    })


if __name__ == '__main__':
    app.run(debug=True)
