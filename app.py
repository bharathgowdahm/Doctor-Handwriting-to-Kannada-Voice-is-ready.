import streamlit as st
st.set_page_config(page_title="Doctor Kannada + AI Search", page_icon="💊", layout="wide")

lang = st.sidebar.selectbox("Language / ಭಾಷೆ", ["ಕನ್ನಡ", "English"])
def t(en, kn): return kn if lang=="ಕನ್ನಡ" else en

# AI Knowledge Base for common medicines in Karnataka
MED_KB = {
    "paracetamol": {"en": "For fever and pain. Reduces fever, safe if 1 tab 6 hours gap, max 4 per day.", "kn": "ಜ್ವರ ಮತ್ತು ನೋವಿಗೆ. ಜ್ವರ ಕಡಿಮೆ ಮಾಡುತ್ತದೆ. 6 ಗಂಟೆ ಅಂತರದಲ್ಲಿ 1 ಮಾತ್ರೆ, ದಿನಕ್ಕೆ 4 ಕ್ಕಿಂತ ಹೆಚ್ಚು ಬೇಡ. ಊಟದ ನಂತರ.", "use": "Fever / ಜ್ವರ"},
    "dolo": {"en": "Same as Paracetamol 650mg - for fever and body pain.", "kn": "Paracetamol 650mg ನಂತೆಯೇ - ಜ್ವರ ಮತ್ತು ಮೈಕೈ ನೋವಿಗೆ.", "use": "Fever / ಜ್ವರ"},
    "cetirizine": {"en": "For cold, sneezing, allergy. Makes sleepy, take at night.", "kn": "ಶೀತ, ಸೀನುವಿಕೆ, ಅಲರ್ಜಿಗೆ. ನಿದ್ದೆ ಬರಬಹುದು, ರಾತ್ರಿ ತೆಗೆದುಕೊಳ್ಳಿ.", "use": "Cold Allergy / ಶೀತ ಅಲರ್ಜಿ"},
    "azithromycin": {"en": "Antibiotic for throat infection. Complete full course, don't stop early.", "kn": "ಗಂಟಲು ಸೋಂಕಿಗೆ ಪ್ರತಿಜೀವಕ. ಪೂರ್ತಿ ಕೋರ್ಸ್ ಮುಗಿಸಿ, ಮಧ್ಯದಲ್ಲಿ ನಿಲ್ಲಿಸಬೇಡಿ.", "use": "Infection / ಸೋಂಕು"},
    "amoxicillin": {"en": "Antibiotic. Take after food, complete course.", "kn": "ಪ್ರತಿಜೀವಕ. ಊಟದ ನಂತರ ತೆಗೆದುಕೊಳ್ಳಿ, ಕೋರ್ಸ್ ಪೂರ್ತಿ ಮಾಡಿ.", "use": "Infection / ಸೋಂಕು"},
    "omeprazole": {"en": "For gas, acidity, stomach burning. Take before breakfast.", "kn": "ಗ್ಯಾಸ್, ಆಸಿಡಿಟಿ, ಹೊಟ್ಟೆ ಉರಿಗೆ. ಬೆಳಿಗ್ಗೆ ಉಪಹಾರಕ್ಕಿಂತ ಮೊದಲು.", "use": "Acidity / ಆಸಿಡಿಟಿ"},
    "metformin": {"en": "For diabetes, controls sugar. Take after food, don't miss.", "kn": "ಮಧುಮೇಹಕ್ಕೆ, ಸಕ್ಕರೆ ನಿಯಂತ್ರಣ. ಊಟದ ನಂತರ, ತಪ್ಪಿಸಬೇಡಿ.", "use": "Diabetes / ಸಕ್ಕರೆ ಕಾಯಿಲೆ"},
}

st.title(t("💊 Doctor Kannada + AI Search", "💊 ಔಷಧಿ AI ಹುಡುಕಾಟ - ಕನ್ನಡದಲ್ಲಿ"))
st.caption(t("Upload prescription + AI search any medicine in Kannada", "ಪ್ರಿಸ್ಕ್ರಿಪ್ಷನ್ + ಯಾವುದೇ ಔಷಧಿಯನ್ನು ಕನ್ನಡದಲ್ಲಿ AI ಹುಡುಕಿ"))

if "meds" not in st.session_state:
    st.session_state.meds = []

tab1, tab2, tab3 = st.tabs([t("📸 My Prescription","📸 ನನ್ನ ಪ್ರಿಸ್ಕ್ರಿಪ್ಷನ್"), t("🤖 AI Medicine Search","🤖 AI ಔಷಧಿ ಹುಡುಕಾಟ"), t("📋 My Medicines","📋 ನನ್ನ ಔಷಧಿಗಳು")])

with tab1:
    img = st.file_uploader(t("Upload prescription photo","ಪ್ರಿಸ್ಕ್ರಿಪ್ಷನ್ ಫೋಟೋ"), type=["jpg","png","jpeg"])
    if img: st.image(img, width=300)
    with st.form("add"):
        name = st.text_input(t("Medicine Name","ಔಷಧಿ ಹೆಸರು"), placeholder="Dolo 650")
        c1,c2,c3 = st.columns(3)
        m = c1.number_input("🌅 "+t("Morning","ಬೆಳಿಗ್ಗೆ"),0,4,1)
        n = c2.number_input("☀️ "+t("Noon","ಮಧ್ಯಾಹ್ನ"),0,4,0)
        ni = c3.number_input("🌙 "+t("Night","ರಾತ್ರಿ"),0,4,1)
        days = st.number_input(t("Days","ದಿನ"),1,90,3)
        if st.form_submit_button(t("Add","ಸೇರಿಸಿ")) and name:
            st.session_state.meds.append({"name":name,"m":m,"n":n,"ni":ni,"days":days})
            st.success(t("Added","ಸೇರಿಸಲಾಗಿದೆ"))

with tab2:
    st.subheader(t("🤖 AI Search - Ask about any medicine", "🤖 AI ಹುಡುಕಾಟ - ಯಾವುದೇ ಔಷಧಿ ಬಗ್ಗೆ ಕೇಳಿ"))
    st.write(t("Type medicine name like 'Dolo', 'Cetirizine', 'Metformin'", "ಔಷಧಿ ಹೆಸರು ಬರೆಯಿರಿ: Dolo, Cetirizine, Metformin"))
    q = st.text_input(t("Search medicine","ಔಷಧಿ ಹುಡುಕಿ"), placeholder="Paracetamol")
    if st.button(t("🔍 AI Explain","🔍 AI ವಿವರಿಸು")) and q:
        ql = q.lower().strip()
        found = None
        for key in MED_KB:
            if key in ql or ql in key:
                found = key; break
        if found:
            data = MED_KB[found]
            st.success(f"**{q.upper()}** - {data['use']}")
            st.markdown(f"### {t('In Kannada:','ಕನ್ನಡದಲ್ಲಿ:')} {data['kn']}")
            st.markdown(f"**English:** {data['en']}")
            # AI-style voice text
            voice = f"{q} - {data['kn']}"
            st.code(voice)
            st.info(t("💡 AI Tip: Always confirm with pharmacist. Don't self-medicate.","💡 AI ಸಲಹೆ: ಫಾರ್ಮಸಿಸ್ಟ್‌ನೊಂದಿಗೆ ಖಚಿತಪಡಿಸಿಕೊಳ್ಳಿ. ಸ್ವಯಂ ಔಷಧಿ ಬೇಡ."))
        else:
            st.warning(t(f"'{q}' not in local AI database. In pro version, this would call AI API for Kannada explanation. For now, add it manually.","ಸ್ಥಳೀಯ ಡೇಟಾಬೇಸ್‌ನಲ್ಲಿ ಇಲ್ಲ. ಪ್ರೊ ಆವೃತ್ತಿಯಲ್ಲಿ AI API ಕನ್ನಡ ವಿವರಣೆ ನೀಡುತ್ತದೆ."))
            st.write(t("Try: Paracetamol, Dolo, Cetirizine, Azithromycin, Omeprazole, Metformin","ಪ್ರಯತ್ನಿಸಿ: Paracetamol, Dolo, Cetirizine..."))
    
    st.markdown("---")
    st.subheader(t("Popular medicines","ಜನಪ್ರಿಯ ಔಷಧಿಗಳು"))
    cols = st.columns(3)
    for i, (k,v) in enumerate(MED_KB.items()):
        with cols[i%3]:
            with st.container(border=True):
                st.write(f"**{k.title()}**")
                st.caption(v['use'])
                if st.button(t("Explain","ವಿವರಿಸು"), key=f"kb_{k}"):
                    st.session_state['last_q'] = k
                    st.rerun()

with tab3:
    for i, med in enumerate(st.session_state.meds):
        with st.container(border=True):
            st.markdown(f"### {med['name']} - {med['days']} {t('days','ದಿನ')}")
            st.write(f"🌅 {med['m']} | ☀️ {med['n']} | 🌙 {med['ni']}")
            if st.button(t("Remove","ತೆಗೆದುಹಾಕಿ"), key=f"r{i}"):
                st.session_state.meds.pop(i); st.rerun()

st.sidebar.info("AI Search uses local KB now, can connect to OpenAI/Gemini later | Built by Bharath Gowda")
