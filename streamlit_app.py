import json
import streamlit as st
import pandas as pd
from streamlit.runtime.uploaded_file_manager import UploadedFile
from streamlit_pdf_viewer import pdf_viewer

from utils.model import process_file_with_gemini

def process_file_and_keyword(file: UploadedFile, keyword: list[str], api_key: str):

    """
    Process the uploaded file and text input.
    This is a placeholder function - replace with your actual processing logic.

    Args:
        file: UploadedFile object
        text: String from user input

    Returns:
        data
    """

    # Example processing
    prompt = "extract all the transactions as a json object."
    response_json = process_file_with_gemini(file, prompt, api_key)
    return json.loads(response_json)

# Set up the Streamlit app
st.title("File and Text Processing App")
st.write("Upload an file and enter text to process them together")

# Create file uploader and text input
uploaded_file = st.file_uploader("Choose an file...", type=["jpg", "jpeg", "png", "pdf"])

# user_text = st.text_area("Enter your keywords with new line as separator:", height=150, placeholder="THE H K JOCKEY CLUB\n自動轉帳\nAUTOPAY")
api_key = st.text_input("Enter API Key:", type="password")
key = api_key or st.secrets.get("GEMINI_API_KEY")
# Add regex validation for CSV format
# Simple CSV validation - checks if lines have consistent number of commas
# text_list = user_text.strip().split('\n')
# text_list = [text.strip() for text in text_list]
if uploaded_file is not None and key:
    # Process the inputs
    bytes_data = uploaded_file.getvalue()

    # Display the uploaded image
    st.subheader("Uploaded file:")
    if uploaded_file.type.startswith("application/pdf"):
        pdf_viewer(bytes_data, pages_to_render=[1])
    else:
        st.image(bytes_data, width=300)


    with st.status("Processing image and text..."):
        # Process the image and text
        result = process_file_and_keyword(uploaded_file, [], key)

        print(result)
        df_result = pd.DataFrame(result['transactions'])

        # Display the results
        st.subheader("Processing Results:")
        st.dataframe(df_result, hide_index=True)

    # You can customize the output display based on your specific needs
    # For example, if your function returns a processed image:
    # st.image(result_image, caption="Processed Image")
else:
    st.info("Please upload an file and enter text to see results")
