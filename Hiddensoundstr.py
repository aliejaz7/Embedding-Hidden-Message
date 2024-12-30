import streamlit as st
import wave

def embed_message(audiofile, secret_message, outputfile):
    try:
        # Read the audio file
        waveaudio = wave.open(audiofile, mode='rb')
        frame_bytes = bytearray(list(waveaudio.readframes(waveaudio.getnframes())))

        # Prepare the secret message
        secret_message += int((len(frame_bytes) - (len(secret_message) * 8 * 8)) / 8) * '#'
        bits = list(map(int, ''.join([bin(ord(i)).lstrip('0b').rjust(8, '0') for i in secret_message])))

        # Modify the audio frames
        for i, bit in enumerate(bits):
            frame_bytes[i] = (frame_bytes[i] & 254) | bit
        frame_modified = bytes(frame_bytes)

        # Save the modified audio to a new file
        with wave.open(outputfile, 'wb') as fd:
            fd.setparams(waveaudio.getparams())
            fd.writeframes(frame_modified)
        waveaudio.close()
        return "Message successfully embedded!"
    except Exception as e:
        return f"Error: {str(e)}"

# Streamlit Interface
st.title("Audio Steganography: Secret Message Embedder")
st.write("Upload a WAV file, enter your secret message, and save the output as a new audio file.")

# File uploader for the input audio file
uploaded_file = st.file_uploader("Choose a WAV file", type=["wav"])

# Text input for the secret message
secret_message = st.text_input("Enter the secret message to embed:")

# File name input for the output file
output_file_name = st.text_input("Enter the output file name (with .wav extension):")

# Embed the secret message
if st.button("Embed Secret Message"):
    if uploaded_file and secret_message and output_file_name:
        with open("temp_input.wav", "wb") as f:
            f.write(uploaded_file.getbuffer())
        result = embed_message("temp_input.wav", secret_message, output_file_name)
        st.success(result)
        st.write(f"Output File Saved as: `{output_file_name}`")
    else:
        st.error("Please provide all inputs (WAV file, secret message, and output file name).")
