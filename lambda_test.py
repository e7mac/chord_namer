import requests
import base64
import os

# Replace with your actual API Gateway URL
API_URL = "https://rcu2rwskvezrt52cpnr6zz4iye0wsdst.lambda-url.us-east-1.on.aws/"

file_path = './samples/Title_Theme_-_Ocarina_of_Time.mxl'

# Read the file in binary mode
with open(file_path, 'rb') as file:
    musicxml_content = file.read()

# Encode the MusicXML content
encoded_content = base64.b64encode(musicxml_content).decode()

# Make the request to the API
response = requests.post(API_URL, json={'body': encoded_content, 'isBase64Encoded': True})

# Check the response
if response.status_code == 200:
    # Decode the response content
    decoded_content = base64.b64decode(response.json()['body'])
    
    # Save the received content to a new file
    output_path = os.path.join(os.path.dirname(file_path), 'output_musicxml.mxl')
    with open(output_path, 'wb') as output_file:
        output_file.write(decoded_content)
    
    print(f"Success! Received MusicXML content saved to: {output_path}")
else:
    print(f"Error: {response.status_code}")
    print(response.text)
