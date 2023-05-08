from dotenv import load_dotenv
import os
import streamlit as st


def main():
    # load api key
    load_dotenv()
    # design page
    st.set_page_config(page_title="Ask your PDF")
    st.header("Ask your PDF ☁️")

    # add uploader widget
    pdf = st.file_uploader("Upload your PDF", type="pdf")



if __name__ == "__main__":
    main()
