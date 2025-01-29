# 🚗 Car Selling AI Agent

## 📌 Overview

This project is an AI-powered car selling agent that interacts with a **SQL database** to provide information about used cars. Users can ask queries like:

> *"How many Ford cars are available that are red in color?"*

The agent processes user queries using **LangChain**, **OpenAI GPT models**, and **LangGraph**, making it capable of dynamically fetching and processing database records.

---

## 🛠️ Technologies Used

- **LangChain** (LLM integration & tool handling)
- **LangGraph** (Agent workflow management)
- **OpenAI GPT-4o Mini** (AI-powered query resolution)
- **SQLite** (Database management)
- **SQLAlchemy** (Database connectivity & ORM)
- **Python** (Core development)

---

## 📂 Project Structure

```
├── DB/
│   ├── car_data.db  # SQLite Database storing used car details
│
├── Prompts/
│   ├── buy.py  # System prompt for the agent
│
├── tools/
│   ├── sql_database.py  # SQL database integration & toolkit setup
│
├── buy.py  # AI Agent implementation using LangGraph
├── sql_database.py  # SQL toolkit and database connectivity setup
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
git clone https://github.com/yourusername/car-selling-agent.git
cd car-selling-agent
```

### 2️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 3️⃣ Set Up Environment Variables

Create a `.env` file and add your OpenAI API key:

```bash
OPENAI_API_KEY=your_api_key_here
```

### 4️⃣ Run the Agent

```bash
python buy.py
```

---

## 📌 Example Queries

- "How many Honda cars are available?"
- "Show me all diesel cars under ₹5 lakhs."
- "List all available SUVs with less than 50,000 km driven."

---

## 📧 Contact & Contribution

Feel free to contribute to the project! If you have any suggestions or issues, reach out via **GitHub Issues**.

📩 **Email**: [your.email@example.com](mailto\:your.email@example.com)\
📝 **GitHub**: [yourusername](https://github.com/yourusername)

