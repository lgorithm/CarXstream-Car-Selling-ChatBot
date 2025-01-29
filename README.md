# 🚗 Car Selling AI Agent

## 📌 Overview

This project is an AI-powered car selling agent that interacts with a **SQL database** to provide information about used cars. Users can ask queries like:

> *"How many Honda cars are available?"*

The agent processes user queries using **LangChain**, **OpenAI GPT models**, and **LangGraph**, making it capable of dynamically fetching and processing database records.

---

## 🛠️ Technologies Used

- **LangChain** (LLM integration & tool handling)
- **Streamlit** (For UI)
- **OpenAI GPT-4o Mini** (AI-powered query resolution)
- **SQLite** (Database management)
- **SQLAlchemy** (Database connectivity & ORM)
- **Python** (Core development)
- **Poetry** (Package Management)

---

## 📂 Project Structure

```
├── Agents/
│   ├── buy.py  # React Agent from LangChain
│
├── DB/
│   ├── car_data.db  # SQLite Database storing used car details
│
├── Prompts/
│   ├── buy.py  # System prompt for the agent
│
├── tools/
│   ├── sql_database.py  # SQL database integration & toolkit setup
│
├── user.py  # UI for interacting to the Agent
├── admin.py  # UI for showing available car list
├── app.py  # starting point of Streamlit App 
├── .env  # API keys and environment variables
```

---

## 🚀 How It Works

1. **Database Connection**
   - The system uses **SQLite** to store and retrieve car details.
2. **AI Agent Workflow**
   - Queries are processed using **GPT-4o Mini** with **LangChain & LangGraph**.
   - The **SQLDatabaseToolkit** is used to fetch relevant car data.
3. **User Interaction**
   - Users can ask about car availability, pricing, models, colors, etc.

---

## 🔧 Setup Instructions

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/lgorithm/Car-Selling-Agent.git
cd car-selling-agent
```

### 2️⃣ Install Dependencies

```bash
poetry install
```

### 3️⃣ Set Up Environment Variables

Create a `.env` file and add your OpenAI API key:

```bash
OPENAI_API_KEY=your_api_key_here
```

### 4️⃣ Run the Agent

```bash
poetry run streamlit run app.py
```

---

## 📌 Example Queries

- "How many Honda cars are available?"
- "Show me all diesel cars under ₹5 lakhs."
---


