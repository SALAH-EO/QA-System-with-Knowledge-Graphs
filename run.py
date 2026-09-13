from flask import Flask, render_template, request
from markupsafe import Markup
import ollama
import json
import re
from neo4j import GraphDatabase

# Initialize Flask app
app = Flask(__name__)

# Neo4j connection details
NEO4J_URI = "bolt://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "Salah123456"

# Establish connection to Neo4j
driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

def query_graph(entities):
    with driver.session() as session:
        results = []
        for entity in entities:
            query = """
            MATCH (n)-[r]-(m) 
            WHERE n.id = $entity
            RETURN n.id AS node, type(r) AS relation, m.id AS neighbor
            """
            records = session.run(query, entity=entity)
            results.extend([f"{rec['node']} -[{rec['relation']}]-> {rec['neighbor']}" for rec in records])

        return results if results else ["No results found."]


# To include entity names that don't match exactly , we'll use Full-Text Index

'''        CREATE FULLTEXT INDEX fulltext_entity_index
        FOR (n:__Entity__) ON EACH [n.id, n.name, n.description]'''


def query_graph_with_index(entities):
    with driver.session() as session:
        results = []
        for entity in entities:
            query = """
            CALL db.index.fulltext.queryNodes('fulltext_entity_index', $search_term, {limit: 5})
            YIELD node, score
            MATCH (node)-[r]-(m)
            RETURN node.id AS entity, type(r) AS relation, m.id AS related_entity
            """
            records = session.run(query, search_term=entity.strip())
            results.extend([f"'{rec['entity']}' -[{rec['relation']}]-> '{rec['related_entity']}'" for rec in records])
        return results if results else ["Aucune correspondance trouvée."]

def extract_entities(question):
    prompt = f"""
    Vous êtes un assistant spécialisé dans l'extraction d'entités nommées à partir de questions en français.
    Extraire les entités nommées à partir du question suivant.

    **Format attendu (JSON valide) :**
    {{"entities": ["Entité1", "Entité2"]}}

    **Question :** "{question}"
    Donnez uniquement la réponse sous forme de JSON sans texte supplémentaire.
    """
    
    response = ollama.chat(model="llama3", messages=[{"role": "user", "content": prompt}])
    
    json_match = re.search(r'\{.*\}', response.message.content, re.DOTALL)
    if json_match:
        try:
            extracted_data = json.loads(json_match.group())
            return extracted_data.get("entities", [])
        except json.JSONDecodeError:
            return []

    return []

def generate_answer(graph_data):
    prompt = f"""
    Vous êtes un assistant intelligent. Reformulez les informations suivantes sous forme d'un texte fluide et naturel en français.

    Voici les relations extraites du graphe :
    {graph_data}

    Fournissez une réponse (sans introductions et sans commentaires) claire et bien structurée en français, adaptée à un utilisateur humain.
    """

    response = ollama.chat(model="llama3", messages=[{"role": "user", "content": prompt}])

    return response["message"]["content"]

def format_graph_data(graph_data):
    formatted_sentences = []
    
    for entry in graph_data:
        parts = entry.split(" -[")
        if len(parts) == 2:
            node, rest = parts
            relation, neighbor = rest.split("]-> ")
            readable_relation = relation.replace("_", " ").lower()
            formatted_sentences.append(f"'{node}' {readable_relation} '{neighbor}'.")
    
    return "<br>".join(formatted_sentences)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        question = request.form['question']
        print(question)
        entities = extract_entities(question)
        print(entities)
        graph_data = query_graph(entities)
        # print(graph_data)
        formatted_answer = format_graph_data(graph_data)
        print(formatted_answer)
        
        # Generate answer using Ollama 
        answer = generate_answer(graph_data)  
        
        return render_template('index.html', question=question, entities=entities, graph_data=graph_data, formatted_answer=Markup(formatted_answer) , answer=answer)

    return render_template('index.html')

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5002)
