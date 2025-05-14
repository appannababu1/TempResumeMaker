import streamlit as st

from ResumeMaker import ResumeMaker

# Set page config
st.set_page_config(layout="wide", page_title="Resume Maker", page_icon=":guardsman:", initial_sidebar_state="expanded")

# Give the page a title with font size and alignment
st.markdown("<h1 style='text-align: left; font-size: 30px;'>Resume Maker</h1>", unsafe_allow_html=True)

@st.dialog("View Resumes", width="large")
def view_resume(resume):
    st.html(resume)

# Initialize bot in session state if it doesn't exist
if "resume_maker" in st.session_state:
    if st.session_state['resume_maker'].user_details != None:
        job_description = st.text_input("Enter the job description:")
        job_description_url = st.text_input("Enter the job description URL (optional):")
        user_prompt = st.text_input("Enter any specific prompt (optional):")
        resume_template = st.selectbox("Select a resume template:", ["Template 1", "Template 2", "Template 3"])
        if st.button("Create Resume"):
            try:
                resume, resume_idx = st.session_state['resume_maker'].create_resume(job_description, job_description_url, user_prompt, resume_template)
                st.success("Resume created successfully!")
                st.button("View Resume", on_click=view_resume, args=(resume,))
            except Exception as e:
                st.error(f"Error creating resume: {e}")
        resumes_list = st.session_state['resume_maker'].get_resumes_list()
        if resumes_list:
            st.subheader("View Previous Resumes")
            for idx, resume in enumerate(resumes_list):
                if st.button(f"View Resume {idx + 1}"):
                    view_resume(resume)
        else:
            st.warning("No previous resumes found.")
    else:
        input_user_details = st.text_input("Enter your details (e.g., name, education, experience):")
        if input_user_details:
            st.session_state['resume_maker'].set_user_details(input_user_details)
            st.success("User details set successfully!")
            st.rerun()
    
else:
    st.session_state['resume_maker'] = ResumeMaker()
    st.rerun()
