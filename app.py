from dotenv import load_dotenv
import streamlit as st
from PyPDF2 import PdfReader


def main():
    # load api key
    load_dotenv()
    # design page
    st.set_page_config(page_title="Ask your PDF")
    st.header("Ask your PDF ☁️")

    # add uploader widget
    pdf = st.file_uploader("Upload your PDF", type="pdf")

    # extract text from pdf
    if pdf:
        # create new pdf reader
        pdf_reader = PdfReader(pdf)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()

        st.write(text)

if __name__ == "__main__":
    main()
