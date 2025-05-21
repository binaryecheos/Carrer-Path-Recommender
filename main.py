import streamlit as st
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
from langchain_google_genai import ChatGoogleGenerativeAI
import PyPDF2
from docx import Document
import json
import os
from dotenv import load_dotenv
import os

load_dotenv()
os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")
google_api_key = st.secrets["GOOGLE_API_KEY"]
st.set_page_config(page_title="Career Path Recommender", layout="wide")

st.title("🚀 Career Path Recommender")
st.markdown("Upload your resume or take the quiz to get started.")


# Define function to extract text from the uploaded resume
def extract_resume_text(uploaded_file):
    resume_text = ""

    # Determine file type and extract text
    if uploaded_file is not None:
        file_extension = uploaded_file.name.split(".")[-1].lower()

        try:
            if file_extension == "pdf":
                # Extract text from PDF
                pdf_reader = PyPDF2.PdfReader(uploaded_file)
                for page in pdf_reader.pages:
                    page_text = page.extract_text()
                    if page_text:
                        resume_text += page_text + "\n"

            elif file_extension == "docx":
                # Extract text from DOCX
                doc = Document(uploaded_file)
                for para in doc.paragraphs:
                    if para.text.strip():
                        resume_text += para.text + "\n"

            else:
                st.error("Unsupported file format. Please upload a PDF or DOCX file.")
                return ""

        except Exception as e:
            st.error(f"Error extracting text from file: {str(e)}")
            return ""

    if not resume_text.strip():
        st.error("No text could be extracted from the uploaded file.")
        return ""

    return resume_text


# Initialize memory
if "memory" not in st.session_state:
    st.session_state.memory = ConversationBufferMemory()
    st.session_state.chat_history = []

# --- Sidebar: Resume Upload and Quiz ---
with st.sidebar:
    st.header("Upload Resume")
    uploaded_file = st.file_uploader("Choose your resume (PDF/DOCX)", type=["pdf", "docx"])

    st.markdown("---")
    st.header("Take Personality Quiz")
    with st.form("quiz_form"):
        q1 = st.radio("You prefer to work:", ["Alone", "In a small team", "In a large team", "Depends on the task"])
        q2 = st.radio("You make decisions based on:",
                      ["Logic and analysis", "Feelings and intuition", "A balance of both"])
        q3 = st.radio("You are more:",
                      ["Highly organized", "Somewhat organized", "Spontaneous", "Chaotic but effective"])
        q4 = st.radio("You focus on:", ["Fine details", "The big picture", "Both equally"])
        q5 = st.radio("When solving problems, you are:",
                      ["Highly creative", "Practical and methodical", "A mix of creative and practical"])
        q6 = st.radio("How do you handle change?",
                      ["I adapt quickly", "I need time to adjust", "I resist change", "I thrive on change"])
        q7 = st.radio("In social settings, you are:",
                      ["Extroverted and outgoing", "Introverted but friendly", "Reserved and observant",
                       "Depends on my mood"])
        q8 = st.radio("Your goals are driven by:",
                      ["Achieving stability", "Pursuing passion", "Gaining recognition", "Personal growth"])
        q9 = st.radio("When faced with risks, you:",
                      ["Take calculated risks", "Avoid risks", "Embrace risks", "Assess risks thoroughly"])
        submit_quiz = st.form_submit_button("Submit Quiz")

# --- Processing Resume ---
extracted_skills = []  # Initialize as empty list
resume_text = ""

if uploaded_file:
    with st.spinner("Extracting resume text..."):
        resume_text = extract_resume_text(uploaded_file)

        if resume_text:
            # Use Gemini 1.5 Flash to extract skills
            llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.7, google_api_key=google_api_key)
            prompt = (
                "Extract technical and soft skills from the following resume text. "
                "Return a list of skills as a comma-separated string (e.g., 'Python, Data Analysis, Teamwork'). "
                "Focus on relevant skills and avoid duplicates. If no skills are found, return an empty string:\n\n"
                f"{resume_text}"
            )
            extracted_skills = llm.invoke(prompt).content.strip()

    if resume_text:
        st.subheader("📄 Resume Summary")
        st.markdown("**Extracted Resume Text:**")
        st.text_area("Resume Content", resume_text, height=300)
        st.markdown(
            "**Extracted Skills:** " +  extracted_skills)

# --- Personality Quiz Result ---
personality_type = None  # Initialize with a default value
if submit_quiz:
    # Collect quiz answers
    quiz_answers = {
        "Work preference": q1,
        "Decision-making": q2,
        "Organization style": q3,
        "Focus": q4,
        "Problem-solving": q5,
        "Adaptability": q6,
        "Social interaction": q7,
        "Goal orientation": q8,
        "Risk approach": q9
    }

    # Use Gemini to analyze the answers
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.7, google_api_key=google_api_key)
    prompt = (
            "Analyze the following quiz answers to determine the user's personality type. "
            "Provide a concise personality type label (e.g., 'Creative Thinker', 'Analytical Strategist', 'Empathetic Leader') "
            "based on these traits:\n" + "\n".join([f"{key}: {value}" for key, value in quiz_answers.items()]) + "\n"
                                                                                                                 "Return only the personality type label, nothing else."
    )
    personality_type = llm.invoke(prompt).content.strip()

    st.subheader("🧠 Personality Type:")
    st.success(f"Based on your answers, you're a **{personality_type}**.")

# --- Career Recommendation ---
if uploaded_file or submit_quiz:
    st.subheader("🎯 Career Recommendations")
    skills = extracted_skills if uploaded_file else []
    personality = personality_type if personality_type else "Unknown"

    # Use Gemini to generate job and course recommendations
    with st.spinner("Finding jobs and courses..."):
        llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.7, google_api_key=google_api_key)

        prompt = (
            "You are a career advisor. Based on the following skills and personality type, "
            "recommend 3–5 relevant jobs and 3–5 relevant online courses.\n\n"
            "Present the recommendations in two clearly separated sections:\n"
            "1. ### Jobs\n"
            "2. ### Courses\n\n"
            "For each job, include:\n"
            "- Job Title\n"
            "- Required Skills\n"
            "- Average Salary (e.g., $80K)\n\n"
            "For each course, include:\n"
            "- Course Title\n"
            "- Platform (e.g., Udemy, Coursera, edX)\n"
            "- URL (link to the course)\n\n"
            "Tailor the recommendations to match the provided skills and personality type.\n"
            "If no input is given, suggest general entry-level jobs and foundational courses.\n"
            "Always suggest at least one job and one course.\n\n"
            f"Skills: {', '.join(skills) if skills else 'None'}\n"
            f"Personality Type: {personality}\n"
        )

        try:
            response = llm.invoke(prompt).content.strip()

            if not response:
                raise ValueError("Gemini returned an empty response")

            # Attempt to split into sections
            if "### Courses" in response:
                jobs_section, courses_section = response.split("### Courses", 1)
                st.markdown("### 🔍 Suggested Jobs")
                st.markdown(jobs_section.replace("### Jobs", "").strip())
                st.markdown("### 📚 Recommended Courses")
                st.markdown(courses_section.strip())
            else:
                # Unexpected format, show whole response
                st.markdown("### 💡 Recommendations")
                st.markdown(response)

        except Exception as e:
            st.error(f"Error processing Gemini response: {str(e)}")
            st.markdown("### 🔍 Suggested Jobs")
            st.markdown("""
    - **Job Title**: General Developer  
      **Required Skills**: Coding Basics  
      **Average Salary**: $60K
            """)
            st.markdown("### 📚 Recommended Courses")
            st.markdown("""
    - **Course Title**: Intro to Programming  
      **Platform**: edX  
      **URL**: [Intro to Programming](https://example.com/intro)
            """)

    # --- Roadmap ---
    st.subheader("🗺 Career Roadmap")
    with st.spinner("Generating roadmap..."):
        # Use Gemini to generate a roadmap
        llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.7, google_api_key=google_api_key)
        prompt = (
            "Generate a career roadmap in markdown format based on the following skills and personality type. "
            "Include 3-5 steps with timelines (e.g., '1-3 months', '3-6 months') and actionable advice:\n"
            f"Skills: {', '.join(skills)}\n"
            f"Personality Type: {personality if personality else 'Unknown'}\n"
            "Return only the markdown content."
        )
        roadmap = llm.invoke(prompt).content.strip()
    st.markdown(roadmap)

# --- Chat Interface ---
st.markdown("### 💬 Ask anything:")
user_input = st.text_input("You:", key="chat_input")

if user_input:
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.7, google_api_key=google_api_key)
    chain = ConversationChain(llm=llm, memory=st.session_state.memory)
    response = chain.run(user_input)
    st.session_state.chat_history.append((user_input, response))

for i, (user_q, bot_r) in enumerate(st.session_state.chat_history[::-1]):
    st.markdown(f"**You:** {user_q}")
    st.markdown(f"**Bot:** {bot_r}")
