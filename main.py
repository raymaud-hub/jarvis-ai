import os
import speech_recognition as sr
import pyttsx3
from dotenv import load_dotenv
import openai

# Load environment variables
load_dotenv()

# Initialize OpenAI client
api_key = os.getenv('OPENAI_API_KEY')
openai.api_key = api_key

# Initialize text-to-speech engine
engine = pyttsx3.init()
engine.setProperty('rate', 150)  # Speed of speech
engine.setProperty('volume', 1)  # Volume (0.0 to 1.0)

# Initialize speech recognizer
recognizer = sr.Recognizer()

def speak(text: str):
    """
    Convert text to speech and play it.
    
    Args:
        text: The text to speak
    """
    print(f"🔊 Jarvis: {text}")
    engine.say(text)
    engine.runAndWait()

def listen() -> str:
    """
    Listen to microphone input and convert speech to text.
    
    Returns:
        The recognized speech as text
    """
    try:
        with sr.Microphone() as source:
            print("🎤 Listening...")
            recognizer.adjust_for_ambient_noise(source, duration=1)
            audio = recognizer.listen(source, timeout=10)
        
        print("🔄 Processing...")
        text = recognizer.recognize_google(audio)
        print(f"You: {text}")
        return text
    except sr.UnknownValueError:
        error_msg = "Sorry, I didn't catch that. Could you repeat?"
        speak(error_msg)
        return None
    except sr.RequestError as e:
        error_msg = f"Error with speech recognition service: {str(e)}"
        speak(error_msg)
        return None
    except Exception as e:
        error_msg = f"Error: {str(e)}"
        speak(error_msg)
        return None

def chat_with_jarvis(user_message: str) -> str:
    """
    Send a message to Jarvis AI and get a response.
    
    Args:
        user_message: The message to send to the AI
        
    Returns:
        The AI's response
    """
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are Jarvis, a helpful AI assistant. Keep responses short and concise (1-2 sentences)."},
                {"role": "user", "content": user_message}
            ],
            temperature=0.7,
            max_tokens=100
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"

def main():
    """Main function to run Jarvis AI voice chatbot."""
    print("=" * 50)
    print("🤖 JARVIS AI - VOICE MODE")
    print("=" * 50)
    print("Commands:")
    print("  • Speak naturally to chat")
    print("  • Say 'quit' or 'exit' to stop")
    print("=" * 50)
    
    # Welcome message
    speak("Hello! I'm Jarvis. How can I help you today?")
    
    while True:
        # Listen to user
        user_input = listen()
        
        if user_input is None:
            continue
        
        # Check for exit command
        if user_input.lower() in ['quit', 'exit', 'bye', 'goodbye']:
            speak("Goodbye! Have a great day!")
            print("👋 Exiting...")
            break
        
        # Get response from Jarvis
        print("🔄 Jarvis is thinking...")
        response = chat_with_jarvis(user_input)
        
        # Speak the response
        speak(response)
        print("-" * 50)

if __name__ == "__main__":
    main()
