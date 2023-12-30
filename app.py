
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


   
col1 , col2 , col3 = st.columns([0.1,0.8,0.1])
with col2:
    radio_btn = st.radio(label ="Choose an option:" ,options= ["Summarize","Translate"], horizontal = True)

submit_btn = st.button(label = "submit")


lang = None
if  radio_btn == "Summarize" and submit_btn == True:
   st.markdown("<h4>Response:</h4>", unsafe_allow_html = True)
   answer = generate_response(user_text)
   st.success(answer)
   st.write(f"You wrote {len(user_text)} characters.")

elif radio_btn == "Translate":
   lang = st.text_input(label = "Enter the language to translate in." , value = None)

if lang != None:
   try:
      st.markdown("<h4>Response:</h4>", unsafe_allow_html = True)
      answer = generate_response(user_text, lang)
      st.success(answer)
     
   except:
      st.warning("Cannot translate in this language.")
 
    

    
