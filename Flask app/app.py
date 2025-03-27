rom flask import Flask, render_template, request
import json
import requests
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)

# S3 URLs
BASE_URL = 'https://nlpprojectamirhossein.s3.us-east-1.amazonaws.com/datasource/'
json_url = 'https://nlpprojectamirhossein.s3.us-east-1.amazonaws.com/json/extracted_key_phrases_and_topics.json'

video_files = [
    "Mod01_Course+Overview.mp4",
    "Mod02_Intro.mp4",
    "Mod02_Sect01.mp4",
    "Mod02_Sect02.mp4",
    "Mod02_Sect03.mp4",
    "Mod02_Sect04.mp4",
    "Mod02_Sect05.mp4",
    "Mod02_WrapUp.mp4",
    "Mod03_Intro.mp4",
    "Mod03_Sect01.mp4",
    "Mod03_Sect02_part1.mp4",
    "Mod03_Sect02_part2.mp4",
    "Mod03_Sect02_part3.mp4",
    "Mod03_Sect03_part1.mp4",
    "Mod03_Sect03_part2.mp4",
    "Mod03_Sect03_part3.mp4",
    "Mod03_Sect04_part1.mp4",
    "Mod03_Sect04_part2.mp4",
    "Mod03_Sect04_part3.mp4",
    "Mod03_Sect05.mp4",
    "Mod03_Sect06.mp4",
    "Mod03_Sect07_part1.mp4",
    "Mod03_Sect07_part2.mp4",
    "Mod03_Sect07_part3.mp4",
    "Mod03_Sect08.mp4",
    "Mod03_WrapUp.mp4",
    "Mod04_Intro.mp4",
    "Mod04_Sect01.mp4",
    "Mod04_Sect02_part1.mp4",
    "Mod04_Sect02_part2.mp4",
 "Mod04_Sect02_part3.mp4",
    "Mod04_WrapUp.mp4",
    "Mod05_Intro.mp4",
    "Mod05_Sect01_ver2.mp4",
    "Mod05_Sect02_part1_ver2.mp4",
    "Mod05_Sect02_part2.mp4",
    "Mod05_Sect03_part1.mp4",
    "Mod05_Sect03_part2.mp4",
    "Mod05_Sect03_part3.mp4",
    "Mod05_Sect03_part4_ver2.mp4",
    "Mod05_WrapUp_ver2.mp4",
    "Mod06_Intro.mp4",
    "Mod06_Sect01.mp4",
    "Mod06_Sect02.mp4",
    "Mod06_WrapUp.mp4",
    "Mod07_Sect01.mp4"
]


def generate_wordcloud_image(text):
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)
    img = io.BytesIO()
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.tight_layout(pad=0)
    plt.savefig(img, format='png')
    plt.close()
    img.seek(0)
    return base64.b64encode(img.read()).decode('utf-8')

@app.route('/', methods=['GET', 'POST'])
def dashboard():
    search_query = request.form.get('search', '').lower()
    response = requests.get(json_url)

    if response.status_code != 200:
        return "Error fetching JSON metadata."

    try:
        json_data = response.json()
    except Exception as e:
        return f"JSON decode error: {e}"
  filtered_key_phrases = {}
    relevant_movies = set()

    for file_name, content in json_data.items():
        key_phrases = content.get('key_phrases', [])
        topics = content.get('topics', [])

        relevant_key_phrases_list = [kp for kp in key_phrases if search_query in kp.lower()]
        relevant_topics_list = [t for t in topics if search_query in ' '.join(t).lower()]

        if relevant_key_phrases_list or relevant_topics_list:
            filtered_key_phrases[file_name] = {
                "key_phrases": relevant_key_phrases_list,
                "topics": relevant_topics_list
            }
            relevant_movies.add(file_name + ".mp4")

    movie_urls = [BASE_URL + video for video in video_files if video in relevant_movies]

    return render_template('index.html',
                           movie_urls=movie_urls,
                           search_query=search_query,
                           filtered_key_phrases=filtered_key_phrases)

@app.route('/watch/<video_filename>')
def watch(video_filename):
    video_url = BASE_URL + video_filename
    movie_name = video_filename.rsplit('.', 1)[0]

    response = requests.get(json_url)
    json_data = response.json()

    video_key = movie_name.replace('+', ' ')
    phrases = json_data.get(video_key, {}).get("key_phrases", [])
    topics = json_data.get(video_key, {}).get("topics", [])

    phrase_text = ' '.join(phrases)
    wordcloud_img = generate_wordcloud_image(phrase_text)

    return render_template('watch.html',
                           video_url=video_url,
                           movie_name=movie_name,
                           key_phrases=phrases,
                           topics=topics,
 wordcloud_img=wordcloud_img)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

