import streamlit as st
import google.generativeai as genai
import json

st.set_page_config(page_title="RegTech OS", page_icon="⚖️", layout="wide")
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel("gemini-1.5-pro", system_instruction="You are RegTech OS — the world's most accurate regulatory compliance AI. Always return perfect JSON.")

st.title("⚖️ RegTech OS")
st.markdown("**Upload any policy, contract, or regulation — get instant compliance mapping, risk score, and remediation plan.**")

uploaded = st.file_uploader("Drop PDF, DOCX, or text", type=["pdf","txt","docx"])
if uploaded and st.button("Analyze Compliance", type="primary"):
    text = uploaded.read().decode() if uploaded.type == "application/pdf" else uploaded.getvalue().decode()
    with st.spinner("Running full regulatory scan..."):
        response = model.generate_content(f"""
        Analyze this document for compliance with: SEC, FINRA, GDPR, CCPA, SOX, HIPAA.
        Return ONLY valid JSON:
        {{
          "overall_risk": "Low|Medium|High|Critical",
          "violations_found": int,
          "top_3_risks": [{{"section": "", "regulation": "", "severity": ""}}],
          "remediation_plan": ["Step 1...", "Step 2..."]
        }}
        Document: {text[:30000]}
        """)
        try:
            result = json.loads(response.text.replace("```json","").replace("```",""))
            st.success(f"Risk Level: {result['overall_risk']}")
            st.json(result, expanded=True)
        except:
            st.code(response.text)
