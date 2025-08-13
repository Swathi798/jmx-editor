import streamlit as st
import xml.etree.ElementTree as ET
import io

st.title("🧪 JMX Scenario Editor")

uploaded_file = st.file_uploader("Upload JMX File", type="jmx")

users = st.number_input("Number of Users", min_value=1, value=100)
ramp_up = st.number_input("Ramp-Up Time (seconds)", min_value=1, value=10)
loop_count = st.number_input("Loop Count", min_value=1, value=10)
duration = st.number_input("Duration (seconds)", min_value=1, value=10)
# endpoint = st.text_input("Endpoint Path", value="/api/test")
# method = st.selectbox("HTTP Method", ["GET", "POST"])

if uploaded_file and st.button("Update Scenario"):
    tree = ET.parse(uploaded_file)
    root = tree.getroot()

    for elem in root.iter():
        if elem.tag == 'stringProp':
            if elem.attrib.get('name') == 'ThreadGroup.num_threads':
                elem.text = str(users)
            elif elem.attrib.get('name') == 'ThreadGroup.ramp_time':
                elem.text = str(ramp_up)
            elif elem.attrib.get('name') == 'ThreadGroup.loop_count':
                elem.text = str(loop_count)
            elif elem.attrib.get('name') == 'ThreadGroup.duration':
                elem.text = str(duration)
            # elif elem.attrib.get('name') == 'HTTPSampler.path':
                # elem.text = endpoint
            # elif elem.attrib.get('name') == 'HTTPSampler.method':
                # elem.text = method

    buffer = io.BytesIO()
    tree.write(buffer, encoding="utf-8", xml_declaration=True)
    st.download_button("📥 Download updated JMX", data=buffer.getvalue(), file_name="updated_test_plan.jmx")