import streamlit as st
import gtts as gtts
import whisper
import tempfile

#petit = st.audio_input("Enregistrer un audio")
#if petit:
    #petit.save("output3.mp3")
    #st.audio("output3.mp3", format="audio/mp3")
    #model = whisper.load_model("base")
    #result = model.transcribe(petit)
    #print(result["text"])
    
    
    # 1️⃣ Capture audio
audio_data = st.audio_input("Enregistrez votre message ")

if audio_data:
    # 2️⃣ Sauvegarde temporaire
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_file:
        tmp_file.write(audio_data.read())
        temp_filename = tmp_file.name

    st.write(" Audio enregistré, transcription en cours...")

    # 3️⃣ Chargement du modèle Whisper
    model = whisper.load_model("base")  # Choisir "tiny", "base", "small", "medium", "large"

    language = "fr"

    # 4️⃣ Transcription
    result = model.transcribe(temp_filename, language=language)
    transcription = result["text"]
    if "text" in result:
        transcription = result["text"]
    else:
        transcription = "Erreur : la transcription a échoué."

    # 5️⃣ Affichage
    st.subheader("Transcription")
    st.write(transcription)
    
    if transcription.strip() != "":
        tts = gtts.gTTS(text=transcription, lang="fr")
        tts_file = "synthese.mp3"
        tts.save(tts_file)

