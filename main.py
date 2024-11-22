import streamlit as st
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.embeddings import HuggingFaceInstructEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.llms import HuggingFaceHub
from sentence_transformers import SentenceTransformer
from langchain_community.vectorstores import FAISS

from langchain.memory import ConversationBufferMemory
from langchain.chains import conversational_retrieval
from htmlTemplates import css,bot_template,user_template

# model = INSTRUCTOR('hkunlp/instructor-xl')
from sentence_transformers import SentenceTransformer


def get_vectorstore(text_chunks):
    # Correctly load the INSTRUCTOR model
    model = SentenceTransformer("hkunlp/instructor-xl")

    # Generate embeddings for each chunk
    embeddings = [model.encode(chunk) for chunk in text_chunks]

    # Create FAISS index from text and embeddings
    vectorstore = FAISS.from_texts(texts=text_chunks, embeddings=embeddings)
    return vectorstore



# def get_vectorstore(text_chunks):
#     # embeddings = OpenAIEmbeddings()
#     embeddings = HuggingFaceInstructEmbeddings(model_name="hkunlp/instructor-xl")
#     vectorstore = FAISS.from_texts(texts=text_chunks, embedding=embeddings)
#     return vectorstore


def get_pdf_text(uploaded_file):
    text = ""  # Initialize an empty string for the text
    for pdf in uploaded_file:  # Loop through each uploaded PDF
        pdfreader = PdfReader(pdf)  # Initialize a PdfReader object for each PDF
        for page in pdfreader.pages:  # Loop through each page
            text += page.extract_text()  # Append extracted text, handle None
    return text

def get_text_chunks(text):
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,  # Maximum chunk size in characters
        chunk_overlap=200  # Overlap between chunks
    )
    chunks = text_splitter.split_text(text)  # Correctly call the split_text method
    return chunks

def get_conversation_chain(vectorstore):
    # llm  = ChatOpenAI(
    llm = HuggingFaceHub(repo_id="google/flan-t5-xxl", model_kwargs={"temperature":0.5, "max_length":512})
    memory = ConversationBufferMemory(memory_key="chat_history",return_messages=True)
    conversation_chain = conversational_retrieval.from_llm(
        llm=llm,
        retriever = vectorstore.as_retriever(),
        memory=memory
    )
    return conversation_chain

def handle_user_input(user_question):
    response = st.session_state.conversation({"question": user_question})
    st.session_state.chat_history =response["chat_history"]

    for i, message in enumerate(st.session_state.chat_history):
        if i % 2 == 0:
            st.write(user_template.replace("{{MSG}}",message.content),unsafe_allow_html=True)
        else:
            st.write(bot_template.replace("{{MSG}}",message.content),unsafe_allow_html=True)
    
    
def main():
    load_dotenv()
    st.set_page_config(page_title="Chat with multiple PDFs", page_icon=":book:")
    st.write(css,unsafe_allow_html=True)

    if "conversation" not in st.session_state:
        st.session_state.conversation = None  # Initialize the conversation state
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = None  # Initialize the conversation state

    st.header("Chat with multiple PDFs :books:")
    user_question=st.text_input("Ask a question about your documents")
    if user_question:
        handle_user_input(user_question)
    st.write(user_template.replace("{{MSG}}","Hello Robot"),unsafe_allow_html=True)
    st.write(bot_template.replace("{{MSG}}","Hello Human"),unsafe_allow_html=True)
    
    with st.sidebar:
        st.subheader("Your documents")
        uploaded_file = st.file_uploader("Upload your PDF files here and click on Process", accept_multiple_files=True)

        if st.button("Process"):
            if uploaded_file:  # Check if files are uploaded
                with st.spinner("Processing"):
                    raw_text = get_pdf_text(uploaded_file)  # Get text from PDFs
                    text_chunks = get_text_chunks(raw_text)  # Get text chunks
                    st.write(text_chunks)  # Display the chunks
                    # Here you can add code to create a vector store if needed
                    vector_store =get_vectorstore(text_chunks)
                    st.write(vector_store)
                    #create conversation chain
                    st.session_state.conversation = get_conversation_chain(vector_store) #takes history of the convo and returns the next element  
                
if __name__ == "__main__":
    main()