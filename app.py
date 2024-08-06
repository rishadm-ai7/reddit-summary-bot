import streamlit as st
import requests

st.title('Reddit URL Summarizer')

url = st.text_input('Enter the Reddit URL')

if st.button('Summarize'):
    if url:
        with st.spinner('Fetching and summarizing data...'):
            try:
                response = requests.post("http://localhost:8000/summarize", json={"url": url}, stream=True)
                if response.status_code == 200:
                    st.success('Data fetched successfully!')
                    summary = ""
                    for line in response.iter_lines():
                        if line:
                            decoded_line = line.decode('utf-8')
                            summary += decoded_line
                            st.write(decoded_line)
                else:
                    st.error('Error fetching summary!')
            except requests.exceptions.RequestException as e:
                st.error(f"Request failed: {e}")
    else:
        st.error('Please enter a valid URL!')
