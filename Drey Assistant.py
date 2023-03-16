# Requires: OpenAI, SpeechRecognition, pyttsx3 and PyAudio, use pip install [Library Name]
# Be sure to give it rights to write files or run it in Visual Studio Code or any tipe of IDE.
import openai
import speech_recognition as sr
import pyttsx3
import time 

# Initialize OpenAI API
openai.api_key = "Your OPENAI KEY API"

# Initialize the text to speech engine 
engine =pyttsx3.init()
recognizer = sr.Recognizer()

# Our Functions
def transcribe_audio_to_test(filename):
    with sr.AudioFile(filename)as source:
        audio=recognizer.record(source) 
    try:
        return recognizer.recognize_google(audio)
    except:
        print("skipping unkown error")

def Respond(prompt):
    Response= openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=4000,
        n=1,
        stop=None,
        temperature=0.5,
    )
    return Response ["choices"][0]["text"]

def speak_text(text):
    engine.say(text)
    engine.runAndWait()

def main():
    while True:
        # wait for the user to say assistant.

        print("Say 'assistant' to start recording your question")

        with sr.Microphone() as source:
            audio = recognizer.listen(source)
            try:
                transcription = recognizer.recognize_google(audio)
                print(transcription.lower())

                if transcription.lower()=="assistant":
                    #Record your question for the assistant
                    File ="VoiceInput.wav"
                    speak_text("Say your question")

                    with sr.Microphone() as source:
                        source.pause_threshold = 1
                        audio = recognizer.listen(source,phrase_time_limit=None,timeout=None)

                        with open(File,"wb")as f:
                            f.write(audio.get_wav_data())
                            
                    #Translate your audio into text
                    Question = transcribe_audio_to_test(File)

                    if Question:
                        print(f"you said: {Question}")
                        
                        #Generate the response
                        Response = Respond(Question)
                        print(f"Assistant said: {Response}")
                            
                        #read resopnse using GPT3
                        speak_text(Response)
                        
            except Exception as e:
                
                print("An error ocurred : {}".format(e))
if __name__=="__main__":
    main()
