import streamlit as st 
from lida import Manager, TextGenerationConfig , llm  
from dotenv import load_dotenv
import os
import openai
from PIL import Image
from io import BytesIO
import base64

load_dotenv()
# openai.api_key = os.getenv('OPENAI_API_KEY')

def base64_to_image(base64_string):
    # Decode the base64 string
    byte_data = base64.b64decode(base64_string)
    
    # Use BytesIO to convert the byte data to image
    return Image.open(BytesIO(byte_data))


textgen_config = TextGenerationConfig(n=1, temperature=0.5, model="gpt-3.5-turbo-0301", use_cache=True)
# st.session_state.OPENAI_API_KEY = ""

openaiKey = st.sidebar.text_input('OpenAI Key', '')
# os.environ["OPENAI_API_KEY"] = openaiKey
if st.button("Start Session") or 'OPENAI_API_KEY' in st.session_state:
    st.session_state.OPENAI_API_KEY = openaiKey
    lida = Manager(text_gen = llm("openai"))
    menu = st.sidebar.selectbox("Choose an Option", ["Summarize", "Question based Graph"])

    if menu == "Summarize":
        st.subheader("Summarization of your Data")
        file_uploader = st.file_uploader("Upload your CSV", type="csv")
        persona = st.text_input('Persona', '')
        if file_uploader is not None and persona:
            path_to_save = "filename.csv"
            with open(path_to_save, "wb") as f:
                f.write(file_uploader.getvalue())
                

            summary = lida.summarize("filename.csv", summary_method="default",textgen_config=textgen_config)
            st.write(summary)

            goals = lida.goals(summary, n=5, textgen_config=textgen_config, persona=persona)
            for goal in goals:
                st.write(goal)
            i = 0
            library = "seaborn"
            textgen_config = TextGenerationConfig(n=1, temperature=0.2, use_cache=True)
            charts = lida.visualize(summary=summary, goal=goals[i], textgen_config=textgen_config, library=library)  
            print(charts)
            if(charts[0]):
                img_base64_string = charts[0].raster
                img = base64_to_image(img_base64_string)
                st.image(img)
            else:
                st.write("Error in generating chart")


                
        elif menu == "Question based Graph":
            charts=''
            st.subheader("Query your Data to Generate Graph")
            file_uploader = st.file_uploader("Upload your CSV", type="csv")
            if file_uploader is not None:
                path_to_save = "filename1.csv"
                with open(path_to_save, "wb") as f:
                    f.write(file_uploader.getvalue())
                text_area = st.text_area("Query your Data to Generate Graph", height=200)
                if st.button("Generate Graph"):
                    if len(text_area) > 0:
                        st.info("Your Query: " + text_area)
                        lida = Manager(text_gen = llm("openai")) 
                        textgen_config = TextGenerationConfig(n=1, temperature=0.2, use_cache=True)
                        summary = lida.summarize("filename1.csv", summary_method="default", textgen_config=textgen_config)
                        user_query = text_area
                        charts = lida.visualize(summary=summary, goal=user_query, textgen_config=textgen_config)  
                        # charts[0]
                        print(charts)
                        if(charts):
                            image_base64 = charts[0].raster
                            img = base64_to_image(image_base64)
                            st.image(img)
                        else:
                            st.write("Error in generating chart")
                        instruction = st.text_area("Instructions for editing the chart", height=200)   
                        instruction_arr = instruction.split(",") #["change color as red for CA location", "change color as blue for NY location"]
                                
                        if st.button("Regenerate Graph"):
                            # if len(instruction_arr) > 0:
                                print("Regenerating")
                                textgen_config = TextGenerationConfig(n=1, temperature=0.2, use_cache=True)
                                summary = lida.summarize("filename1.csv", summary_method="default", textgen_config=textgen_config)
                                print(charts)
                                print(textgen_config)
                                e_charts = lida.edit(code=charts[0]['code'],  summary=summary, instructions=instruction_arr, library="seaborn", textgen_config=textgen_config)
                                charts = e_charts
                                image_base64 = charts[0].raster
                                img = base64_to_image(image_base64)
                                st.image(img)
                                        


