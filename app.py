
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.chains.summarize import load_summarize_chain
from langchain.text_splitter import  RecursiveCharacterTextSplitter
from langchain.docstore.document import Document
import streamlit as st


st.markdown("<h2 style = 'text-align:center'>TranscribeMate</h2>", unsafe_allow_html = True)


st.markdown("<br>" , unsafe_allow_html = True)
st.markdown("<br>" , unsafe_allow_html = True)

user_text = st.text_area(label = "Copy paste the text here:" ,height = 200, value = " " )

#key
key = st.secrets["PROJECT_KEY"]

#model
model = ChatGoogleGenerativeAI(model = "gemini-pro" , google_api_key = key)

def generate_response(text, language = None):
    #template
    if language != None       :
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
    response = chain.run({"input_documents":docs, "language" : language})
    
    return  response

st.markdown("<br>" , unsafe_allow_html = True)


   
col1 , col2 , col3 = st.columns([0.32,0.36,0.32])
with col2:
    radio_btn = st.radio(label ="Choose an option:" ,options= ["Summarize","Translate"], horizontal = True)

st.markdown("<br>", unsafe_allow_html = True)
   
col1 , col2 , col3 = st.columns(3)
with col2:
   submit_btn = st.button(label = "submit", use_container_width = True)
    

st.markdown("<br>", unsafe_allow_html = True)

lang = None
if  radio_btn == "Summarize" and submit_btn == True and user_text != " ":
   st.markdown("<h4>Response:</h4>", unsafe_allow_html = True)
   answer = generate_response(user_text)
   st.success(answer)
   st.write(f"You wrote {len(user_text)} characters.")

elif radio_btn == "Translate" and user_text != " ":
   lang = st.text_input(label = "Enter the language to translate in." , value = None)

if lang != None:
   try:
      st.markdown("<h4>Response:</h4>", unsafe_allow_html = True)
      answer = generate_response(user_text, lang)
      st.success(answer)
     
   except:
      st.warning("Cannot translate in this language.")
 
    

    
