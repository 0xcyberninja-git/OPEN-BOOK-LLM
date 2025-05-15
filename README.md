# OPEN-BOOK-LLM
📖 OPENBOOK: Offline AI-powered document Q&amp;A tool. Upload PDFs/textbooks, ask questions, get precise answers with page references. No internet needed—100% private. Supports 3000+ page books via Mistral-7B &amp; FAISS. Perfect for students/researchers.  

(Note) This is a Prototype Version - Complete Project will be upload soon in README2.md file. Where i will Upload the Google Drive Link. 
Here I just Uploaded a Prototype Project - YOU CAN USE THEM TO MAKE AN ADDITIONAL UPDATES. 

# 📖 OPENBOOK - Offline Document Q&A with AI

![image](https://github.com/user-attachments/assets/5d3c9aff-0913-4afc-af0e-079da248f687)


**Ask questions about your PDFs/textbooks—100% offline, no data leaks.** Powered by Mistral-7B and FAISS for lightning-fast, private document analysis.

## ✨ Features

- **100% Offline**: No internet? No problem. Works in secure environments
- **3000+ Page Support**: Handles giant textbooks with ease
- **Precision Answers**: Page references + highlighted text snippets
- **Diagram Support**: Extracts and explains figures/charts
- **Privacy-First**: Your documents never leave your device

## 🚀 Quick Start

```bash
# 1. Clone repo
git clone https://github.com/0xcyberninja-get/OPEN-BOOK-LLM.git
cd OPEN-BOOK-LLM

# 2. Install dependencies
pip install -r requirements.txt

# 3. Download model (one-time)
wget https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.1-GGUF/resolve/main/mistral-7b-instruct-v0.1.Q4_K_M.gguf -O models/mistral.gguf

# 4. Run!
python openbook.py


🔧 Configuration
Edit config.yaml to:

model:
  path: "./models/mistral.gguf"
  gpu_layers: 20  # Set to 0 for CPU-only

retrieval:
  chunk_size: 512  # Optimize for your documents


📦 Project Structure

OPENBOOK/
├── models/          # Store GGUF models here
├── indexes/         # FAISS vector stores
├── docs/            # Sample PDFs for testing
├── openbook.py      # Main application
└── requirements.txt

🤝 How to Contribute
Fork the project

Create your feature branch (git checkout -b feat/amazing-feature)

Submit a pull request

📜 License
MIT © PRATIEK BHIVGADE 
