from pytube import YouTube
import streamlit as st
import whisper
import pandas as pd
import ffmpeg

media = st.selectbox('media',['YouTube','Audio upload'])
# if media == 'Youtube':
#   disable_youtube = False
#   disable_audio = True
# elif media == 'Audio upload':
#   disable_audio = False
#   disable_youtube = True
# else:
#   disable_youtube = True
#   disable_audio = True
  
video_url = st.text_input(label='YouTube url',value='https://youtu.be/7EnmlzbocEU') #,disabled=disable_youtube)
# audio_url = st.file_uploader(label='Upload Audio',disabled=disable_audio)
st.video(video_url)

file = YouTube(video_url).streams.filter(only_audio=True).first().download(filename="audio.mp4")

whisper_model = whisper.load_model("base")

load = st.button('Load')

if load:
  with st.spinner('loading...'):
      transcription = whisper_model.transcribe(file)
      # print as DataFrame
      df = pd.DataFrame(transcription['segments'], columns=['start', 'end', 'text'])
  text = "\n".join(df["text"].to_list())
  st.download_button(label='download text file',data=text,file_name='whisper-writer-result.txt',mime='text/plain')
  st.dataframe(df)

  

