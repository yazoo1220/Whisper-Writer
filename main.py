from pytube import YouTube
import streamlit as st

media = st.selectbox('media',['YouTube','Audio upload'])
if media == 'Youtube':
  disable_youtube = False
  disable_audio = True
elif media == 'Audio upload':
  disable_audio = False
  disable_youtube = True
else:
  disable_youtube = True
  disable_audio = True
  
video_url = st.text_input(label='YouTube URL',placeholder='https://youtu.be/svm8hlhF8PA',disabled=disable_youtube)
audio_url = st.file_uploader(label='Upload Audio',disabled=disable_audio)

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

