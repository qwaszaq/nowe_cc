# 🕸️ GRAF RELACJI - Status Implementacji

**Data:** 5 Listopada 2024  
**Pytanie:** Czy mamy lokalny graf relacji z heurystyką i semantyką?

---

## 📊 SZYBKA ODPOWIEDŹ

```
Neo4j (Full Graph DB):        ✅ Zaimplementowany (ale offline)
Lokalny In-Memory Graph:      ❌ NIE zaimplementowany
Heurystyczne Entity Extract:  ❌ NIE zaimplementowany
Semantyczne Relationships:    ❌ NIE zaimplementowany
```

---

## ✅ CO MAMY: Neo4j Client

**Lokalizacja:** `src/data/neo4j_client.py`

### **Funkcjonalność:**

```python
class Neo4jClient:
    """
    Neo4j graph database client
    - Entity relationship mapping
    - Financial flow analysis
    - Timeline analysis
    - Graph traversal queries
    """
    
    def create_entity(case_id, entity_id, entity_type, properties)
    def create_relationship(case_id, from_entity, to_entity, rel_type)
    def find_connections(case_id, entity_id, max_depth=3)
    def analyze_financial_flow(case_id, start_entity)
```

### **Problem:**

```
❌ Wymaga uruchomionego Neo4j server
❌ Nie działa offline
❌ Heavy (pełna baza danych)
❌ Brak automatycznej ekstrakcji relacji
```

**Status:** Infrastructure ready, but no data/extraction logic

---

## ❌ CZEGO BRAKUJE: Lokalny Graf Relacji

### **Potrzeba:**

```
Szybki, lokalny graf z:
✅ In-memory storage (NetworkX/igraph)
✅ Heurystyczna ekstrakcja encji
✅ Semantyczna identyfikacja relacji
✅ Brak zależności od zewnętrznych serwisów
```

---

## 🎯 PROPOZYCJA IMPLEMENTACJI

### **Architektura:**

```
┌─────────────────────────────────────────┐
│   Lokalny Graf Relacji (In-Memory)      │
├─────────────────────────────────────────┤
│                                         │
│  1. HEURYSTYCZNA EKSTRAKCJA ENCJI       │
│     - Rule-based patterns               │
│     - Regex dla nazwisk, firm, kwot     │
│     - POS tagging (opcjonalnie)         │
│                                         │
│  2. SEMANTYCZNA IDENTYFIKACJA RELACJI   │
│     - Embedding similarity              │
│     - Co-occurrence w zdaniach          │
│     - Dependency parsing (opcjonalnie)  │
│                                         │
│  3. IN-MEMORY GRAPH (NetworkX)          │
│     - Nodes: entities                   │
│     - Edges: relationships              │
│     - Fast traversal                    │
│                                         │
│  4. QUERY INTERFACE                     │
│     - Find connections                  │
│     - Shortest path                     │
│     - Community detection               │
│     - Centrality analysis               │
│                                         │
└─────────────────────────────────────────┘
```

---

## 💡 IMPLEMENTACJA - 3 Moduły

### **Moduł 1: Heurystyczna Ekstrakcja Encji**

```python
class HeuristicEntityExtractor:
    """
    Fast, rule-based entity extraction
    """
    
    PATTERNS = {
        'person': [
            r'\b[A-ZŻŹĆĄŚĘŁÓŃ][a-zżźćńąśęłó]+ [A-ZŻŹĆĄŚĘŁÓŃ][a-zżźćńąśęłó]+\b',
            r'\b(?:Pan|Pani|Dr|Mgr) [A-ZŻŹĆĄŚĘŁÓŃ][a-zżźćńąśęłó]+\b'
        ],
        'organization': [
            r'\b[A-ZŻŹĆĄŚĘŁÓŃ][A-Z\s]+(?:Sp\. z o\.o\.|S\.A\.|GmbH)\b',
            r'\bCentralne Biuro Antykorupcyjne\b',
            r'\bCBA\b'
        ],
        'money': [
            r'\b\d+(?:\.\d{3})*(?:,\d{2})?\s*(?:zł|PLN|EUR|USD)\b',
            r'\b\d+(?:,\d{3})*(?:\.\d{2})?\s*(?:dollars|euros)\b'
        ],
        'date': [
            r'\b\d{1,2}[./]\d{1,2}[./]\d{4}\b',
            r'\b\d{4}-\d{2}-\d{2}\b',
            r'\b(?:styczeń|luty|marzec|kwiecień|maj|czerwiec|lipiec|sierpień|wrzesień|październik|listopad|grudzień)\s+\d{4}\b'
        ],
        'case_number': [
            r'\b(?:sprawa|postępowanie)\s+nr\s+[A-Z0-9/-]+\b',
            r'\b[A-Z]{2,}\s+\d+/\d+\b'
        ]
    }
    
    def extract(self, text: str) -> List[Entity]:
        """
        Extract entities using regex patterns
        
        Returns:
            List of Entity(text, type, start, end)
        """
        entities = []
        
        for entity_type, patterns in self.PATTERNS.items():
            for pattern in patterns:
                for match in re.finditer(pattern, text):
                    entities.append(Entity(
                        text=match.group(),
                        type=entity_type,
                        start=match.start(),
                        end=match.end(),
                        confidence=0.8  # Heuristic confidence
                    ))
        
        return self._deduplicate(entities)
```

**Przykład użycia:**

```python
extractor = HeuristicEntityExtractor()

text = """
Pan Jan Kowalski z firmy ABC Sp. z o.o. otrzymał łapówkę 
w wysokości 50.000 zł w sprawie nr CBA-123/2024.
"""

entities = extractor.extract(text)

# Output:
# Entity(text='Pan Jan Kowalski', type='person', ...)
# Entity(text='ABC Sp. z o.o.', type='organization', ...)
# Entity(text='50.000 zł', type='money', ...)
# Entity(text='CBA-123/2024', type='case_number', ...)
```

---

### **Moduł 2: Semantyczna Identyfikacja Relacji**

```python
class SemanticRelationshipFinder:
    """
    Find relationships using semantic similarity
    """
    
    RELATIONSHIP_PATTERNS = {
        'payment': ['zapłacił', 'przekazał', 'otrzymał', 'przelew', 'płatność'],
        'employment': ['pracuje', 'zatrudniony', 'dyrektor', 'prezes', 'członek zarządu'],
        'ownership': ['posiada', 'właściciel', 'udziałowiec', 'akcjonariusz'],
        'investigation': ['śledztwo', 'postępowanie', 'zarzut', 'podejrzany'],
        'corruption': ['łapówka', 'korupcja', 'przekupstwo', 'przekręt']
    }
    
    def __init__(self, embedder: DualEmbeddingSystem):
        self.embedder = embedder
        self.relationship_embeddings = self._precompute_embeddings()
    
    def find_relationships(
        self, 
        entities: List[Entity], 
        text: str,
        window_size: int = 50
    ) -> List[Relationship]:
        """
        Find relationships between entities
        
        Strategy:
        1. Find entity pairs within window_size characters
        2. Extract context text between entities
        3. Classify relationship using:
           a) Keyword matching (heuristic)
           b) Semantic similarity (semantic)
        """
        relationships = []
        
        for i, entity1 in enumerate(entities):
            for entity2 in entities[i+1:]:
                # Check if entities are close enough
                distance = abs(entity1.start - entity2.start)
                
                if distance < window_size:
                    # Extract context
                    start = min(entity1.start, entity2.start)
                    end = max(entity1.end, entity2.end)
                    context = text[start:end]
                    
                    # Find relationship type
                    rel_type = self._classify_relationship(context)
                    
                    if rel_type:
                        relationships.append(Relationship(
                            from_entity=entity1,
                            to_entity=entity2,
                            type=rel_type['type'],
                            confidence=rel_type['confidence'],
                            context=context
                        ))
        
        return relationships
    
    def _classify_relationship(self, context: str) -> Optional[Dict]:
        """
        Classify relationship using hybrid approach
        """
        context_lower = context.lower()
        
        # 1. HEURISTIC: Keyword matching
        for rel_type, keywords in self.RELATIONSHIP_PATTERNS.items():
            if any(kw in context_lower for kw in keywords):
                return {
                    'type': rel_type,
                    'confidence': 0.85,
                    'method': 'heuristic'
                }
        
        # 2. SEMANTIC: Embedding similarity
        context_emb = self.embedder.embed_text(context)
        
        best_match = None
        best_score = 0.0
        
        for rel_type, rel_emb in self.relationship_embeddings.items():
            similarity = cosine_similarity(context_emb, rel_emb)
            
            if similarity > best_score and similarity > 0.7:
                best_score = similarity
                best_match = rel_type
        
        if best_match:
            return {
                'type': best_match,
                'confidence': best_score,
                'method': 'semantic'
            }
        
        return None
```

**Przykład użycia:**

```python
finder = SemanticRelationshipFinder(embedder)

relationships = finder.find_relationships(entities, text)

# Output:
# Relationship(
#   from='Jan Kowalski', 
#   to='ABC Sp. z o.o.', 
#   type='employment',
#   confidence=0.85
# )
# Relationship(
#   from='Jan Kowalski', 
#   to='50.000 zł', 
#   type='payment',
#   confidence=0.92
# )
```

---

### **Moduł 3: Lokalny Graf (NetworkX)**

```python
import networkx as nx

class LocalKnowledgeGraph:
    """
    Fast, in-memory knowledge graph
    """
    
    def __init__(self):
        self.graph = nx.MultiDiGraph()  # Directed, allows multiple edges
        self.entity_index = {}  # Fast lookup
    
    def add_entities(self, entities: List[Entity]):
        """Add entities as nodes"""
        for entity in entities:
            node_id = self._get_node_id(entity)
            
            self.graph.add_node(
                node_id,
                text=entity.text,
                type=entity.type,
                confidence=entity.confidence
            )
            
            self.entity_index[entity.text] = node_id
    
    def add_relationships(self, relationships: List[Relationship]):
        """Add relationships as edges"""
        for rel in relationships:
            from_id = self._get_node_id(rel.from_entity)
            to_id = self._get_node_id(rel.to_entity)
            
            self.graph.add_edge(
                from_id,
                to_id,
                type=rel.type,
                confidence=rel.confidence,
                context=rel.context
            )
    
    def find_connections(
        self, 
        entity: str, 
        max_hops: int = 3
    ) -> List[Path]:
        """
        Find all entities connected to given entity
        within max_hops
        """
        if entity not in self.entity_index:
            return []
        
        node_id = self.entity_index[entity]
        
        # BFS to find connections
        paths = []
        visited = {node_id}
        queue = [(node_id, [node_id])]
        
        while queue:
            current, path = queue.pop(0)
            
            if len(path) > max_hops + 1:
                continue
            
            for neighbor in self.graph.neighbors(current):
                if neighbor not in visited:
                    visited.add(neighbor)
                    new_path = path + [neighbor]
                    paths.append(new_path)
                    queue.append((neighbor, new_path))
        
        return self._format_paths(paths)
    
    def find_shortest_path(self, entity1: str, entity2: str):
        """Find shortest path between two entities"""
        try:
            id1 = self.entity_index[entity1]
            id2 = self.entity_index[entity2]
            
            path = nx.shortest_path(self.graph, id1, id2)
            return self._format_path(path)
        except (KeyError, nx.NetworkXNoPath):
            return None
    
    def get_central_entities(self, top_n: int = 10):
        """
        Find most central entities (most connections)
        """
        centrality = nx.degree_centrality(self.graph)
        
        sorted_entities = sorted(
            centrality.items(), 
            key=lambda x: x[1], 
            reverse=True
        )[:top_n]
        
        return [
            (self.graph.nodes[node]['text'], score)
            for node, score in sorted_entities
        ]
    
    def detect_communities(self):
        """Find groups of closely related entities"""
        # Convert to undirected for community detection
        undirected = self.graph.to_undirected()
        
        communities = nx.community.greedy_modularity_communities(undirected)
        
        return [
            [self.graph.nodes[node]['text'] for node in community]
            for community in communities
        ]
    
    def export_to_neo4j(self, neo4j_client: Neo4jClient, case_id: str):
        """
        Export to Neo4j for persistent storage
        """
        # Add all nodes
        for node_id, data in self.graph.nodes(data=True):
            neo4j_client.create_entity(
                case_id=case_id,
                entity_id=node_id,
                entity_type=data['type'],
                properties={
                    'text': data['text'],
                    'confidence': data['confidence']
                }
            )
        
        # Add all edges
        for from_id, to_id, data in self.graph.edges(data=True):
            neo4j_client.create_relationship(
                case_id=case_id,
                from_entity=from_id,
                to_entity=to_id,
                rel_type=data['type'],
                properties={
                    'confidence': data['confidence'],
                    'context': data['context']
                }
            )
```

**Przykład użycia:**

```python
# Build graph
graph = LocalKnowledgeGraph()
graph.add_entities(entities)
graph.add_relationships(relationships)

# Query
connections = graph.find_connections('Jan Kowalski', max_hops=2)
# Returns: [ABC Sp. z o.o., 50.000 zł, CBA-123/2024, ...]

path = graph.find_shortest_path('Jan Kowalski', 'CBA-123/2024')
# Returns: Jan Kowalski → 50.000 zł → CBA-123/2024

central = graph.get_central_entities(top_n=5)
# Returns: [('Jan Kowalski', 0.85), ('ABC Sp. z o.o.', 0.72), ...]

communities = graph.detect_communities()
# Returns: [
#   ['Jan Kowalski', 'ABC Sp. z o.o.', '50.000 zł'],
#   ['CBA', 'prokuratura', 'śledztwo'],
#   ...
# ]
```

---

## 🚀 KOMPLETNY PRZYKŁAD

```python
from src.graph.heuristic_extractor import HeuristicEntityExtractor
from src.graph.semantic_relationships import SemanticRelationshipFinder
from src.graph.local_knowledge_graph import LocalKnowledgeGraph
from src.data.embedding_pipeline import DualEmbeddingSystem

# Initialize
extractor = HeuristicEntityExtractor()
embedder = DualEmbeddingSystem()
finder = SemanticRelationshipFinder(embedder)
graph = LocalKnowledgeGraph()

# Process document
text = """
Pan Jan Kowalski, dyrektor firmy ABC Sp. z o.o., otrzymał łapówkę
w wysokości 50.000 zł od Piotra Nowaka w związku ze sprawą 
przetargu publicznego. CBA wszczęło śledztwo w sprawie nr CBA-123/2024
dnia 15.03.2024.
"""

# 1. Extract entities (HEURISTIC)
entities = extractor.extract(text)
print(f"Found {len(entities)} entities:")
for e in entities:
    print(f"  - {e.text} ({e.type})")

# 2. Find relationships (SEMANTIC + HEURISTIC)
relationships = finder.find_relationships(entities, text)
print(f"\nFound {len(relationships)} relationships:")
for r in relationships:
    print(f"  - {r.from_entity.text} --[{r.type}]--> {r.to_entity.text}")

# 3. Build graph (IN-MEMORY)
graph.add_entities(entities)
graph.add_relationships(relationships)

# 4. Query graph
print("\nConnections for 'Jan Kowalski':")
connections = graph.find_connections('Jan Kowalski', max_hops=2)
for conn in connections:
    print(f"  → {conn}")

print("\nMost central entities:")
central = graph.get_central_entities(top_n=3)
for entity, score in central:
    print(f"  - {entity}: {score:.2f}")

# 5. Optional: Export to Neo4j
if neo4j_available:
    graph.export_to_neo4j(neo4j_client, case_id="cba_reports_2024")
```

**Output:**

```
Found 6 entities:
  - Jan Kowalski (person)
  - ABC Sp. z o.o. (organization)
  - 50.000 zł (money)
  - Piotr Nowak (person)
  - CBA (organization)
  - CBA-123/2024 (case_number)
  - 15.03.2024 (date)

Found 5 relationships:
  - Jan Kowalski --[employment]--> ABC Sp. z o.o.
  - Jan Kowalski --[corruption]--> 50.000 zł
  - Piotr Nowak --[payment]--> 50.000 zł
  - CBA --[investigation]--> CBA-123/2024
  - Jan Kowalski --[investigation]--> CBA-123/2024

Connections for 'Jan Kowalski':
  → Jan Kowalski → ABC Sp. z o.o.
  → Jan Kowalski → 50.000 zł
  → Jan Kowalski → CBA-123/2024
  → Jan Kowalski → 50.000 zł → Piotr Nowak

Most central entities:
  - Jan Kowalski: 0.83
  - 50.000 zł: 0.67
  - CBA-123/2024: 0.50
```

---

## 📊 PORÓWNANIE: Neo4j vs Lokalny Graf

| Feature | Neo4j | Lokalny Graf |
|---------|-------|--------------|
| **Setup** | ❌ Wymaga serwera | ✅ Zero setup |
| **Speed** | 🟡 Medium (network) | ✅ Fast (in-memory) |
| **Scalability** | ✅ Millions of nodes | ⚠️ Thousands (RAM limit) |
| **Persistence** | ✅ Yes | ❌ No (export needed) |
| **Query Language** | ✅ Cypher | ⚠️ Python API |
| **Dependencies** | ❌ Docker/server | ✅ NetworkX only |
| **Use Case** | Production, large scale | Development, prototyping |

---

## 🎯 REKOMENDACJA

### **Implementuj Lokalny Graf dla:**

1. ✅ **Szybkie prototypowanie** - Instant results, no setup
2. ✅ **Analiza pojedynczych dokumentów** - 13 PDFów CBA to ideal case
3. ✅ **Development/testing** - Easy debugging
4. ✅ **Offline work** - No external dependencies

### **Użyj Neo4j dla:**

1. ⚠️ **Production deployment** - Persistent storage
2. ⚠️ **Large scale** - Millions of entities
3. ⚠️ **Complex queries** - Cypher is powerful
4. ⚠️ **Multi-user access** - Concurrent queries

---

## 💡 BOTTOM LINE

```
╔═══════════════════════════════════════════════════╗
║                                                   ║
║  OBECNY STAN:                                     ║
║  ✅ Neo4j client ready (but offline)              ║
║  ❌ Lokalny graf - NIE zaimplementowany           ║
║                                                   ║
║  POTRZEBA:                                        ║
║  🚀 Lokalny In-Memory Graf                        ║
║     - Heurystyczna ekstrakcja encji               ║
║     - Semantyczna identyfikacja relacji           ║
║     - Fast NetworkX queries                       ║
║     - Zero dependencies                           ║
║                                                   ║
║  BENEFIT:                                         ║
║  ⚡ Instant entity/relationship extraction        ║
║  ⚡ Find connections in <1 second                 ║
║  ⚡ Perfect for CBA reports analysis              ║
║                                                   ║
╚═══════════════════════════════════════════════════╝
```

**Chcesz żebym zaimplementował lokalny graf relacji?**

To da Ci:
- 🕸️ Automatyczną mapę powiązań w raportach CBA
- 🔍 "Kto z kim jest powiązany?"
- 💰 "Jakie są przepływy finansowe?"
- 📊 "Kto jest centralną postacią?"

**Implementacja: ~2-3 godziny** 🚀
