import streamlit as st
from transformers import MarianMTModel, MarianTokenizer
import gtts as gtts
import whisper
import tempfile 
# Charger le modèle de traduction FR -> EN
st.sidebar.title("Choix de la fonctionnalité")
st.sidebar.write("1 pour traduire du texte :")
st.sidebar.write("2 pour traduire de l'audio :")
choix = st.sidebar.radio("Sélectionnez une option :", (1, 2))

if choix == 1:
    @st.cache_resource
    def load_model():
        model_name = "Helsinki-NLP/opus-mt-fr-en"
        tokenizer = MarianTokenizer.from_pretrained(model_name)
        model = MarianMTModel.from_pretrained(model_name)
        return tokenizer, model

    tokenizer, model = load_model()

    # Interface utilisateur
    st.title(" Traduction Français --> Anglais")
    st.write("Tape une phrase en français")

    # Input utilisateur
    texte_fr = st.text_input(" Entrez une phrase en français :")

    if texte_fr:
        # Encoder
        tokens = tokenizer(texte_fr, return_tensors="pt")
        encoder_outputs = model.get_encoder()(**tokens)

        # Decoder
        generated_tokens = model.generate(**tokens)
        traduction = tokenizer.decode(generated_tokens[0], skip_special_tokens=True)

        # Résultats
        st.subheader("Résultat :")
        st.write(f"**Texte original :** {texte_fr}")
        st.write(f"**Traduction :** {traduction}")
        st.write(f" Sortie de l'encodeur : {encoder_outputs.last_hidden_state.shape}")
        if traduction != "":
            tts = gtts.gTTS(text=traduction, lang="en")
            tts_file = "synthese.mp3"
            tts.save(tts_file)
            st.audio(tts_file, format="audio/mp3")
elif choix == 2:
    audio_data = st.audio_input("Enregistrez votre message ")
    #traduction de l'audio
    if audio_data:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file:
            tmp_file.write(audio_data.read())
            temp_filename = tmp_file.name
        model = whisper.load_model("base")  # Choisir "tiny", "base", "small", "medium", "large"

        language = "en"
        result = model.transcribe(temp_filename, language=language)
        transcription = result["text"]
        if "text" in result:
            transcription = result["text"]
            result = model.transcribe(temp_filename, language='fr')
            transcription = result["text"]
        else:
            transcription = "Erreur : la transcription a échoué."

        st.subheader("Transcription")
        a=st.write(transcription)