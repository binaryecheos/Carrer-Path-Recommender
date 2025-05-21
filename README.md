# Carrer-Path-Recommender

The **Career Path Recommender** is a Streamlit-based web application designed to provide personalized career guidance for students and professionals. Developed as a B.Tech project in Computer Science and Engineering with a specialization in Artificial Intelligence & Machine Learning at Quantum University, Roorkee, this tool leverages Google’s Gemini 1.5 Flash large language model (LLM) and LangChain to analyze user inputs from resumes or a personality quiz, delivering tailored job recommendations, online courses, and career roadmaps.

## Features

- **Resume Analysis**: Upload PDF or DOCX resumes to extract technical and soft skills using PyPDF2 and python-docx.
- **Personality Quiz**: Answer a nine-question quiz to assess traits like work preferences, adaptability, and decision-making style.
- **Career Recommendations**: Receive 3–5 job suggestions (including titles, required skills, and salaries) and 3–5 online courses (with titles, platforms, and URLs).
- **Career Roadmap**: Obtain a markdown-formatted roadmap with 3–5 actionable steps and timelines.
- **Interactive Chat**: Engage with a context-aware AI chat interface powered by LangChain’s ConversationChain and ConversationBufferMemory.

## Demo

Try the live application: https://carrer-path-recommender.streamlit.app/

## Installation

To run the project locally, follow these steps:

1. **Clone the Repository**  
   ```bash
   git clone https://github.com/binaryecheos/Carrer-Path-Recommender
   cd career-path-recommender
   ```

2. **Set Up a Virtual Environment**  
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**  
   Ensure Python 3.8+ is installed. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set Up Environment Variables**  
   Create a `.env` file in the project root with your Google API key:
   ```plaintext
   GOOGLE_API_KEY=your_google_api_key_here
   ```
   Obtain a key from [Google Cloud Console](https://console.cloud.google.com/). Do **not** hardcode API keys in the source code.

5. **Run the Application**  
   Launch the Streamlit app:
   ```bash
   streamlit run main.py
   ```

## Requirements

Key dependencies are listed in `requirements.txt`:
- `streamlit==1.30.0` - Web application framework
- `langchain==0.2.0` - Conversational AI framework
- `langchain-google-genai==1.0.0` - Google Gemini API integration
- `PyPDF2==3.0.1` - PDF resume parsing
- `python-docx==1.1.0` - DOCX resume parsing
- `python-dotenv==1.0.0` - Environment variable management

Sample `requirements.txt`:
```plaintext
streamlit==1.30.0
langchain==0.2.0
langchain-google-genai==1.0.0
PyPDF2==3.0.1
python-docx==1.1.0
python-dotenv==1.0.0
```

## Usage

1. **Access the Application**: Open the app at `http://localhost:8501` (local) or via the deployment link.
2. **Upload Resume**: Use the sidebar to upload a PDF or DOCX resume for skill extraction.
3. **Take the Quiz**: Complete the nine-question personality quiz to receive a personality type (e.g., Creative Thinker).
4. **View Recommendations**: Get tailored job recommendations, course suggestions, and a career roadmap based on your inputs.
5. **Chat with AI**: Use the chat interface to ask follow-up career-related questions.

## Project Structure

```
career-path-recommender/
├── main.py              # Main Streamlit application
├── requirements.txt     # Project dependencies
├── .gitignore          # Excludes sensitive and temporary files
├── .env                # Environment variables (not tracked)
└── README.md           # Project documentation
```

## Technologies Used

- **Python 3.8+**: Core programming language
- **Streamlit**: Web application framework
- **Google Gemini 1.5 Flash**: LLM for skill extraction and recommendations
- **LangChain**: Framework for conversational AI and memory management
- **PyPDF2 & python-docx**: Libraries for resume text extraction
- **python-dotenv**: Environment variable loading
- **Markdown**: For formatting recommendations and roadmaps

