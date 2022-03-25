import streamlit as st
import os
import openai
import re
import urllib.request
from PIL import Image

openai.api_key = ""

st.title("Labinftec APP - Detalhar")
texto = st.text_area("Escreva sintomas causados por algum vírus, ou o nome dele.", "")
keyopenai = st.text_input("Coloque a chave da OpenAI aqui", "")

if keyopenai != "":
    openai.api_key = keyopenai

texto_quebrado = texto.replace(',', '\n')
if st.button("Detalhar"):
    if texto == "":
        st.write("Você precisa escrever algo na caixa de texto.")
    else: 
        response = openai.Completion.create(
  engine="text-davinci-002",
  prompt="Lista:\n"+texto_quebrado+"\n'''\nFale sobre as características do vírus da lista (nome científico ou a qual família pertence, envelope, diametro, se é RNA ou DNA, sua replicação, informações do genoma, em qual hospedeiro parasita - animais, planta, bacterias, fungos etc, qual sua classe/tamanho), se for sintomas, escolha o vírus que mais se aproxima aos sintomas dados na lista e mostre os motivos da escolha:\n\n Bom.",
  temperature=0,
  max_tokens=200,
  top_p=1,
  frequency_penalty=0,
  presence_penalty=0,
  stop=["\n\n\n"]
)

        st.write("Detalhes obtidos:")
        texto = response.choices[0].text
        padrao = re.compile(r'\w+[dae]$')
        familia = padrao.findall(texto)
        link = 'https://www.gettyimages.com.br/fotos/' #-
        link2 ='-virus?assettype=image&phrase'

        def pesquisar(familia):
            url = link + familia + link2
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            html = urllib.request.urlopen(req).read()

            for i in re.findall(r'<img.*?src="(.*?)"', str(html)):
                if i.startswith('http') and not i.endswith('.gif'):
                    urllib.request.urlretrieve(i, 'imagem.jpg')
                    break
        texto = response.choices[0].text
        if len(familia) == 0:
            st.write("Não foi possível encontrar uma imagem para mostrar.")
        else:
            pesquisar(familia[0])
            st.image('imagem.jpg', use_column_width=True)
            os.remove('imagem.jpg')
            st.write("Imagem do vírus encontrado pela internet.")
            
        content = response.choices[0].text
        explicação0 = openai.Completion.create(
            engine="text-davinci-002",
            prompt="Lista:\n"+texto_quebrado+"\n'''\nDescreva os vírus da lista:\n\n"+content+"\nCite vírus relacionado e explique: Além desse,",
            temperature=0.7,
            max_tokens=200,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0,
            stop=["\n\n"])
        explicação = explicação0.choices[0].text
        st.write(content+".\n\n"+"Além desse,"+explicação)
        st.write("[Você não pode confiar 100% nessa resposta. O programa ainda está em fase de desenvolvimento e pode conter erros.]")
