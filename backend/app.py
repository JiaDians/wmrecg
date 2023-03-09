from flask import Flask, render_template, request
from watermelon_speech_recognition import process
import base64

app = Flask(__name__)


@app.route("/submit", methods=['POST'])
def submit():
    content = request.json
    decode_bytes = base64.b64decode(content['data'])
    with open('wav/wavfile.wav','wb') as wav_file:
        wav_file.write(decode_bytes)
    ans = process(content['category'], 'wav/wavfile.wav')

    return ans



if __name__ == "__main__":
    # app.run(host='140.116.245.157', port=40250)
    app.run(host='0.0.0.0', port=40250)
