import boto3
import json
#import openpyxl
import os 
import subprocess

class SpeechGenerator:

    def __init__(self, id, key):
        self.aws_access_key_id = id
        self.aws_secret_access_key = key        
    
    def connect_polly(self,id,key):
        polly_client = boto3.Session(
            aws_access_key_id= id,                     
            aws_secret_access_key= key,
            region_name='ap-northeast-2').client('polly')

        return polly_client
    
    def generate_audio_marks(self, speech_lines, audio_filenames, marks_filenames):
        # connect aws polly
        session = self.connect_polly(self.aws_access_key_id, self.aws_secret_access_key)
        #self.connect_polly()

        # generate one
        for index, speech_line in enumerate(speech_lines, start=0):   # Python indexes start at zero
            print(index, speech_line)
            filename_audio = audio_filenames[index]
            filename_mark = marks_filenames[index]
            self.make_audio_marks(session, speech_line, filename_audio, filename_mark)
        



    def getAudioStream(self,session, line):
        stream = session.synthesize_speech(VoiceId='Seoyeon',
                    OutputFormat='mp3', 
                    Text = line)
        return stream

    def getSpeechMark(self,session, line):
        marks = session.synthesize_speech(VoiceId='Seoyeon',
                    OutputFormat='json',
                    SpeechMarkTypes= ['sentence','viseme','word'], 
                    Text = line)
        return marks

    def saveAudio(self,stream, filename):
        with open(filename,'wb') as file:
            file.write(stream['AudioStream'].read())    

    def saveSpeechMarks(self,marks, filename):
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(marks['AudioStream'].read().decode('UTF-8'))
    
    def make_audio_marks(self,session, lineText, filename_audio, filename_marks):    
        stream = self.getAudioStream(session, lineText)
        marks = self.getSpeechMark(session, lineText)
        self.saveAudio(stream, filename_audio)
        self.saveSpeechMarks(marks, filename_marks)


    def conv_mp3_to_wav(self,audio_filenames):        
        for filename_audio in audio_filenames:
            fileMP3 = filename_audio + '.mp3'
            fileWav = filename_audio + '.wav'
            subprocess.call(['ffmpeg','-i',fileMP3,fileWav])    
        