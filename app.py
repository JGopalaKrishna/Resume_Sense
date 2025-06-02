import streamlit as st
import os
import pandas as pd
from utils.file_reader import extract_text_from_files
from utils.text_cleaning import clean_text
from utils.vectorizer import vectorize_texts
from utils.matcher import compute_similarity

import base64
def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

st.set_page_config(page_title="Resume Screener", layout="wide")

st.markdown("""
    <style>
    .stApp{
        background-color: #f0f0f0;
    }
    .st-emotion-cache-t1wise{
        padding: 30px 20px;
    }
    header{
        display: none;
    }
    .stAppHeader{
        display: none;
    }
    
    /* Custom top bar */
    .custom-top-bar {
        background-color: #50C9CE;color: #2E382E;
        padding: 10px 30px;
        font-size: 30px;font-weight: bold;
        position: fixed;top: 0px;left: 0;right: 0;
        z-index: 9999;
        display: flex;justify-content: space-between;align-items: center;
    }
    .custom-top-bar img {
        height: 50px;
        margin-right: 10px;
        border-radius: 50%;
    }
    #intelligent-resume-screening-system{
        color: #2E382E;
    }
    .st-emotion-cache-1gulkj5{
        background-color: #fff;
        # color: #2E382E;
    }
    .st-emotion-cache-ocsh0s{
        border-color: #50C9CE;color: #50C9CE;
    }
    .st-emotion-cache-6rlrad{
        color: #2E382E;
    }
    .st-emotion-cache-br351g{
        color: #2E382E;
    }
    .st-bb {
        background-color: #fff;color: #2E382E;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.2/css/all.min.css" integrity="sha512-SnH5WK+bZxgPHs44uWIX+LLJAJ9/2PkPKZ5QiAj6Ta86w+fsb2TkcmfRyVX3pBnMFcV7oQPJkl9QevSCWr3W6A==" crossorigin="anonymous" referrerpolicy="no-referrer" />
""", unsafe_allow_html=True)

st.markdown("""
    <style>
        .component{}
        .component1{
            min-height: 100svh;width: 100%;
            display: flex;justify-content: space-between;align-items: center;
        }
        .compart11,.compart12{height: fit-content;}
        .compart11{width: calc(95% - 550px);}
        .compart12 img{height: 300px;width: 550px;}
        @media screen and (max-width:939px){
            .component1{display: flex;justify-content: space-evenly;align-items: center;flex-direction: column;gap:20px;}
            .compart11,.compart12{width: 95%;display: flex;justify-content: center;align-items: center;flex-direction: column;}
            .compart11 p,h2{text-align: center;}
        }
        @media screen and (max-width:612px){
            .compart12 img{width: 100%;height: auto;aspect-ratio: 11 / 6;object-fit: cover;}
        }
        .ButtonsDiv{display: flex;gap: 10px;}
        .Button1{
            padding: 5px 10px;
            border-radius: 10px;border: 2px solid #50C9CE;
            background-color: #50C9CE;color: white;
            cursor: pointer;position: relative;overflow: hidden;transition: all 1s;
        }
        .Button1::after{
            content: "";
            height: 120%;width: 0%;
            position: absolute;top: -15%;left: -15%;
            border-radius: 25px; transform: rotate(30deg); box-shadow: 1px 1px 9px 4.5px white;
        }
        .Button1:hover::after{animation: Move_white_light 2s infinite;}
        .Button1:hover{scale: 1.1;}
        .Button2{
            padding: 5px 10px;
            border-radius: 10px;border: 2px solid #50C9CE;
            background-color: white;color: #50C9CE;
            cursor: pointer;position: relative;overflow: hidden;transition: all 1s;
        }
        .Button2::after{
            content: "";
            height: 120%;width: 0%;
            position: absolute;top: -15%;left: -15%;
            border-radius: 25px; transform: rotate(30deg); box-shadow: 1px 1px 9px 4.5px white;
        }
        .Button2:hover::after{animation: Move_white_light 2s infinite;}
        .Button2:hover{scale: 1.1;}
        @keyframes Move_white_light{
            0%{left: -15%;}
            100%{left: 115%;}
        }
        .component2{
            min-height: 85svh;max-height: fit-content;width: 100%;
            display: flex;justify-content: space-evenly;align-items: center;
            flex-wrap: wrap;gap: 25px;
        }
        .compart21{
            height: 350px;width: 260px;
            border-radius: 10px;border: 2px solid #6a6a6a;
            position: relative;overflow: hidden;
            transition: all 1s;
        }
        .compart21Div1{
            height: 150px;width: 100%;
            position: absolute;top: 0;
        }
        .compart21Div1 img{height: 100%;width: 100%;transition: all 1s;}
        .compart21Div2{
            height: 200px;width: 100%;padding: 5px 5%;
            display: flex;justify-content: center;align-items: center;flex-direction: column;
            position: absolute;bottom: 0;
            background-color: rgb(255, 255, 255);
            border-radius: 10px 10px 0 0;border-top: 2px solid #454545;
            transition: all 1s;
        }
        .compart21:hover{cursor: pointer;box-shadow: 3px 3px 10px black;}
        .compart21:hover .compart21Div1 img{opacity: 0.7;scale: 1.1;}
        .compart21:hover .compart21Div2{height: 220px;box-shadow: 0px -5px 10px 5px black;}
        .compart21Div2 p{
            padding: 0;margin: 5px;
            text-align: center;transition: all 1s;
        }
        .compart21Div2 i{font-size: 30px;color: #50C9CE;margin-bottom: 5px;}
        .sideHeading{font-size: 20px;font-weight: bolder;transition: all 1s;}
        .content{font-size: 16px;text-align: center;transition: all 1s;}
        .compart21:hover .content{transform: scale(1.05);text-shadow: 0px 0px 1px #50C9CE;}
        .compart21:hover .sideHeading{color: #50C9CE;font-size: 23px;}
        .footer{
            background-color: white;
            padding: 20px;border-radius: 15px;margin-top: 200px;
            display: flex;justify-content: space-evenly;align-items: center;flex-wrap: wrap;gap: 10px;
        }
        .connectData{
            font-size: 20px;
            display: flex;gap: 10px;
            color: black;text-decoration: none;
            width: fit-content;transition: all 1s;
        }
        .connectData:hover{transform: scale(1.05);text-shadow: 2px 2px 2px #50C9CE;}
    </style>
""", unsafe_allow_html=True)

# Inject images
img_base64 = get_base64_image("./img/Logo.png")
ai1 = get_base64_image("./img/ai1.png")
resume = get_base64_image("./img/resume.png")
des = get_base64_image("./img/job_description.png")
ai = get_base64_image("./img/ai.png")
st.markdown(f"""
    <div class="custom-top-bar">
        <img src="data:image/png;base64,{img_base64}" alt="Logo">
        <div class="title">Resume Sense</div>
        <div></div>
    </div>
""", unsafe_allow_html=True)
st.markdown(f"""
    <main class="component">
        <section class="component1">
            <div class="compart11">
                <h2>Al-Powered Resume Scanning for Recruiters</h2>
                <p>Quickly scan multiple resumes and match them to a job description using advanced Al, saving hours of manual review. Find the best candidates faster and more efficiently.</p>
                <div class="ButtonsDiv">
                    <a href="#intelligent-resume-screening-system" style="text-decoration: none;"><div class="Button1">Get Started Now</div></a>
                    <a href="#how-it-works" style="text-decoration: none;"><div class="Button2">Learn More</div></a>
                </div>
            </div>
            <div class="compart12"><img src="data:image/png;base64,{ai1}" alt="Logo"/></div>
        </section>
        <h1 style="text-align: center;">How It Works</h1>
        <section class="component2">
            <div class="compart21">
                <div class="compart21Div1"><img src="data:image/png;base64,{resume}" alt="Logo"/></div>
                <div class="compart21Div2">
                    <i class="fa-solid fa-arrow-up-from-bracket"></i>
                    <p class="sideHeading">Upload Resumes</p>
                    <sp class="content">Drag and drop multiple resume files (PDF,DOCX,TXT) securely into the platform.</sp>
                </div>
            </div>
            <div class="compart21">
                <div class="compart21Div1"><img src="data:image/png;base64,{des}" alt="Logo"/></div>
                <div class="compart21Div2">
                    <i class="fa-solid fa-pen-to-square"></i>
                    <p class="sideHeading">Add Job Description</p>
                    <sp class="content">Paste or type the job description you want to match the resumes against.</sp>
                </div>
            </div>
            <div class="compart21">
                <div class="compart21Div1"><img src="data:image/png;base64,{ai}" alt="Logo"/></div>
                <div class="compart21Div2">
                    <i class="fa-solid fa-tower-broadcast"></i>
                    <p class="sideHeading">Al Scans & Matches</p>
                    <sp class="content">Our Al analyzes each resume and compares it to the job description, identifying key matches.</sp>
                </div>
            </div>
        </section>
    </main>
""", unsafe_allow_html=True)
st.markdown("---")
st.title("Intelligent Resume Screening System")

# Upload resumes and paste job description
uploaded_resumes = st.file_uploader(
    "Upload multiple resumes (PDF/DOCX/TXT)",
    type=["pdf", "docx","txt"],
    accept_multiple_files=True
)
job_description = st.text_area("📋Paste the Job Description here")

# When button is clicked and input is valid
if st.button("🔍 Match Resumes") and uploaded_resumes and job_description:
    with st.spinner("Matching resumes to the job description..."):
        texts = extract_text_from_files(uploaded_resumes)       # 1. Extract text from resumes
        cleaned_resumes = [clean_text(text) for text in texts]  # 2. Clean each resume and JD
        cleaned_jd = clean_text(job_description)
        resume_vectors, jd_vector = vectorize_texts(cleaned_resumes, cleaned_jd)# 3. Vectorize the texts
        scores = compute_similarity(resume_vectors, jd_vector)  # 4. Compute similarity scores
        results = pd.DataFrame({                                # 5. Prepare and display results
            "Resume File": [file.name for file in uploaded_resumes],
            "Match Score (%)": [score for score in scores],
            "Category": ["⭐ Excellent" if score>=90 else "✅ Good" if score>=70 else "⚠️ Moderate" if score>=50 else "❌ Weak" if score>=30 else "🚫 Very Poor" for score in scores],
            "Fit": ["Top Match" if score>=90 else "Fit" if score>=70 else "Maybe" if score>=50 else "Not a Fit" if score>=30 else "Irrelevant" for score in scores],
        }).sort_values(by="Match Score (%)", ascending=False)
        st.success("✅ Matching Complete!")
        st.dataframe(results)
        os.makedirs("data", exist_ok=True)                      # 6. Save and offer download
        results.to_csv("data/results.csv", index=False)
        st.download_button(label="⬇️ Download Results as CSV",data=results.to_csv(index=False),file_name="matched_resumes.csv",mime="text/csv")

#Copyright Mark
st.markdown(f"""
    <div class="footer">
        <a href="mailto:jakkakrishna2003@gmail.com"  class="connectData" style="text-decoration: none;color:black;">
            <div><i class="fa-regular fa-envelope" style="color: #50C9CE;"></i></div>
            <div>Email</div>
        </a>
        <a href="https://www.linkedin.com/in/gopala-krishna-jakka-294a3b2a6/" class="connectData" style="text-decoration: none;color:black;">
            <div><i class="fa-brands fa-linkedin" style="color: #50C9CE;"></i></div>
            <div>Linked In</div>
        </a>
        <a href="https://github.com/JGopalaKrishna" class="connectData" style="text-decoration: none;color:black;">
            <div><i class="fa-brands fa-github" style="color: #50C9CE;"></i></div>
            <div>Git Hub</div>
        </a>
        <a href="https://jgopalakrishna-portfolio.netlify.app/" class="connectData" style="text-decoration: none;color:black;">
            <div><i class="fa-regular fa-folder-open" style="color: #09cedc;"></i></div>
            <div>Portfolio</div>
        </a>
        <div style="transform: scale(1.05);text-shadow: 1px 1px 1px #50C9CE;font-size: 20px;">© Copyright 2025 J.Gopala Krishna, All rights reserved | Designed with care and crafted with 💚 using Streamlit.</div>
    </div>
""", unsafe_allow_html=True)