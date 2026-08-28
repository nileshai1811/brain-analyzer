import streamlit as st
import openai
import os

st.set_page_config(page_title="NeuroQuant Report Generator", layout="wide", page_icon="🧠")
st.title("🧠 AI NeuroQuant Volumetric Reporting Agent")
st.write("Extracts raw quantitative brain metrics into localized Body and Impression report sections.")

api_key = os.getenv("OPENAI_API_KEY", "")
if api_key:
    openai.api_key = api_key
else:
    st.sidebar.warning("⚠️ OpenAI API Key not detected in environment variables.")

# Unified Text Input Pane
raw_data = st.text_area("Paste the raw NeuroQuant text output here:", height=250, placeholder="Amygdala Left Side Volume: 1.70...")

# Highly specific structured radiology prompt
NQ_SYSTEM_PROMPT = """You are an expert neuroradiologist. Analyze the raw absolute volumes, percentages of intracranial volume, and Asymmetry Indices from the attached NeuroQuant study. 

You must generate an output divided strictly into two distinct parts:

PART 1: BODY OF REPORT (FINDINGS)
- Provide a concise yet detailed paragraph outlining the exact metrics of key evaluated structures (e.g., Amygdala, Frontal regions, Brainstem, Caudate, Cerebellum).
- Explicitly state absolute volumes or side-specific characteristics extracted from the text stream.

PART 2: IMPRESSION
- Focus exclusively on clinically relevant abnormal findings (such as severe volume loss or striking structural asymmetries where the Asymmetry Index is >15% or < -15%).
- If all values and indices fall within normal expected limits, explicitly state that brain volumes and structural symmetry are age-appropriate.

Do not include any conversational intro/outro or markdown divider lines. Start directly with 'PART 1: BODY OF REPORT'."""

if st.button("🚀 Generate Segmented Report", type="primary"):
    if not api_key:
        st.error("Please configure an active OpenAI API Key before running.")
    elif not raw_data.strip():
        st.error("Please enter data first.")
    else:
        with st.spinner("Processing data stream and isolating structural anomalies..."):
            try:
                client = openai.OpenAI(api_key=api_key)
                response = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {"role": "system", "content": NQ_SYSTEM_PROMPT},
                        {"role": "user", "content": f"Analyze the following data stream:\n\n{raw_data}"}
                    ],
                    temperature=0.1
                )
                generated_report = response.choices.message.content.strip()
                
                st.subheader("📋 Output Text (Ready to Copy)")
                st.text_area("Final Split Narrative", value=generated_report, height=350)
                st.info("💡 You can copy individual segments directly into the Body or Impression zones of your primary reporting system.")
            except Exception as e:
                st.error(f"An engine communication error occurred: {str(e)}")
