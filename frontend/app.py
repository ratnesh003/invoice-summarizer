import streamlit as st
import requests
import json
import pandas as pd
from datetime import datetime

# Backend URL
API_URL = "http://localhost:8000/api"

st.set_page_config(layout="wide", page_title="Order Processor")

def fetch_history():
    try:
        response = requests.get(f"{API_URL}/history")
        if response.status_code == 200:
            return response.json()
        else:
            st.error("Failed to fetch history")
            return []
    except Exception as e:
        st.error(f"Error fetching history: {e}")
        return []



def delete_submission(submission_id):
    try:
        response = requests.delete(f"{API_URL}/history/{submission_id}")
        if response.status_code == 200:
            st.success("Submission deleted")
            return True
        else:
            st.error("Failed to delete submission")
            return False
    except Exception as e:
        st.error(f"Error deleting submission: {e}")
        return False

def main():
    st.title("Order Processing System")
    
    # Sidebar History
    st.sidebar.header("History")
    history = fetch_history()
    
    # Store selected submission in session state
    if 'selected_submission_id' not in st.session_state:
        st.session_state['selected_submission_id'] = None
    
    if history:
        for submission in history:
            # Check for valid submission structure (migration)
            if 'files' not in submission:
                continue
                
            timestamp = submission['timestamp'][:16].replace('T', ' ')
            file_count = len(submission['files'])
            label = f"{timestamp} ({file_count} files)"
            
            with st.sidebar.expander(label):
                if st.button("View Files", key=f"view_{submission['id']}"):
                    st.session_state['selected_submission_id'] = submission['id']
                
                if st.button("Delete", key=f"del_{submission['id']}"):
                    if delete_submission(submission['id']):
                        st.rerun()

    # New Upload Section
    if not st.session_state['selected_submission_id']:
        st.subheader("Upload New Files")
        uploaded_files = st.file_uploader("Choose text files", type=['txt'], accept_multiple_files=True)
        
        if uploaded_files:
            if st.button("Process Files"):
                with st.spinner("Processing..."):
                    files_payload = [("files", (file.name, file, "text/plain")) for file in uploaded_files]
                    try:
                        response = requests.post(f"{API_URL}/upload", files=files_payload)
                        if response.status_code == 200:
                            submission = response.json()
                            st.success(f"Processed {len(submission['files'])} files!")
                            st.session_state['selected_submission_id'] = submission['id']
                            st.rerun()
                        else:
                            st.error(f"Upload failed: {response.text}")
                    except Exception as e:
                        st.error(f"Error uploading files: {e}")

    # Display Section (Submission View)
    if st.session_state['selected_submission_id']:
        # Find submission in history (in case it wasn't just uploaded)
        history = fetch_history() # Re-fetch to be safe
        submission = next((s for s in history if s['id'] == st.session_state['selected_submission_id']), None)
        
        if submission:
            st.button("Back to Upload", on_click=lambda: st.session_state.update({'selected_submission_id': None}))
            
            st.subheader(f"Submission: {submission['timestamp'][:16].replace('T', ' ')}")
            
            # File Tabs
            file_names = [f['filename'] for f in submission['files']]
            selected_tab = st.selectbox("Select File", file_names)
            
            selected_file = next(f for f in submission['files'] if f['filename'] == selected_tab)
            
            view_mode = st.radio("View Mode", ["Output Report", "Error Log"], horizontal=True, key=f"mode_{selected_file['id']}")
            file_type = "output" if view_mode == "Output Report" else "error"
            
            col1, col2 = st.columns(2)
            
            try:
                response = requests.get(f"{API_URL}/file/{selected_file['id']}/{file_type}")
                if response.status_code == 200:
                    content = response.text
                    st.code(content, language="text")
                    
                    st.download_button(
                        label=f"Download {view_mode}",
                        data=content,
                        file_name=f"{selected_file['filename']}_{file_type}.txt",
                        mime="text/plain"
                    )
                else:
                    st.error("Failed to load content")
            except Exception as e:
                st.error(f"Connection error: {e}")
        else:
            st.warning("Submission not found (it may have been deleted).")
            st.session_state['selected_submission_id'] = None
            st.rerun()

if __name__ == "__main__":
    main()
