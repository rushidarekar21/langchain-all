import streamlit as st
from PIL import Image
import google.generativeai as genai
import speech_recognition as sr

# Configure the Generative AI API key
genai.configure(api_key="AIzaSyCX-lKx6QIAtwEjdPmTBaExfuMGN-DBMlo")

model = genai.GenerativeModel(model_name="gemini-1.5-flash")
# Initialize recognizer
recognizer = sr.Recognizer()

# Function to take audio input from the mic and convert it to text
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

# Initialize session state for prompt if it doesn't exist
if 'prompt' not in st.session_state:
    st.session_state.prompt = ""

# Streamlit app title
st.title('Smart Document Assistant')

# Image upload input
img = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
prompt = ""
# Display uploaded image
if img is not None:
    image = Image.open(img)
    st.image(image, caption='Uploaded Image', use_column_width=True)

    # Select the mode of prompt input
    mode = st.radio("How would you like to provide your prompt?", ('Text Input', 'Speak Prompt'))

    if mode == 'Speak Prompt':
        st.write("Click the button to record your audio.")
        if st.button("Record Audio"):
            st.session_state.prompt = recognize_audio()
            if st.session_state.prompt:
                st.success(f"Recognized Prompt: {st.session_state.prompt}")
    elif mode == 'Text Input':
        st.session_state.prompt = st.text_input("Enter your prompt", st.session_state.prompt)
    
    # Generate response based on prompt and image
    if st.session_state.prompt:
        if st.button("Submit"):
            # Only proceed if prompt is not empty
            try:
                # Generate the text using the correct method from Google Generative AI
                response = model.generate_content([prompt,image])  # Pass model and prompt correctly
                st.subheader("Generated Response:")
                st.code(response.text)  # Extract the text response from the API response
            except Exception as e:
                st.error(f"Error generating response: {str(e)}")
else:
    st.warning("Please upload an image.")
