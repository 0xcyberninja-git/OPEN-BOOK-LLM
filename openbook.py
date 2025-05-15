import os
import sys
from tkinter import Tk, Label, Entry, Button, filedialog, scrolledtext, messagebox
from llama_cpp import Llama
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import numpy; print(numpy.__version__)

class OpenBook:
    def __init__(self):
        # Create necessary directories
        self.create_directories()
        
        # Initialize with default paths
        self.model_path = "./models/mistral-7b-instruct.Q4_K_M.gguf"
        self.index_path = "./indexes/book_index"
        self.llm = None
        self.embeddings = None
        self.db = None
        
        # GUI elements
        self.root = Tk()
        self.root.title("OPENBOOK - Offline Document Q&A")
        self.root.geometry("800x600")
        
        # Create UI
        self.create_widgets()
        
    def create_directories(self):
        """Create necessary directories if they don't exist"""
        directories = ["./models", "./indexes"]
        for directory in directories:
            if not os.path.exists(directory):
                os.makedirs(directory)
                print(f"Created directory: {directory}")

    def initialize_models(self):
        """Load ML models (called once at startup)"""
        try:
            # Load Mistral-7B (4-bit quantized)
            self.llm = Llama(
                model_path=self.model_path,
                n_ctx=2048,
                n_threads=4,
                n_gpu_layers=20 if '--gpu' in sys.argv else 0
            )
            
            # Load embeddings
            self.embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
            
            return True
        except Exception as e:
            print(f"Model loading failed: {str(e)}")
            return False

    def create_widgets(self):
        """Build the Tkinter interface"""
        # Upload Button
        Button(self.root, 
               text="Upload PDF", 
               command=self.upload_pdf,
               font=("Arial", 12, "bold")).pack(pady=10)
        
        # Question Entry
        self.question_entry = Entry(self.root, width=80, font=("Arial", 12))
        self.question_entry.pack(pady=10)
        
        # Ask Button
        Button(self.root, 
               text="Ask Question", 
               command=self.ask_question,
               font=("Arial", 12)).pack(pady=5)
        
        # Answer Display
        self.answer_display = scrolledtext.ScrolledText(self.root, 
                                                      width=100, 
                                                      height=20,
                                                      font=("Arial", 11))
        self.answer_display.pack(pady=10)
        
        # Status Label
        self.status_label = Label(self.root, text="Ready", fg="gray")
        self.status_label.pack()

    def upload_pdf(self):
        """Handle PDF upload and indexing"""
        file_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
        if not file_path:
            return
            
        self.status_label.config(text="Processing PDF...", fg="orange")
        self.root.update()  # Force UI update
        
        try:
            # Load and split PDF
            loader = PyPDFLoader(file_path)
            pages = loader.load_and_split()
            
            splitter = RecursiveCharacterTextSplitter(
                chunk_size=500,
                chunk_overlap=100
            )
            chunks = splitter.split_documents(pages)
            
            # Create and save index
            if not os.path.exists("./indexes"):
                os.makedirs("./indexes")
                
            self.db = FAISS.from_documents(chunks, self.embeddings)
            self.db.save_local(self.index_path)
            
            self.status_label.config(text="Ready (Index built)", fg="green")
        except Exception as e:
            self.status_label.config(text=f"Error: {str(e)}", fg="red")

    def ask_question(self):
        """Handle question answering"""
        if not self.db:
            self.status_label.config(text="Error: No PDF loaded", fg="red")
            return
            
        question = self.question_entry.get()
        if not question:
            return
            
        self.status_label.config(text="Thinking...", fg="blue")
        self.root.update()  # Force UI update
        
        try:
            # Retrieve relevant chunks
            docs = self.db.similarity_search(question, k=2)
            
            # Build prompt
            context = "\n\n".join([d.page_content for d in docs])
            prompt = f"""Answer the question based ONLY on the following context. If unsure, say "I couldn't find this in the document."

            CONTEXT:
            {context}

            QUESTION: {question}
            ANSWER: """
            
            # Generate answer
            response = self.llm(
                prompt,
                max_tokens=300,
                temperature=0.3  # Less creative, more factual
            )
            
            answer = response["choices"][0]["text"]
            
            # Display results
            self.answer_display.delete(1.0, "end")
            self.answer_display.insert("end", answer)
            self.status_label.config(text="Ready", fg="green")
        except Exception as e:
            self.status_label.config(text=f"Error: {str(e)}", fg="red")

if __name__ == "__main__":
    # Check for model file
    if not os.path.exists("./models/mistral-7b-instruct.Q4_K_M.gguf"):
        print("Error: Model file not found. Please download:")
        print("wget https://huggingface.co/TheBloke/Mistral-7B-Instruct-v0.1-GGUF/resolve/main/mistral-7b-instruct-v0.1.Q4_K_M.gguf -O ./models/mistral-7b-instruct.Q4_K_M.gguf")
        messagebox.showerror("Error", "Model file not found. Please download the model file first.")
        sys.exit(1)
        
    # Create app
    app = OpenBook()
    
    # Initialize models
    if app.initialize_models():
        app.root.mainloop()
    else:
        messagebox.showerror("Error", "Failed to initialize models. Check console for errors.")
        sys.exit(1)