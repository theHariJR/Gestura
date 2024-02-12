# install libraries

import streamlit as st
import streamlit_lottie as st_lottie
from streamlit_option_menu import option_menu
import cv2
from ultralytics import YOLO
import pyttsx3
from googletrans import Translator
import matplotlib.pyplot as plt
from PIL import Image
import requests
import os
import gtts as gt 
import pygame
from io import BytesIO

# set the page config

st.set_page_config(page_title='Gestura', page_icon=':hand:', layout='wide')

# url loader 

def url_loader(url):
    r = requests.get(url)
    if r.status_code !=200:
        return None
    return r.json()

# loading assests

front = url_loader('https://lottie.host/394eb195-2a7f-4d5c-bbdf-94bece89bccc/1M1kQXv8jc.json')
image = url_loader('https://lottie.host/d41d28f9-09f9-42c4-80ba-fd5d5a80e559/YOwqOelSQc.json')

# Home page sidebar

with st.sidebar:
    with st.container():
        i,j = st.columns((4,4))
        with i:
            st.empty()
        with j:
            st.empty()

    choose = option_menu(
        "Gestura",
        ["Home", "Image", "Video"],
        menu_icon="rocket",
        default_index=0,
        orientation= 'vertical'
    )

# model 

model = YOLO("sign_language.pt")

# class names

classNames = ['additional', 'alcohol', 'allergy', 'bacon', 'bag', 'barbecue', 'bill', 'biscuit', 'bitter', 'bread', 'burger', 'bye', 
              'cake', 'cash', 'cheese', 'chicken', 'coke', 'cold', 'cost', 'coupon', 'credit card', 'cup', 'dessert', 'drink', 'drive', 'eat', 
              'eggs', 'enjoy', 'fork', 'french fries', 'fresh', 'hello', 'hot', 'icecream', 'ingredients', 'juicy', 'ketchup', 'lactose', 'lettuce', 
              'lid', 'manager', 'menu', 'milk', 'mustard', 'napkin', 'no', 'order', 'pepper', 'pickle', 'pizza', 'please', 'ready', 'receipt', 'refill', 
              'repeat', 'safe', 'salt', 'sandwich', 'sauce', 'small', 'soda', 'sorry', 'spicy', 'spoon', 'straw', 'sugar', 'sweet', 'thank-you', 'tissues', 
              'tomato', 'total', 'urgent', 'vegetables', 'wait', 'warm', 'water', 'what', 'would', 'yoghurt', 'your']

# initializing

translator = Translator()


# functions

# def gesture_image(img):
#     image = Image.open(img)
#     out = image.save('sample.png')
#     img_file = cv2.imread('sample.png')
#     results = model(img_file)[0]
#     for result in results.boxes.data.tolist():
#         x1, y1, x2, y2, score, class_id = result
#         word = classNames[int(class_id)]
#         translation = translator.translate(word, dest='es')
#         print(translation.text)
#         output = translation.text
#         try:
#             # Initialize the engine only once
#             engine = pyttsx3.init()

#             # Check if the engine's run loop is not already running
#             if not engine._inLoop:
#                 voices = engine.getProperty('voices')
#                 engine.setProperty('voice', voices[0].id)
#                 engine.say(word)
#                 engine.runAndWait()
#             else:
#                 print("Text-to-speech run loop is already in progress. Wait until it finishes.")
#         except Exception as e:
#             print(f"Error during text-to-speech conversion: {e}")
#     return word

def new_gestura(img, language):
    image = Image.open(img)
    out = image.save('sample.png')
    img_file = cv2.imread('sample.png')
    results = model(img_file)[0]
    for result in results.boxes.data.tolist():
        x1, y1, x2, y2, score, class_id = result
        word = classNames[int(class_id)]
        translation = translator.translate(word, dest = language)
        print(translation.text)
        output = translation.text
        try:
            tts = gt.gTTS(text=output, lang=language)
            audio_bytes = BytesIO()
            tts.write_to_fp(audio_bytes)
            audio_bytes.seek(0)

            # Initialize pygame mixer
            pygame.mixer.init()
            pygame.mixer.music.load(audio_bytes)
            pygame.mixer.music.play()

        except Exception as e:
            print(f"Error during text-to-speech conversion: {e}")
    return word



# Page navigations

if choose == "Home":

    st.markdown("<h1 style='text-align: center;'>Welcome to Gestura</h1>", unsafe_allow_html=True)

    st.write('----')

    st.lottie(front, height=250, key='touch')

    st.markdown("""
                Gestura is an innovative project designed to enhance communication between individuals by leveraging the power of sign language. 
                The primary goal of Gestura is to detect sign language gestures and convert them into the user's native language, facilitating better 
                understanding and communication for diverse communities.
                By providing a bridge between sign language and spoken/written languages, Gestura empowers individuals to express themselves more freely and 
                participate in a broader range of conversations.
    """, unsafe_allow_html=True)

    #st.lottie(front, height=400, key='touch')


elif choose == "Image":

    st.title('For Images')

    st.lottie(image, height=200, key='image')

    upload_file = st.file_uploader("Upload an image", type=['jpg', 'png', 'jpeg', 'tiff'])

    audio = st.selectbox(label="Enter the Audio", options=['ta', 'en', 'hi', 'te'])

    if st.button('Convert') and upload_file is not None:

        st.image(upload_file)

        st.write(new_gestura(upload_file, audio))
        
        os.remove('sample.png')

elif choose == 'Video':

    st.title("Gestura video phase")

    audio = st.selectbox(label="Enter the Audio", options=['ta', 'en', 'hi', 'te'])

    if st.button(label='Start to capture') is not None:

        cap = cv2.VideoCapture(0)

        while True:

            ret, frame = cap.read()

            results = model(frame, show=True)[0]

            for result in results.boxes.data.tolist():
                x1, y1, x2, y2, score, class_id = result
                word = classNames[int(class_id)]
                translation = translator.translate(word, dest = 'ta')
                print(translation.text)
                output = translation.text
            
                try:
                    tts = gt.gTTS(text=output, lang='ta')
                    audio_bytes = BytesIO()
                    tts.write_to_fp(audio_bytes)
                    audio_bytes.seek(0)

                    # Initialize pygame mixer
                    pygame.mixer.init()
                    pygame.mixer.music.load(audio_bytes)
                    pygame.mixer.music.play()
                except Exception as e:
                    print(f"Error during text-to-speech conversion: {e}")

            #cv2.imshow('sample', frame)

            if cv2.waitKey(1) == ord('q'):
                break
        cap.release()
        cv2.destroyAllWindows()
        
    




