from pytube import YouTube
import streamlit

video_url = st.text_input(label='YouTube URL',placeholder='https://youtu.be/svm8hlhF8PA')
file = YouTube(video_url).streams.filter(only_audio=True).first().download(filename="audio.mp4")

import whisper

whisper_model = whisper.load_model("base")

transcription = whisper_model.transcribe(file)

import pandas as pd

# print as DataFrame
df = pd.DataFrame(transcription['segments'], columns=['start', 'end', 'text'])
st.download(label='download text file',data=text,file_name='whisper-writer-result.txt',mime='text/plain')
st.dataframe(df)

text = "\n".join(df["text"].to_list())

