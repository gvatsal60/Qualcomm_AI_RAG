import asyncio
import streamlit as st
import os
import shutil
from langchain_community.vectorstores import Chroma
from imagine.langchain import ImagineEmbeddings
from imagine.langchain import ImagineChat
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import re
import glob
from crawl4ai import AsyncWebCrawler
from langchain.docstore.document import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
import time
import sys
from dotenv import load_dotenv
from pathlib import Path

load_dotenv(Path("cfg/keys.env"))

# Load API key from environment variable
os.environ['IMAGINE_API_KEY'] = os.getenv('IMAGINE_API_KEY', '')
os.environ['IMAGINE_API_ENDPOINT'] = os.getenv(
    'IMAGINE_API_ENDPOINT', 'https://cloudai.cirrascale.com/apis/v2')

# Set the event loop policy for Windows
if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())


#############################################
# Utility functions
def is_same_domain(base_url, new_url):
    return urlparse(base_url).netloc == urlparse(new_url).netloc


def sanitize_filename(url):
    return re.sub(r'[^\w\-_\.]', '_', url)


# Function to perform crawling
async def crawl_website(url):
    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(
            url=url,
        )
        return result.markdown


def extract_links(markdown_text):
    # Regular expression to match markdown links
    link_pattern = r'\[([^\]]+)\]\((https?://[^\s)]+)\)'

    # Find all matches in the markdown text
    links = re.findall(link_pattern, markdown_text)

    cleaned_links = []
    for text, link in links:
        link = link.replace("<", "")
        link = link.replace(">", "")
        cleaned_links.append((text, link))

    # Return a list of tuples containing (text, url)
    return cleaned_links


def crawl_and_save_docs(url, set_name, visited=None, max_depth=0, depth=0, output_dir=".docs", max_urls=20):
    if visited is None:
        visited = set()
    if depth > max_depth or len(visited) >= max_urls:
        return
    if url in visited:
        return
    visited.add(url)

    # Create a placeholder to display the current URL
    with st.empty():
        st.info(f"**Crawling**: {url}")
        print(f'Crawling :{url}')
        try:
            res = asyncio.run(crawl_website(url))
            filename = sanitize_filename(url)+".md"
            file_path = os.path.join(output_dir, set_name, filename)
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, 'w', encoding="utf-8") as f:
                f.write(f"# URL : {url}\n\n{res}")
            for _, link in extract_links(res):
                # Only follow if it's the same domain
                if is_same_domain(url, link):
                    crawl_and_save_docs(link, set_name, visited=visited, max_depth=max_depth,
                                        depth=depth+1, output_dir=output_dir, max_urls=max_urls)
        except Exception as e:
            st.error(f"Error crawling {url}: {str(e)}")


def load_and_chunk_docs(docs_dir=".docs", chunk_size=1000, chunk_overlap=100):
    md_files = glob.glob(os.path.join(docs_dir, "**", "*.md"), recursive=True)
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size, chunk_overlap=chunk_overlap
    )
    all_docs = []
    for md_file in md_files:
        with open(md_file, "r", encoding="utf-8") as f:
            raw_text = f.read()
        metadata = {"source": md_file}
        for chunk in text_splitter.split_text(raw_text):
            doc = Document(page_content=chunk, metadata=metadata)
            all_docs.append(doc)
    return all_docs


def create_vector_store(docs, collection_name, batch_size=100):
    embeddings = ImagineEmbeddings()
    collection_dir = os.path.join(".vectordb", collection_name)

    # Create the collection first
    vectordb = Chroma(embedding_function=embeddings,
                      persist_directory=collection_dir, collection_name=collection_name)

    # Add documents in batches with progress bar
    total_docs = len(docs)
    progress_bar = st.progress(0)
    for i in range(0, total_docs, batch_size):
        batch = docs[i:i + batch_size]
        vectordb.add_documents(batch)
        progress_bar.progress((i + len(batch)) / total_docs)

    vectordb.persist()
    return vectordb


def create_rag_chain(vectordb):
    llm = ImagineChat(model="Llama-3.1-8B", temperature=0.0, max_tokens=2000)
    memory = ConversationBufferMemory(
        memory_key="chat_history", return_messages=True, output_key='answer')
    qa = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectordb.as_retriever(search_kwargs={"k": 3}),
        memory=memory,
        output_key='answer',
        return_source_documents=True
    )
    return qa


def clean_cache_and_files():
    st.session_state.pop("qa_chain", None)
    if os.path.exists(".docs"):
        shutil.rmtree(".docs")
    if os.path.exists('.vectordb'):
        shutil.rmtree('.vectordb')
    st.session_state.pop("vectordb", None)
    st.success("Cache, docs folder, and vectordb have been cleaned!")


def get_available_collections():
    vectordb_dir = ".vectordb"
    if os.path.exists(vectordb_dir):
        return [d for d in os.listdir(vectordb_dir) if os.path.isdir(os.path.join(vectordb_dir, d))]
    return []

#############################################
# Streamlit UI
#############################################


def rag_with_docs():
    st.title("Recursive Doc Crawler + RAG Demo")
    # Step 1: Provide a URL and a button to crawl/index
    with st.expander("1) Provide URL to Crawl & Build Index"):
        user_url = st.text_input("Enter the documentation URL:", value="")
        set_name = st.text_input(
            "Enter a name for this set of documents:", value="")

        # max_depth = st.slider("Max Depth", min_value=2, max_value=7, value=2)
        # max_urls = st.slider("Max URLs to Scrape", min_value=20, max_value=100, value=20)
        if st.button("Start Crawling and Indexing"):
            if user_url and set_name:
                # Check if the set_name already exists
                if os.path.exists(os.path.join(".docs", set_name)):
                    st.error(
                        f"The set name '{set_name}' already exists. Please choose a different name.")
                else:
                    # Clear old docs if any
                    crawl_and_save_docs(user_url, set_name,
                                        max_depth=0, max_urls=20)
                    # Load + chunk
                    docs = load_and_chunk_docs(docs_dir=".docs")
                    # Create vector store
                    vectordb = create_vector_store(
                        docs, collection_name=set_name)
                    # Save vectordb to a session state so we can use in Step 2
                    st.session_state["vectordb"] = vectordb
                    st.success("Crawling & Indexing Complete!")

    available_collections = get_available_collections()
    if available_collections:
        st.header("Chat with your Docs")
        selected_collection = st.selectbox(
            "Select a document set to chat with:", available_collections)
        if selected_collection:
            collection_dir = os.path.join(".vectordb", selected_collection)
            if os.path.exists(collection_dir):
                vectordb = Chroma(embedding_function=ImagineEmbeddings(
                ), persist_directory=collection_dir, collection_name=selected_collection)
                qa_chain = create_rag_chain(vectordb)
                st.session_state["qa_chain"] = qa_chain
            else:
                st.error(
                    f"Collection directory for '{selected_collection}' does not exist.")

        if prompt := st.chat_input("Ask a question about the docs"):
            # Initialize the messages list in session state if it doesn't exist
            if "messages" not in st.session_state:
                st.session_state.messages = []

            # Add the user's question to the messages list
            st.session_state.messages.append(
                {"role": "user", "content": prompt})

            # Display all previous messages
            for message in st.session_state.messages:
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])

            # Get the response from the RAG chain
            if "qa_chain" in st.session_state:
                response = st.session_state["qa_chain"]({"question": prompt})
                answer = response["answer"]

                # Add the assistant's response to the messages list
                st.session_state.messages.append(
                    {"role": "assistant", "content": answer})

                # Display the assistant's response
                with st.chat_message("assistant"):
                    st.write(answer, unsafe_allow_html=True)
            else:
                st.error("Please select a document set and try again.")
    else:
        st.info(
            "No document sets available. Please crawl and index a document set first.")
