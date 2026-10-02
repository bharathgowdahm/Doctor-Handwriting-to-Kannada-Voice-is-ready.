import streamlit as st
from datetime import date
st.set_page_config(page_title="Doctor Handwriting to Kannada Voice", page_icon="💊", layout="wide")

lang = st.sidebar.selectbox("Language / ಭಾಷೆ", ["ಕನ್ನಡ", "English"])
def t(en, kn): return kn if lang=="ಕನ್ನಡ" else en

st.title(t("Medicine Reader - Your Language", "💊 ಔಷಧಿ ಅರ್ಥಮಾಡಿಕೊಳ್ಳಿ - ನಿಮ್ಮ ಭಾಷೆಯಲ್ಲಿ"))
st.caption(t("Upload prescription photo, get simple Kannada explanation + voice", "ಪ್ರಿಸ್ಕ್ರಿಪ್ಷನ್ ಫೋಟೋ ಅಪ್ಲೋಡ್ ಮಾಡಿ, ಸರಳ ಕನ್ನಡ ವಿವರಣೆ + ಧ್ವನಿ ಪಡೆಯಿರಿ"))

if "meds" not in st.session_state:
    st.session_state.meds = [
        {"name":"Paracetamol 650mg", "morning":1, "noon":0, "night":1, "days":3, "note":"ಊಟದ ನಂತರ / After food"},
        {"name":"Cetirizine 10mg", "morning":0, "noon":0, "night":1, "days":2, "note":"ರಾತ್ರಿ ಮಾತ್ರ / Night only"},
    ]

tab1, tab2 = st.tabs([t("📸 Add Medicine","📸 ಔಷಧಿ ಸೇರಿಸಿ"), t("📋 My Medicines","📋 ನನ್ನ ಔಷಧಿಗಳು")])

with tab1:
    st.subheader(t("Add from Prescription", "ಪ್ರಿಸ್ಕ್ರಿಪ್ಷನ್‌ನಿಂದ ಸೇರಿಸಿ"))
    img = st.file_uploader(t("Upload prescription photo (optional)", "ಪ್ರಿಸ್ಕ್ರಿಪ್ಷನ್ ಫೋಟೋ ಅಪ್ಲೋಡ್ ಮಾಡಿ"), type=["jpg","png","jpeg"])
    if img:
        st.image(img, caption=t("Prescription preview","ಪ್ರಿಸ್ಕ್ರಿಪ್ಷನ್"), width=300)
        st.info(t("Manual entry needed for accuracy - OCR is future upgrade","ನಿಖರತೆಗಾಗಿ ಕೈಯಾರೆ ನಮೂದಿಸಿ - OCR ಮುಂದಿನ ಆವೃತ್ತಿಯಲ್ಲಿ"))
    
    with st.form("med_form"):
        c1,c2 = st.columns(2)
        name = c1.text_input(t("Medicine Name","ಔಷಧಿ ಹೆಸರು"), placeholder="Paracetamol 650")
        days = c2.number_input(t("For how many days?","ಎಷ್ಟು ದಿನ?"), 1, 90, 3)
        st.write(t("When to take? / ಯಾವಾಗ ತೆಗೆದುಕೊಳ್ಳಬೇಕು?",""))
        cm, cn, cni = st.columns(3)
        m = cm.number_input(t("Morning - ಬೆಳಿಗ್ಗೆ","ಬೆಳಿಗ್ಗೆ"), 0, 4, 1)
        n = cn.number_input(t("Afternoon - ಮಧ್ಯಾಹ್ನ","ಮಧ್ಯಾಹ್ನ"), 0, 4, 0)
        ni = cni.number_input(t("Night - ರಾತ್ರಿ","ರಾತ್ರಿ"), 0, 4, 1)
        note = st.selectbox(t("Instruction","ಸೂಚನೆ"), ["ಊಟದ ನಂತರ / After food","ಊಟದ ಮೊದಲು / Before food","ಹಾಲಿನೊಂದಿಗೆ ಅಲ್ಲ / Not with milk",""])
        submit = st.form_submit_button(t("Add Medicine","ಔಷಧಿ ಸೇರಿಸಿ"))
        if submit and name:
            st.session_state.meds.append({"name":name,"morning":m,"noon":n,"night":ni,"days":days,"note":note})
            st.success(t("Added! Check My Medicines tab","ಸೇರಿಸಲಾಗಿದೆ! ನನ್ನ ಔಷಧಿಗಳನ್ನು ನೋಡಿ"))

with tab2:
    st.subheader(t("Big, Simple Cards for Elders","ಹಿರಿಯರಿಗೆ ದೊಡ್ಡ ಅಕ್ಷರಗಳಲ್ಲಿ"))
    if not st.session_state.meds:
        st.warning(t("No medicines added","ಯಾವುದೇ ಔಷಧಿ ಸೇರಿಸಿಲ್ಲ"))
    for i, med in enumerate(st.session_state.meds):
        with st.container(border=True):
            st.markdown(f"## 💊 {med['name']}")
            c1,c2,c3 = st.columns(3)
            c1.metric("🌅 " + t("Morning","ಬೆಳಿಗ್ಗೆ"), f"{med['morning']} ಮಾತ್ರೆ" if lang=="ಕನ್ನಡ" else f"{med['morning']} tab")
            c2.metric("☀️ " + t("Afternoon","ಮಧ್ಯಾಹ್ನ"), f"{med['noon']} ಮಾತ್ರೆ" if lang=="ಕನ್ನಡ" else f"{med['noon']} tab")
            c3.metric("🌙 " + t("Night","ರಾತ್ರಿ"), f"{med['night']} ಮಾತ್ರೆ" if lang=="ಕನ್ನಡ" else f"{med['night']} tab")
            st.info(f"📅 {med['days']} {t('days','ದಿನ')} | 📝 {med['note']}")
            # Kannada voice instruction text
            voice_text = f"{med['name']}. {med['morning']} ಮಾತ್ರೆ ಬೆಳಿಗ್ಗೆ, {med['night']} ಮಾತ್ರೆ ರಾತ್ರಿ, {med['days']} ದಿನ. {med['note']}"
            st.code(voice_text, language=None)
            st.caption(t("Press speaker button on phone to hear (browser TTS)","ಫೋನ್‌ನಲ್ಲಿ ಸ್ಪೀಕರ್ ಬಟನ್ ಒತ್ತಿ ಕೇಳಿ"))
            if st.button(t(f"Remove {med['name']}","ತೆಗೆದುಹಾಕಿ"), key=f"del{i}"):
                st.session_state.meds.pop(i)
                st.rerun()

st.sidebar.markdown("---")
st.sidebar.write(t("**Safety:** Always confirm with pharmacist. This is helper, not doctor.","**ಸುರಕ್ಷತೆ:** ಯಾವಾಗಲೂ ಫಾರ್ಮಸಿಸ್ಟ್‌ನೊಂದಿಗೆ ಖಚಿತಪಡಿಸಿಕೊಳ್ಳಿ."))
st.sidebar.write("Built by Bharath Gowda | For Karnataka Elders")
