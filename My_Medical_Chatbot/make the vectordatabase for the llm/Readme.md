# AI Medical Chatbot - Vector Database

This folder creates a FAISS vector database from medical dialogue data for use in a Retrieval-Augmented Generation (RAG) medical chatbot.

## Directory Structure

```
8-Interviewer/
├── 2-Data.ipynb              # Processes raw dialogue data
├── 3-Compression.ipynb       # Compresses data to Parquet
├── dialogues_embededd.pkl    # Embedded dialogue data
├── faiss.py                  # Creates FAISS vector database
├── tools/
│   ├── Notes.txt             # Clinical procedure notes
│   ├── timer.py              # Timer utility
```

## Prerequisites

- Python 3.8+
- Libraries: `pandas numpy langchain-community langchain-openai faiss-cpu python-dotenv tqdm`
- OpenAI API key in `.env`

## Setup

1. **Clone & Navigate**
   ```bash
   git clone https://github.com/Kaustubh-Rathi/ai-medical-chatbot-master.git
   cd ai-medical-chatbot-master/8-Interviewer
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set API Key**
   ```
   OPENAI_API_KEY=your-key  # In .env
   ```

## Usage

1. **Process Data**: Run `2-Data.ipynb` to generate `dialogues.csv`.
2. **Compress Data**: Run `3-Compression.ipynb` for `dialogues.parquet`.
3. **Create Vector DB**: Run `faiss.py` to build and save the FAISS index:
   ```bash
   python faiss.py
   ```
   Outputs: `knowledge/embeddings.npy`, `knowledge/faiss_index_all_documents`.

## Output

- Vector database for RAG, using OpenAI embeddings from `dialogues_embededd.pkl`.

## Notes

- Data sourced from [healthcaremagic.com](https://healthcaremagic.com) and [icliniq.com](https://icliniq.com).

--- 

### GitHub Upload

1. **`.gitignore`**:
   ```
   *.csv
   *.parquet
   *.pkl
   knowledge/
   .env
   ```

2. **Push**:
   ```bash
   git add .
   git commit -m "Vector DB for RAG"
   git push origin master
   ```
