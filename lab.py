
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
  prompt="Lista:\n"+texto_quebrado+"\n'''\nClassificação do mais perigoso para o menos perigoso na lista:\n\n1.",
  temperature=0.7,
  max_tokens=150,
  top_p=1,
  frequency_penalty=0,
  presence_penalty=0,
  stop=["\n\n"]
)
        st.write("Resultado da classificação:")
        content = response.choices[0].text
        explicação0 = openai.Completion.create(
            engine="text-davinci-002",
            prompt="Lista:\n"+texto_quebrado+"\n'''\nClassificação do mais perigoso para o menos perigoso na lista:\n\n1. "+content+"\nExplicação: Bom,",
            temperature=0.7,
            max_tokens=150,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
            stop=["\n\n"])
        explicação = explicação0.choices[0].text
        st.write("1. "+content+".\n\nExplicação: "+explicação)



