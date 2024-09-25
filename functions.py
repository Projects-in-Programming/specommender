import json
import cv2
import os
from inference_sdk import InferenceHTTPClient
from scrapper import get_items_by_face_type
import pandas as pd
import ast
import random

# Read the API key from the secrets.json file
def read_api_key(file_path):
    with open(file_path, 'r') as f:
        secrets = json.load(f)
    return secrets.get('api', {}).get('api_key')

model_api_key = read_api_key('secrets.json')

def search_results(num_pages):
    # Open the camera to take a picture
    cam = cv2.VideoCapture(0)

    if not cam.isOpened():
        return "Could not open camera"

    # Set the resolution for a portrait image (e.g., 480x640 for a 3:4 aspect ratio)
    cam.set(cv2.CAP_PROP_FRAME_WIDTH, 480)
    cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 640)

    print("Press 'Space' to capture the image or 'q' to quit.")

    while True:
        ret, frame = cam.read()

        if not ret:
            return "Failed to capture image"

        # Display the captured frame
        cv2.imshow("Capture Image", frame)

        # Wait for a key press
        key = cv2.waitKey(1)

        # If the spacebar is pressed, capture the image
        if key == 32:  # Spacebar key code
            # Save the captured image to a file
            captured_image_path = "captured_image.jpg"
            cv2.imwrite(captured_image_path, frame)
            break

        # If 'q' is pressed, quit the loop
        elif key == ord('q'):
            return "Image capture cancelled by the user"

    # Release the camera after capturing the image
    cam.release()
    cv2.destroyAllWindows()

    # Initialize the InferenceHTTPClient with the API URL and key
    CLIENT = InferenceHTTPClient(
        api_url="https://detect.roboflow.com",
        api_key=model_api_key  # Replace with your actual API key
    )

    # Perform inference on the captured image
    result = CLIENT.infer(captured_image_path, model_id="face-shape-detection/1")
    print(result)

    # Delete the captured image after inference
    os.remove(captured_image_path)

    # Extract the predicted face shape from the result
    class_name = result['predictions'][0]['class']

    # if no class is predicted, pick a random number between 0 and 5
    classes = ['heart', 'oval', 'round', 'square', 'triangle']
    if not class_name:
        i = random.randint(0, 5) # pick a random number between 0 and 5
        class_name = classes[i]

    # Prepare the message based on the prediction
    message = f"Detected face shape: {class_name} \n Here are the best suited glasses for you ....."

    # Get the items based on the predicted face shape
    items = get_items_by_face_type(class_name,num_pages)
    return class_name

def clean_data(file_name):
    ''' function to clean the data and save it to a new csv file '''

    df = pd.read_csv(file_name)

    # cleaning the price column, converting it to number and putting currency in different column
    df['Price'] = df['Price'].str.replace('$', '').str.replace(',', '').astype(float)
    df['Currency'] = '$'

    #print(df.shape)

    # convert the colors column to list of colors
    df['Colors'] = df['Colors'].apply(ast.literal_eval)

    # use dummise to get the colors as dummies
    colors_dummies = pd.get_dummies(df['Colors'].apply(pd.Series).stack()).groupby(level=0).max()

    # concatinate the dummy columns back to the original dataframe
    df = pd.concat([df, colors_dummies], axis=1)

    #print(df.shape)

    # drop the colors column
    df.drop('Colors', axis=1, inplace=True)

    # check for nan values in the dataframe
    print("Number of null values in the dataset:", df.isnull().sum())

    # drop the rows with nan values
    df.dropna(inplace=True)

    # saving the cleaned data to a new csv file
    cleaned_file_name = 'cleaned_' + file_name
    df.to_csv(cleaned_file_name, index=False)

    return df




