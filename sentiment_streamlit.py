import requests
import streamlit as st
from loguru import logger

logger.add("logs/sentiment_streamlit.log", rotation="500 MB", level="INFO")

API_URL = "http://127.0.0.1:8000"

st.title("Analyse de sentiment")

with st.form('form'):
    text = st.text_area("Saisir votre texte pour analyser le sentiment")
    submit = st.form_submit_button("Analyser")

if submit:
    if not text:
        st.error("Vous devez saisir un texte à analyser")
    else:
        logger.info(f"Analyse : {text}")

        try:
            payload = {
                "text": text
            }

            url = f"{API_URL}/analyse_sentiment/"
            response = requests.post(url, json=payload)

            if response.status_code == 200:
                results = response.json()
                logger.success(f"Résultats API pour le texte : {text}. {results}")

                st.subheader("Résultats")
                st.write(f"neg : {results['neg']}")
                st.write(f"neu : {results['neu']}")
                st.write(f"pos : {results['pos']}")
                st.write(f"compound : {results['compound']}")

                if results['compound'] >= 0.05:
                    st.write("Sentiment global : Positif")
                elif results['compound'] <= -0.05:
                    st.write("Sentiment global : Négatif")
                else:
                    st.write("Sentiment global : Neutre")

            else:
                st.error(f"Erreur API : {response.text}")
                logger.error(f"Erreur analyse API pour le texte : {text}. {response.text}")
        except Exception as e:
            st.error(f"Une erreur est survenue : {e}")
            logger.error(f"Erreur analyse pour le texte : {text}. {e}")
