from pytube import YouTube
import streamlit as st
import whisper
import pandas as pd
import ffmpeg


media = st.selectbox('media',['YouTube','Audio upload'])
if media == 'YouTube':
  video_url = st.text_input(label='YouTube url',value='https://youtu.be/7EnmlzbocEU')
  st.video(video_url)
  file = YouTube(video_url).streams.filter(only_audio=True).first().download(filename="audio.mp4")
else:
  uploaded_file = st.file_uploader("Upload an audio file", type=["wav", "mp3"])
  if uploaded_file is not None:
      # Save the uploaded file to a temporary file on disk
      with open(os.path.join("temp", uploaded_file.name), "wb") as f:
          f.write(uploaded_file.read())
      # Get the file path to the temporary file
      file = os.path.join("temp", uploaded_file.name)

whisper_model = whisper.load_model("base")

load = st.button('Load')

if file and load:
  with st.spinner('loading... This might take minutes'):
      transcription = whisper_model.transcribe(file)
      # print as DataFrame
      df = pd.DataFrame(transcription['segments'], columns=['start', 'end', 'text'])
      text = "\n".join(df["text"].to_list())
      st.download_button(label='download text file',data=text,file_name='whisper-writer-result.txt',mime='text/plain')
      st.dataframe(df)

  

