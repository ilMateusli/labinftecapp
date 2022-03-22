
import streamlit as st
import os
import openai

openai.api_key = ""

st.title("Labinftec APP - Classificador")
texto = st.text_area("Coloque os ítens aqui", "")
keyopenai = st.text_input("Coloque a chave da OpenAI aqui", "")

if keyopenai != "":
    openai.api_key = keyopenai

texto_quebrado = texto.replace(',', '\n')
if st.button("Classificar"):
    if texto == "":
        st.write("Você precisa inserir os ítens na caixa de texto.")
    else: 
        response = openai.Completion.create(
  engine="text-davinci-002",
  prompt="Lista:\n"+texto_quebrado+"\n'''\nFale sobre as características do vírus da lista (envelope, diametro, se é RNA ou DNA, sua replicação, informações do genoma.):\n\n Bom.",
  temperature=0.7,
  max_tokens=200,
  top_p=1,
  frequency_penalty=0,
  presence_penalty=0,
  stop=["\n\n"]
)
        st.write("Resultado da classificação:")
        content = response.choices[0].text
        explicação0 = openai.Completion.create(
            engine="text-davinci-002",
            prompt="Lista:\n"+texto_quebrado+"\n'''\nDescreva os vírus da lista:\n\n"+content+"\nExplique os detalhes técnicos: Bom,",
            temperature=0.7,
            max_tokens=200,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
            stop=["\n\n"])
        explicação = explicação0.choices[0].text
        st.write(content+".\n\nExplicação: "+explicação)



