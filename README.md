# Legal QA System with Knowledge Graphs ⚖️🧠

## LLM-Powered Question Answering for the Moroccan Legal Market

**QA System with Knowledge Graphs** is an AI-powered **Question Answering system designed to retrieve and explain information about the Moroccan legal market** using a combination of **Local Large Language Models, Knowledge Graphs, Neo4j, and Natural Language Processing**.

Instead of asking an LLM to answer directly from its own learned knowledge, the system first identifies relevant entities from the user's question, retrieves their relationships from a **Neo4j Knowledge Graph**, and then uses a **local Llama 3 model through Ollama** to transform the retrieved graph information into a natural-language answer in French.

This architecture combines the flexibility of LLMs with the structure and traceability of graph-based knowledge retrieval.

---

## 🎯 Project Overview

Legal information is naturally interconnected.

A company can be associated with a legal activity, a profession can be governed by a regulation, an organization can have relationships with other entities, and legal concepts can be connected through multiple relationships.

A traditional keyword search can struggle to represent these connections.

This project addresses the problem by representing legal-domain knowledge as a **Knowledge Graph**, where:

```text
Entities ── Relationships ── Entities
```

are stored and queried through **Neo4j**.

The LLM is then used for **natural-language understanding and answer generation**, while Neo4j acts as the structured knowledge source.

---

## 🧠 Core Architecture

The system follows a simple but powerful **LLM → Knowledge Graph → LLM** pipeline:

```text
                    User Question
                          │
                          ▼
              ┌─────────────────────┐
              │      Flask Web App  │
              └──────────┬──────────┘
                         │
                         ▼
              ┌─────────────────────┐
              │   Local LLM / Llama3│
              │  Entity Extraction  │
              └──────────┬──────────┘
                         │
                    Named Entities
                         │
                         ▼
              ┌─────────────────────┐
              │       Neo4j         │
              │   Knowledge Graph   │
              └──────────┬──────────┘
                         │
                  Graph Relations
                         │
                         ▼
              ┌─────────────────────┐
              │   Local LLM / Llama3│
              │   Answer Generation │
              └──────────┬──────────┘
                         │
                         ▼
                  Natural Language
                       Answer
```

The architecture separates **knowledge retrieval** from **language generation**, allowing the LLM to work with information retrieved from a structured domain-specific graph.

---

## 🔍 How the System Works

### 1. User submits a question

The user asks a question in natural language through the web interface.

The application is designed around **French-language questions**, making it suitable for querying the legal information represented in the project knowledge graph.

### 2. Entity Extraction

The question is sent to the locally running **Llama 3 model through Ollama**.

The model is prompted specifically to identify the named entities contained in the question and return them in JSON format.

For example:

```json
{
  "entities": [
    "Entity A",
    "Entity B"
  ]
}
```

This converts an unstructured natural-language question into structured entities that can be used for graph retrieval.

### 3. Knowledge Graph Retrieval

The extracted entities are then used to query **Neo4j**.

The system traverses relationships around the identified entities using Cypher:

```cypher
MATCH (n)-[r]-(m)
WHERE n.id = $entity
RETURN n.id AS node,
       type(r) AS relation,
       m.id AS neighbor
```

The result is a collection of graph relationships such as:

```text
Entity A ──[RELATIONSHIP]──> Entity B
```

This allows the system to retrieve structured information connected to the entities mentioned in the user's question.

### 4. Graph Data Formatting

The retrieved relationships are transformed into readable statements.

For example:

```text
'Entity A' related_to 'Entity B'.
'Entity B' belongs_to 'Entity C'.
```

This creates a textual representation of the graph context.

### 5. Answer Generation

The retrieved graph information is passed back to **Llama 3 through Ollama**.

The model is instructed to transform the graph relationships into a clear and natural answer in French.

This creates the final response shown to the user.

---

## 🤖 Why Use a Knowledge Graph?

The project is based on an important principle:

> **Let the Knowledge Graph provide the structured facts, and let the LLM provide the language understanding and generation.**

The graph provides explicit relationships between entities, while the LLM provides the flexibility required to understand natural-language questions and communicate the retrieved information.

This is particularly useful for domains such as legal information, where relationships between entities can be as important as the entities themselves.

---

## 🧩 Key Features

### ⚖️ Legal-Domain Question Answering

The system is specialized around information related to the **Moroccan legal market**, rather than functioning as a generic chatbot.

### 🧠 Local LLM Processing

The project uses **Llama 3 locally through Ollama**, avoiding the need to send questions to a hosted LLM API.

This provides a foundation for privacy-oriented and locally controlled AI applications.

### 🕸️ Knowledge Graph Retrieval

Legal-domain entities and their relationships are represented in **Neo4j**, enabling structured graph traversal.

### 🔎 Entity-Based Search

The system extracts relevant entities from natural-language questions before querying the graph.

### 🗣️ Natural-Language Answer Generation

Raw graph relationships are transformed into readable French answers using the local LLM.

### 🌐 Web Interface

A Flask web application provides the user-facing interface for submitting questions and displaying:

* User question
* Extracted entities
* Retrieved graph information
* Formatted graph relationships
* Generated answer

---

## 🏗️ Technology Stack

| Technology           | Role                                    |
| -------------------- | --------------------------------------- |
| **Python**           | Application and AI pipeline             |
| **Flask**            | Web application and request handling    |
| **Ollama**           | Local LLM runtime                       |
| **Llama 3**          | Entity extraction and answer generation |
| **Neo4j**            | Knowledge Graph database                |
| **Cypher**           | Graph querying                          |
| **JSON**             | Structured entity extraction            |
| **HTML/CSS**         | User interface                          |
| **Knowledge Graphs** | Structured legal-domain knowledge       |

---

## 🔄 End-to-End Pipeline

```text
Natural Language Question
          │
          ▼
      Flask App
          │
          ▼
    Llama 3 / Ollama
          │
          ▼
    Entity Extraction
          │
          ▼
      Named Entities
          │
          ▼
        Neo4j
          │
          ▼
   Graph Relationships
          │
          ▼
  Graph Context Formatting
          │
          ▼
    Llama 3 / Ollama
          │
          ▼
  Natural Language Answer
```

This architecture is effectively a lightweight **Knowledge-Graph-Augmented Question Answering pipeline**.

---

## 🕸️ Knowledge Graph Layer

The project includes a dedicated `KGs/` directory containing the knowledge-graph resources used by the application.

The graph represents domain information as connected entities and relationships, allowing the QA system to retrieve information based on the structure of the underlying knowledge rather than relying exclusively on text matching.

At runtime, Neo4j is accessed through the official Python Neo4j driver:

```python
from neo4j import GraphDatabase
```

The application connects to the Neo4j Bolt interface:

```text
bolt://localhost:7687
```

and performs graph traversal queries against the stored knowledge.

---

## 🔎 Entity Resolution

The project also includes an alternative retrieval approach using a **Neo4j full-text index**.

The implementation can search across:

```text
id
name
description
```

before traversing the relationships of matching nodes.

The intended purpose is to make entity retrieval more flexible when the user's wording does not exactly match the stored entity identifier.

This is an important component for natural-language interfaces because users rarely formulate entity names exactly as they appear in a database.

---

## 🧠 Local AI Architecture

One of the defining characteristics of this project is that the LLM layer runs locally.

The application communicates with Ollama:

```python
ollama.chat(
    model="llama3",
    messages=[...]
)
```

The model is used for two separate tasks:

### Entity Extraction

```text
Question
   ↓
Llama 3
   ↓
Named Entities
   ↓
JSON
```

### Answer Generation

```text
Neo4j Graph Data
       ↓
    Llama 3
       ↓
Natural Language Answer
```

This separation allows the LLM to act as both a **semantic interface** and a **natural-language generation layer**, while Neo4j remains responsible for structured knowledge retrieval.

---

## 📁 Project Structure

```text
QA-System-with-Knowledge-Graphs/
│
├── KGs/
│   └── Knowledge Graph resources
│
├── static/
│   └── Frontend static assets
│
├── templates/
│   └── Flask HTML templates
│
├── run.py
│   └── Flask application
│       ├── Ollama / Llama 3 integration
│       ├── Entity extraction
│       ├── Neo4j connection
│       ├── Graph querying
│       ├── Graph formatting
│       └── Answer generation
│
├── Project Presentation.pptx
│
└── QA System with Knowledge Graphs - Project Report.docx
```

The repository contains both the implementation and the accompanying academic project documentation.

---

## 🚀 Getting Started

### Prerequisites

The application requires:

* Python 3.x
* Flask
* Neo4j
* Ollama
* Llama 3
* Python Neo4j driver

---

### 1. Clone the Repository

```bash
git clone https://github.com/SALAH-EO/QA-System-with-Knowledge-Graphs.git
cd QA-System-with-Knowledge-Graphs
```

### 2. Install Python Dependencies

Install the required packages used by the application:

```bash
pip install flask
pip install markupsafe
pip install ollama
pip install neo4j
```

Or install them from a project requirements file if you add one to the repository.

---

### 3. Install and Run Ollama

Install Ollama and make sure the local service is running.

Then pull the Llama 3 model:

```bash
ollama pull llama3
```

Verify that the model is available:

```bash
ollama list
```

---

### 4. Start Neo4j

Start a local Neo4j database and make sure the Bolt interface is available:

```text
bolt://localhost:7687
```

The current application configuration expects:

```text
Host: localhost
Port: 7687
```

The Neo4j credentials should be configured locally before running the application.

> **Security note:** Database credentials should never be committed directly to a public repository. For a production-ready version, use environment variables such as `NEO4J_URI`, `NEO4J_USER`, and `NEO4J_PASSWORD`.

---

### 5. Load the Knowledge Graph

The knowledge graph resources included in the `KGs/` directory should be available in the Neo4j instance used by the application.

Once the graph is populated, the application can retrieve relationships associated with extracted entities.

---

### 6. Run the Application

Start the Flask application:

```bash
python run.py
```

The application runs on:

```text
http://127.0.0.1:5002
```

Open the address in a browser and submit a question about the legal-domain knowledge represented in the graph.

---

## 💬 Example Interaction

A simplified interaction looks like:

```text
User:
"Quels sont les liens entre [Entity A] et [Entity B] ?"

                ↓

Llama 3
Entity Extraction

                ↓

["Entity A", "Entity B"]

                ↓

Neo4j
Graph Traversal

                ↓

Entity A
    │
    ├── RELATIONSHIP → Entity B
    └── RELATIONSHIP → Entity C

                ↓

Llama 3
Answer Generation

                ↓

Natural-language response in French
```

---

## 🧱 Architecture Principles

### Structured Knowledge + Generative AI

The project combines two complementary approaches:

```text
Knowledge Graph
     │
     │ Structured facts
     ▼
   Neo4j
     │
     │ Retrieved context
     ▼
    LLM
     │
     │ Natural language
     ▼
   Answer
```

The graph is responsible for **structured retrieval**, while the LLM is responsible for **language understanding and generation**.

### Local-First AI

Using Ollama allows the LLM component to run locally instead of depending on a remote commercial API.

### Domain-Specific QA

The system is built around a specific knowledge domain, allowing the graph to encode relationships that are meaningful for the target use case.

---

## 💡 Engineering Challenges Addressed

This project explores several practical challenges encountered when building domain-specific AI systems:

### Natural Language → Structured Knowledge

Users ask questions naturally, while graph databases require structured entities and queries.

The entity extraction stage acts as the bridge between the two.

### Entity Matching

User terminology does not always exactly match database identifiers.

The project therefore explores full-text entity indexing as an alternative retrieval mechanism.

### Graph-Based Retrieval

Instead of retrieving isolated documents, the system retrieves **relationships between entities**, allowing connected domain information to be surfaced.

### LLM Grounding

Rather than asking the LLM to generate an answer solely from its pretrained knowledge, graph information is provided as context for answer generation.

---

## 🎓 Academic Context

This project was developed as an **academic exploration of Knowledge Graphs and Question Answering systems**, with a practical application to the **Moroccan legal market**.

The project combines concepts from:

* Natural Language Processing
* Large Language Models
* Knowledge Representation
* Knowledge Graphs
* Graph Databases
* Question Answering
* Information Retrieval
* Generative AI

The repository includes the project's **technical report and presentation** documenting the work.

---

## 👨‍💻 Author

**Salah Eddine Ouirra**

**Data Science & Big Data | AI Engineering | LLMs | Knowledge Graphs | Intelligent Systems**

**Portfolio:** https://salah-eo.vercel.app
