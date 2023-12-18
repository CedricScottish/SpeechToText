import moviepy.editor as mp
import speech_recognition as sr
import os
from pydub import AudioSegment
from pydub.silence import split_on_silence

r = sr.Recognizer()
r.operation_timeout = 150

def extract_audio(path):    
    video = mp.VideoFileClip(path)         
    audioFile = video.audio 
    audioFile.write_audiofile(path.split(".")[0] + ".wav") 

def convert_mp3_to_wav(path):
    sound = AudioSegment.from_mp3(path) 
    sound.export(path.split(".")[0] + ".wav", format="wav") 


def transcribe_audio(path):        
    fileName =path.split(".")[0]
    
    sound = AudioSegment.from_wav(path)
    chunks = split_on_silence(sound, min_silence_len=700, silence_thresh=sound.dBFS-14, keep_silence=700)
    
    folderName = f"{fileName}_Audio_Chunks"
    if not os.path.isdir(folderName):
        os.mkdir(folderName)
    
    
    for i, audioChunk in enumerate(chunks, start=1):
        chunkFilename = os.path.join(folderName, f"Audio{i}.wav")
        audioChunk.export(chunkFilename, format="wav")
        
        
    wholeText = ""
    
    for i, audioChunk in enumerate(chunks, start=1):
        chunkFilename = os.path.join(folderName, f"Audio{i}.wav")
        
        file1 = open(f"{fileName}_OnlineText.txt", "a", encoding="utf-8")
        
        with sr.AudioFile(chunkFilename) as source:
            audio_listened = r.record(source)        
            
            try:                
                text = r.recognize_google_cloud(audio_listened, language="tr-TR")    
                #  text = r.recognize_google(audio_listened, language="tr-TR")              
            except Exception as ex:
                print("Error:", str(ex))
                text= f"Error: {str(i)}. Audio File Transcribe Fault"
                file1.write(text + "\n")  
                continue
            else:
                text = f"{text.capitalize()}. "
                print(chunkFilename, ":", text)
                file1.write(text + "\n")                
                wholeText += text + "\n"                
    return wholeText




fileName="fileName"
convert_mp3_to_wav(fileName +".mp3")
# extract_audio(fileName+".mp4")
result = transcribe_audio(fileName + ".wav")
print(result)
print(result, file=open(fileName+"_Text.txt", "w", encoding="utf-8"))




