# Resume\_Sense

Resume\_Sense is an AI-powered web application designed to analyze and provide insights into resumes. Built with Streamlit, it leverages advanced natural language processing techniques to extract key information from resumes, facilitating efficient candidate evaluation.

## 🚀 Features

* **Resume Upload & Parsing**: Upload resumes in PDF format, which are then parsed to extract structured information.
* **AI-Powered Analysis**: Utilizes advanced NLP models to analyze resume content and provide meaningful insights.
* **Interactive Interface**: User-friendly Streamlit interface for seamless interaction.

## 📁 Project Structure

```
Resume_Sense/
├── app.py
├── utils/
│ ├── init.py
│ ├── file_reader.py
│ ├── text_cleaning.py
│ ├── vectorizer.py
│ └── matcher.py
├── img/
├── data/ ← (This will be auto-created for results)
├── requirements.txt
└── README.md
```



* `app.py`: Main application script.
* `utils/`: Utility functions and modules.
* `img/`: Contains images used in the application.
* `data/`: Directory to store uploaded resumes and related data.
* `requirements.txt`: List of required Python packages.

## 🛠️ Technologies Used

* **Frontend**: [Streamlit](https://streamlit.io/)
* **Backend**: Python
* **Libraries**: PyPDF2, pandas, NumPy, etc.([github.com][1])

## 🧑‍💻 Getting Started

### Prerequisites

* Python 3.8 or higher
* pip package manager

### Installation

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/JGopalaKrishna/Resume_Sense.git
   cd Resume_Sense
   ```

2. **Install Dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Application**:

   ```bash
   streamlit run app.py
   ```

4. **Access the App**:
   Open your browser and navigate to `http://localhost:8501` to use the application.

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## 🔗 Live Demo

Check out the live version of the app here:  
👉 [Resume_Sense - Live App](https://jgopalakrishna-machinelearn-resumesense.streamlit.app/)
