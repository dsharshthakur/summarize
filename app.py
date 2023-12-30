
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.chains.summarize import load_summarize_chain
from langchain.text_splitter import  RecursiveCharacterTextSplitter
from langchain.docstore.document import Document
import streamlit as st

st.markdown("<h2 style = 'text-align:center'>Text Summarization</h2>", unsafe_allow_html = True)
user_text = st.text_area(label = "Copy paste the text here:" ,height = 200)

#key
key = st.secrets["PROJECT_KEY"]

#model
model = ChatGoogleGenerativeAI(model = "gemini-pro" , google_api_key = key)

def generate_response(text, language = None):
    #template
    if translatebtn == True:
        template = '''Translate the given text in {language}.The text is:\n{text}'''
        prompt = PromptTemplate(input_variables = ["text"], template = template)
    
    else:        
        template = '''You are a helpfull assistant that summarizes a large text in such a way that it can be easily understood by any user.Also add appropriate main heading.
        The text is :\n{text}'''
        prompt = PromptTemplate(input_variables = ["text"], template = template)

    docs = [Document(page_content = text)]
    
    #chain
    chain= load_summarize_chain(llm = model , chain_type="stuff" ,prompt = prompt, verbose = False)
    
    #generate
    response = chain.run(docs, language = language)
    
    return  response

st.markdown("<br>" , unsafe_allow_html = True)

col1 , col2 , col3 ,col4= st.columns(4)
with col2:
    generatebtn = st.button(label = "Summarize", use_container_width=True)
with col3:
    translatebtn = st.button(label = "Translate" , use_container_width = True)

if generatebtn:
    translatebtn = False 
    st.markdown("<h4>Response:</h4>", unsafe_allow_html = True)
    answer = generate_response(user_text)
    st.info(answer)
    st.write(f"You wrote {len(user_text)} characters.")

if translatebtn == True:
    generatebtn = False
    lang = st.text_input(label = "Enter the language to translate in.")
    answer = generate_response(user_text, lang)
    st.info(answer)
    
    
    

    
