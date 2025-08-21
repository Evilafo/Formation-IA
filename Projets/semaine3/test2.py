import streamlit as st
from transformers import MarianMTModel, MarianTokenizer
import gtts as gtts
import whisper
import tempfile 
# Charger le modèle de traduction FR -> EN
st.sidebar.title("fonctionnalité")
st.sidebar.write("1 pour texte :")
st.sidebar.write("2 pour audio :")
choix = st.sidebar.radio("selection :", (1, 2))

if choix == 1:
    @st.cache_resource
    def load_model():
        model_name = "Helsinki-NLP/opus-mt-en-fr"
        tokenizer = MarianTokenizer.from_pretrained(model_name)
        model = MarianMTModel.from_pretrained(model_name)
        return tokenizer, model

    tokenizer, model = load_model()

    # Interface utilisateur
    st.title(" traduction anglais --> français")
    st.write("écrit une phrase en anglais")

    # Input utilisateur
    texte_en = st.text_input(" Entrez une phrase en anglais :")

    if texte_en:
        # Encoder
        tokens = tokenizer(texte_en, return_tensors="pt")
        encoder_outputs = model.get_encoder()(**tokens)

        # Decoder
        generated_tokens = model.generate(**tokens)
        traduction = tokenizer.decode(generated_tokens[0], skip_special_tokens=True)

        # Résultats
        st.subheader("Résultat :")
        st.write(f"**texte original :** {texte_en}")
        st.write(f"**Traduction :** {traduction}")
        st.write(f" Sortie de l'encodeur : {encoder_outputs.last_hidden_state.shape}")
        if traduction != "":
            tts = gtts.gTTS(text=traduction, lang="fr")
            tts_file = "synthese.mp3"
            tts.save(tts_file)
            st.audio(tts_file, format="audio/mp3")
elif choix == 2:
    audio_data = st.audio_input("entrez votre audio :")
    #traduction de l'audio
    if audio_data:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file:
            tmp_file.write(audio_data.read())
            temp_filename = tmp_file.name
        model = whisper.load_model("base")  # Choisir "tiny", "base", "small", "medium", "large"

        language = "fr"
        result = model.transcribe(temp_filename, language=language)
        transcription = result["text"]
        if "text" in result:
            transcription = result["text"]
            result = model.transcribe(temp_filename, language='en')
            transcription = result["text"]
        else:
            transcription = "Erreur : la transcription a échoué."

        st.subheader("Transcription")
        a=st.write(transcription)