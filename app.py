from dotenv import load_dotenv
import streamlit as st
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI
from loguru import logger
from langchain.callbacks import get_openai_callback

loguru_logger = logger
loguru_logger.add("logs.log", rotation="500 MB")

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
        # read pdf
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()

        # split text into chunks
        text_splitter = CharacterTextSplitter(
            separator="\n",
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len
        )
        chunks = text_splitter.split_text(text)

        # create embeddings
        embeddings = OpenAIEmbeddings()

        # create knowledge base
        knowledge_base = FAISS.from_texts(chunks, embeddings)

        # show user input
        user_question = st.text_input("Ask a question to the PDF")
        if user_question:
            docs = knowledge_base.similarity_search(user_question)

            # log content of each doc
            for doc in docs:
                logger.info(doc)

            llm = OpenAI()
            chain = load_qa_chain(llm, chain_type="stuff")
            with get_openai_callback() as cb:
                response = chain.run(input_documents=docs, question=user_question)
                logger.info(response)
                logger.info(cb)

            st.write(response)




if __name__ == "__main__":
    main()
