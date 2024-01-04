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

# set the page config

st.set_page_config(page_title='Gestura', page_icon=':sparkle:', layout='wide')

# url loader 

def url_loader(url):
    r = requests.get(url)
    if r.status_code !=200:
        return None
    return r.json()

# Home page sidebar

with st.sidebar:
    with st.container():
        i,j = st.columns((4,4))
        with i:
            st.empty()
        with j:
            st.empty()

    choose = option_menu(
        "Gestura Testing",
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
engine = pyttsx3.init()

# functions

def gesture_image(img):
    image = Image.open(img)
    out = image.save('sample.png')
    #st.image('sample.png')
    img_file = cv2.imread('sample.png')
    print(img_file)
    results = model(img_file)[0]
    for result in results.boxes.data.tolist():
        x1, y1, x2, y2, score, class_id = result
        word = classNames[int(class_id)]
        # translation = translator.translate(word, dest='ta')
        # output = translation.text
        # text_to_speech.say(word)
    return word

def convert_text_to_speech(text):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    engine.say(text)
    engine.runAndWait()

# Page navigations

if choose == "Home":

    st.markdown("<h1 style='text-align: center;'>Welcome to Gestura</h1>", unsafe_allow_html=True)


elif choose == "Image":

    st.title('For Images')

    upload_file = st.file_uploader("Upload an image", type=['jpg', 'png', 'jpeg', 'tiff'])

    if st.button('Convert') and upload_file is not None:

        st.image(upload_file)

        st.write(gesture_image(upload_file))

        #convert_text_to_speech(out)
        


        os.remove('sample.png')

elif choose == 'Video':

    st.title("Text to speech convertor")


    user_input = st.text_input('Enter the text')

    if st.button('Convert to speech') and user_input is not None:

        text = user_input

        # voices = text_to_speech.getProperty('voices')
        # text_to_speech.setProperty('voice', voices[1].id)

        engine.say(text)
        engine.runAndWait()
        
    




