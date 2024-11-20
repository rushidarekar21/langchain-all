import streamlit as st
from PIL import Image
import google.generativeai as genai
import speech_recognition as sr

# Configure Generative AI
genai.configure(api_key="AIzaSyCX-lKx6QIAtwEjdPmTBaExfuMGN-DBMlo")
model = genai.GenerativeModel(model_name="gemini-1.5-flash")

# Initialize recognizer
recognizer = sr.Recognizer()

def recognize_audio():
    with sr.Microphone() as source:
        st.info("Adjusting for ambient noise... Please wait.")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        st.info("Listening... Please speak now.")
        audio = recognizer.listen(source)

        try:
            # Convert audio to text using Google Web Speech API
            st.info("Converting speech to text...")
            text = recognizer.recognize_google(audio)
            return text
        except sr.UnknownValueError:
            st.error("Sorry, I could not understand the audio.")
            return ""
        except sr.RequestError:
            st.error("Could not request results from Google Speech Recognition service.")
            return ""

# Upload an image
img = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

# Check if an image is uploaded
if img is not None:
    image = Image.open(img)
    st.image(image, caption='Uploaded Image', use_column_width=True)

    use_mic = st.checkbox("Use microphone for prompt input")

    if use_mic:
        st.write("Click the button to record your audio.")
        if st.button("Record Audio"):
            prompt = recognize_audio()

            if prompt:
                # Generate text content from the prompt
                response = model.generate_content([prompt,image])
                st.code(response.text)
else:
    st.warning("Please upload an image.")
