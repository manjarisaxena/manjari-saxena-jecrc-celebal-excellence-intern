# 🚀 Manjari Saxena — Celebal Excellence Intern (CEI)

Welcome to my internship repository for the **Celebal Technologies Summer Internship Program (CEI)**.

This repository contains weekly assignments, hands-on projects, and practical implementations completed throughout my internship journey in **Data Science, Machine Learning, Deep Learning, Computer Vision, Natural Language Processing, and Generative AI**.

---

# 👩‍💻 Intern Details

- **Name:** Manjari Saxena
- **University:** JECRC University, Jaipur
- **Internship Role:** Celebal Excellence Intern (CEI)
- **Organization:** Celebal Technologies

---

# 📂 Week 1

## Project

**Python Fundamentals, Data Analysis & Visualization**

### Topics Covered

- Python Programming Fundamentals
- NumPy Operations
- Pandas Data Analysis
- Data Visualization
- Statistical Analysis
- Data Manipulation

### Skills Learned

- Python Programming
- Data Analysis
- Problem Solving
- Statistical Thinking
- Data Visualization

---

# 📂 Week 2

## Project

**Tesla EV Deliveries and Production Forecasting (2015–2025)**

### Topics Covered

- Exploratory Data Analysis (EDA)
- Feature Engineering
- Linear Regression
- Cross Validation
- Hyperparameter Tuning
- Random Forest Regression
- ARIMA Forecasting
- Time Series Analysis

### Key Results

- Linear Regression R² Score: **0.9889**
- Cross Validation R² Score: **0.9903**
- Successful ARIMA Forecasting

### Skills Learned

- Machine Learning
- Feature Engineering
- Time Series Forecasting
- Model Evaluation
- Hyperparameter Tuning

---

# 📂 Week 3

## Project

**Customer Intelligence System using Classification, Ensemble Learning & Clustering**

### Algorithms Used

#### Clustering

- K-Means
- DBSCAN

#### Classification

- Random Forest
- XGBoost

### Topics Covered

- Data Preprocessing
- Feature Scaling
- Clustering
- Classification
- Ensemble Learning
- Feature Importance Analysis
- Business Intelligence

### Key Results

- Country Segmentation
- Developed, Developing and Underdeveloped Country Clusters
- High Classification Performance
- Actionable Business Insights

### Skills Learned

- Clustering
- Ensemble Learning
- Classification
- XGBoost
- Random Forest
- Business Intelligence

---

# 📂 Week 4

## Project

**CIFAR-10 Image Classification using ANN, CNN and Augmented CNN**

### Topics Covered

- Computer Vision
- Deep Learning
- ANN
- CNN
- Data Augmentation
- Batch Normalization
- Dropout
- Early Stopping

### Models Implemented

- Artificial Neural Network (ANN)
- Convolutional Neural Network (CNN)
- Augmented CNN

### Key Results

- Comparative Performance Analysis
- Validation Accuracy Curves
- CNN Test Accuracy: **64.3%**

### Skills Learned

- Computer Vision
- CNN Architecture Design
- Image Classification
- Deep Learning
- TensorFlow & Keras

---

# 📂 Week 5

## Project

**Text Generation using Vanilla RNN, LSTM and GRU**

### Project Description

Implemented and compared three recurrent neural network architectures for next-word prediction and text generation. The project focuses on learning grammatical structure, contextual dependencies, and sequence modeling from a custom text corpus.

### Topics Covered

- Natural Language Processing (NLP)
- Text Preprocessing
- Tokenization
- N-Gram Sequence Generation
- Sequence Padding
- Word Embeddings
- Recurrent Neural Networks
- LSTM Networks
- GRU Networks
- Text Generation
- Language Modeling
- Next Word Prediction

### Models Implemented

#### Vanilla RNN

- Embedding Layer
- SimpleRNN Layer
- Dense Output Layer

#### LSTM

- Embedding Layer
- LSTM Layer
- Dense Output Layer

#### GRU

- Embedding Layer
- GRU Layer
- Dense Output Layer

### Key Results

- Trained Vanilla RNN, LSTM and GRU using identical configurations.
- Generated meaningful text sequences using next-word prediction.
- Compared model convergence using loss and accuracy curves.
- Extended training to 200 epochs.
- Implemented a custom text corpus and enhanced model architecture.

### Skills Learned

- Natural Language Processing
- Sequence Modeling
- Text Generation
- Deep Learning
- RNN
- LSTM
- GRU
- Language Modeling
- TensorFlow & Keras

---

# 📂 Week 6

## Project

**Image Denoising using Convolutional Autoencoder (MNIST)**

### Project Description

Designed and implemented a **Convolutional Denoising Autoencoder** to remove Gaussian noise from handwritten digit images using the **MNIST dataset**. The model learns compressed latent representations through an encoder and reconstructs clean images using a decoder. This project demonstrates the application of deep learning for image restoration, feature extraction, and representation learning.

### Topics Covered

- Autoencoders
- Convolutional Autoencoders
- Encoder–Decoder Architecture
- Latent Space Representation
- Image Denoising
- Gaussian Noise Generation
- Image Reconstruction
- Deep Learning
- TensorFlow & Keras

### Model Architecture

#### Encoder

- Input Layer (28 × 28 × 1)
- Convolutional Layers
- Max Pooling Layers
- Bottleneck (Latent Space)

#### Decoder

- Convolutional Layers
- UpSampling Layers
- Sigmoid Output Layer
- Image Reconstruction

### Workflow

- Load and preprocess the MNIST dataset.
- Normalize pixel values.
- Add Gaussian noise to training and testing images.
- Build a Convolutional Denoising Autoencoder.
- Train the model using noisy images as input and clean images as target.
- Generate denoised outputs on the test set.
- Compare original, noisy, and reconstructed images.
- Analyze reconstruction performance using training and validation loss curves.

### Key Results

- Successfully removed Gaussian noise from handwritten digit images.
- Preserved the digit structure while reconstructing clean images.
- Generated clear comparisons between Original, Noisy, and Denoised images.
- Achieved effective reconstruction using a Convolutional Autoencoder.
- Visualized training and validation loss for model evaluation.

### Skills Learned

- Autoencoders
- Image Denoising
- Representation Learning
- Feature Extraction
- Convolutional Neural Networks (CNN)
- Encoder–Decoder Networks
- Computer Vision
- Deep Learning
- TensorFlow & Keras

---

# 📂 Week 7

## Project

**ScrollMind AI — RAG-Based Document Question Answering System**

🔗 **Live App:** [scrollmindai.streamlit.app](https://scrollmindai.streamlit.app/)

### Project Description

Built a full-stack **Retrieval-Augmented Generation (RAG)** chatbot that lets users upload PDFs and ask questions grounded in their content, with **native inline citations** pointing to the exact document chunk that supports each part of the answer. Combines **Cohere** (embeddings + grounded generation) with **Pinecone** (vector search) behind a dark-themed **Streamlit** chat interface.

### Topics Covered

- Retrieval-Augmented Generation (RAG)
- Large Language Models (LLMs)
- Vector Embeddings
- Vector Databases
- Semantic Search
- Prompt Engineering
- Grounded Generation & Citations
- PDF Text Extraction
- Text Chunking Strategies
- Session Management
- Full-Stack AI App Deployment

### Architecture

```
PDF Upload (Streamlit)
        │
        ▼
Text Extraction (PyMuPDF)
        │
        ▼
Chunking (overlapping word-based chunks)
        │
        ▼
Embedding (Cohere embed-english-v3.0, 1024-dim)
        │
        ▼
Vector Storage (Pinecone serverless index, per-session namespace)
        │
   [User Question]
        │
        ▼
Query Embedding → Pinecone similarity search (top-k)
        │
        ▼
Grounded Generation (Cohere command-r-plus, with `documents=` param)
        │
        ▼
Answer + Inline Citations + Source Chunks (Streamlit chat UI)
```

### Key Features

- Grounded answers using Cohere's Chat API `documents` parameter for fine-grained inline citations.
- Multi-document support with per-source metadata tagging.
- Session-scoped Pinecone namespaces so documents from different sessions never mix.
- Transparent retrieval — every answer includes an expandable panel showing the exact chunks and similarity scores used.
- Downloadable chat history as `.txt`.
- Deployed live on Streamlit Community Cloud.

### Skills Learned

- Retrieval-Augmented Generation (RAG)
- LLM Application Development
- Vector Embeddings & Semantic Search
- Pinecone Vector Database
- Cohere API (Embeddings + Chat)
- Prompt Engineering
- Full-Stack AI App Design
- Streamlit Deployment

---

# 📂 Week 8

## Project

**Single-Agent Smart Assistant — Agentic AI Pipeline**

### Project Description

Built a **single-agent smart assistant** that understands user queries, applies conditional routing based on intent, and dispatches to the appropriate tool — returning a consistent, structured JSON output for every response. The project demonstrates core agentic AI concepts: intent-based routing, tool integration, and defensive error handling, all within a single-agent architecture that internally simulates multi-step agent behavior.

### Topics Covered

- Agentic AI Fundamentals
- Single-Agent Architecture
- Conditional / Intent-Based Routing
- Tool Integration & Tool Calling
- Structured JSON Output Design
- Error Handling in Agent Pipelines
- Logging for Agent Observability

### Tools Implemented

#### Calculator Tool

- Evaluates mathematical expressions extracted from natural language queries
- Returns computed result or a graceful error on invalid expressions

#### Keyword Extractor Tool

- Extracts up to 5 significant keywords (length > 4 characters) from input text
- Deduplicates and lowercases extracted terms

### Agent Routing Logic

```
User Query
    │
    ▼
Contains "calculate"? ──Yes──▶ Calculator Tool ──▶ {"type": "calculation", "result": ...}
    │
    No
    ▼
Contains "keywords"? ──Yes──▶ Keyword Extractor Tool ──▶ {"type": "keywords", "result": [...]}
    │
    No
    ▼
General Response ──▶ {"type": "general", "result": ...}

(Any failure at any stage) ──▶ {"type": "error", "result": "..."}
```

### Key Features

- Rule-based conditional routing across 3 query types (math, keyword extraction, general).
- Consistent structured JSON schema (`type` + `result`) across every response path.
- Top-level exception handling so the agent degrades gracefully instead of crashing.
- Bonus: Python `logging` module integrated for step-by-step observability (query received → tool routed → result returned).
- Interactive CLI mode for live query testing alongside batch test cases.

### Key Results

- Verified correct routing across all test queries (calculation, keyword extraction, general).
- Achieved consistent structured output across all 4 response types (`calculation`, `keywords`, `general`, `error`).

### Skills Learned

- Agentic AI Design
- Conditional Routing Logic
- Tool-Calling Patterns
- JSON Schema Design for Agent I/O
- Error Handling & Resilience
- Agent Observability / Logging

---

# 🎯 Final Project

## HireSense AI — Intelligent Hiring Assistant

📁 **Project Folder:** [`final_project/`](./final_project)

### Project Description

An end-to-end, full-stack **AI Hiring Assistant** that evaluates candidate resumes against job requirements using a combination of machine learning and deep learning models, then generates personalized, explainable feedback through a retrieval-based intelligent text generation pipeline. The system also features a conversational interface for candidates to interact with and understand their evaluation results.

Built as the capstone project for the JECRC–Celebal Excellence internship, this project combines every major skill developed across the internship — NLP, deep learning embeddings, ensemble ML, RAG, and full-stack deployment — into a single production-style application.

### Topics Covered

- Resume Parsing & Skill Extraction (spaCy)
- Semantic Similarity with Sentence Embeddings
- Hybrid ML Scoring (Deep Learning + Gradient Boosting)
- Retrieval-Augmented Generation (RAG)
- Vector Search with FAISS
- LLM-Powered Explainable Feedback (Google Gemini)
- Conversational AI Interfaces
- Authentication & Session Security (JWT, bcrypt)
- Full-Stack Application Architecture (FastAPI + React)
- Cloud Database Integration (MongoDB Atlas)

### Architecture

```
Resume Upload (React / Vite frontend)
        │
        ▼
Text & Skill Extraction (spaCy, pypdf, docx2txt)
        │
        ▼
Semantic Embedding (sentence-transformers: all-MiniLM-L6-v2)
        │
        ▼
Hybrid Scoring Engine
   ├── Semantic similarity (cosine similarity)
   └── XGBoost ranking probability (skill match features)
        │
        ▼
Missing Skills Identified
        │
        ▼
RAG Feedback Pipeline
   ├── FAISS vector store (resume as document)
   ├── Gemini embeddings (gemini-embedding-001)
   └── Gemini LLM (gemini-flash-latest) via LangChain RetrievalQA
        │
        ▼
Explainable, Personalized Feedback + Score (FastAPI → React UI)
```

### Key Features

- **Hybrid Scoring Engine** — combines sentence-embedding semantic similarity with a trained XGBoost classifier for robust, explainable candidate ranking.
- **RAG-Based Explainable Feedback** — uses FAISS retrieval + Gemini generation to produce actionable, personalized feedback on missing skills rather than a black-box score.
- **Conversational Interface** — a chatbot panel lets candidates ask follow-up questions about their evaluation.
- **Evaluation History** — every scan is persisted to MongoDB Atlas and viewable per user.
- **Secure Authentication** — JWT-based sessions with bcrypt password hashing.
- **Full-Stack, Deployment-Ready Architecture** — FastAPI backend with interactive Swagger docs, React (Vite) frontend, Dockerized for containerized deployment.

### Tech Stack

| Layer | Technology |
|---|---|
| Backend | FastAPI, Python 3.11 |
| Frontend | React, Vite |
| Database | MongoDB Atlas |
| Embeddings | sentence-transformers (`all-MiniLM-L6-v2`) |
| ML Ranking | XGBoost |
| RAG / Vector Store | FAISS, LangChain |
| LLM | Google Gemini (`gemini-flash-latest`, `gemini-embedding-001`) |
| Auth | JWT, bcrypt |

### Key Results

- Verified end-to-end pipeline: registration → login → resume upload → hybrid scoring → RAG-based feedback → evaluation history, all working locally against a live MongoDB Atlas cluster and the Gemini API.
- Dataset reference for the ranking model: [Resume Dataset (Kaggle)](https://www.kaggle.com/datasets/rayyankauchali0/resume-dataset).

### Skills Learned

- Full-Stack AI Application Development
- Retrieval-Augmented Generation (RAG)
- Hybrid ML/DL Scoring Systems
- LLM Integration & Prompt-Grounded Generation
- Vector Search (FAISS)
- Authentication & API Security
- FastAPI + React Integration
- Cloud Database Design (MongoDB Atlas)

📄 See [`final_project/README.md`](./final_project/README.md) for full setup instructions and screenshots.

---

# 🛠️ Technologies & Libraries Used

- Python
- NumPy
- Pandas
- Matplotlib
- Seaborn
- Scikit-Learn
- TensorFlow
- Keras
- OpenCV
- XGBoost
- Statsmodels
- Jupyter Notebook
- Cohere
- Pinecone
- Streamlit
- PyMuPDF
- FastAPI
- React / Vite
- MongoDB Atlas
- LangChain
- FAISS
- Google Gemini API
- sentence-transformers
- spaCy

---

# 📈 Skills Developed During Internship

- Python Programming
- Data Analysis
- Statistical Analysis
- Data Visualization
- Machine Learning
- Deep Learning
- Computer Vision
- Natural Language Processing
- Time Series Forecasting
- Clustering
- Classification
- Ensemble Learning
- Feature Engineering
- Hyperparameter Tuning
- Model Evaluation
- TensorFlow & Keras
- Autoencoders
- Image Denoising
- Representation Learning
- Feature Extraction
- Retrieval-Augmented Generation (RAG)
- Vector Databases
- LLM Application Development
- Agentic AI Design
- Tool-Calling & Conditional Routing
- Full-Stack AI Application Development
- Hybrid ML/DL Scoring Systems
- Authentication & API Security

---

# 🚀 Future Learning Goals

- Variational Autoencoders (VAEs)
- Generative Adversarial Networks (GANs)
- Diffusion Models
- Transformers
- BERT & GPT Models
- LangChain
- LangGraph
- Agentic AI
- MLOps
- Cloud AI Solutions
- Advanced Large Language Model (LLM) Fine-Tuning

---

# ⭐ Internship Journey

This repository showcases my learning journey as a **Celebal Excellence Intern (CEI)**, highlighting practical implementations across **Data Science, Machine Learning, Deep Learning, Computer Vision, Time Series Forecasting, Natural Language Processing, and Generative AI** through hands-on projects and real-world problem solving.

Each week's project reflects progressive learning—from Python fundamentals and machine learning to deep learning, NLP, computer vision, autoencoders, and modern Generative AI concepts, culminating in the **Final Project: HireSense AI**, a deployment-ready full-stack AI hiring assistant that brings together RAG, hybrid ML scoring, and conversational AI into one complete application.

If you find this repository helpful, feel free to ⭐ **Star** the repository.

Happy Coding! 🚀
