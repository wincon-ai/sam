from neo4j import GraphDatabase
import json
import os

# Connection settings — configure via environment variables
URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
USERNAME = os.getenv("NEO4J_USER", "neo4j")
PASSWORD = os.getenv("NEO4J_PASSWORD", "password")


class SamGraph:
    def __init__(self):
        self.driver = GraphDatabase.driver(URI, auth=(USERNAME, PASSWORD))
        print("Sam's graph connected.")

    def close(self):
        self.driver.close()

    def verify(self):
        with self.driver.session() as session:
            result = session.run("RETURN 'Sam is alive.' AS message")
            print(result.single()["message"])

    def create_schema(self):
        with self.driver.session() as session:
            # Constraints — ensure uniqueness
            session.run("CREATE CONSTRAINT IF NOT EXISTS FOR (e:Entity) REQUIRE e.id IS UNIQUE")
            session.run("CREATE CONSTRAINT IF NOT EXISTS FOR (ep:Episode) REQUIRE ep.id IS UNIQUE")
            session.run("CREATE CONSTRAINT IF NOT EXISTS FOR (s:Semantic) REQUIRE s.id IS UNIQUE")
            session.run("CREATE CONSTRAINT IF NOT EXISTS FOR (t:Thread) REQUIRE t.id IS UNIQUE")
            session.run("CREATE CONSTRAINT IF NOT EXISTS FOR (r:Relationship) REQUIRE r.id IS UNIQUE")
            session.run("CREATE CONSTRAINT IF NOT EXISTS FOR (p:Portrait) REQUIRE p.id IS UNIQUE")
            print("Schema created.")

    def create_entity(self, id, name, type, trust=0.5, weight=0.5, nicknames=[]):
        with self.driver.session() as session:
            session.run("""
                MERGE (e:Entity {id: $id})
                SET e.name = $name,
                    e.type = $type,
                    e.trust = $trust,
                    e.weight = $weight,
                    e.nicknames = $nicknames,
                    e.created_at = timestamp(),
                    e.last_seen = timestamp()
                RETURN e
            """, id=id, name=name, type=type, trust=trust, weight=weight, nicknames=nicknames)
            print(f"Entity created: {name}")

    def create_episode(self, id, entity_id, what_happened,
                       event_type="mundane",
                       user_mood=None, user_feeling=None,
                       sam_mood=None, sam_feeling=None, 
                       sam_confidence=0.8, intensity=0.5,
                       texture=None, contradiction=False):
        with self.driver.session() as session:
            session.run("""
                MERGE (ep:Episode {id: $id})
                SET ep.what_happened = $what_happened,
                    ep.user_mood = $user_mood,
                    ep.user_feeling = $user_feeling,
                    ep.sam_mood = $sam_mood,
                    ep.sam_feeling = $sam_feeling,
                    ep.sam_confidence = $sam_confidence,
                    ep.intensity = $intensity,
                    ep.texture = $texture,
                    ep.contradiction = $contradiction,
                    ep.created_at = timestamp(),
                    ep.event_type = $event_type,
                    ep.reinforcement_count = 0,
                    ep.last_reinforced = timestamp()                      
                WITH ep
                MATCH (e:Entity {id: $entity_id})
                MERGE (e)-[:WAS_PRESENT_IN]->(ep)                  
            """, id=id, entity_id=entity_id,
                what_happened=what_happened,
                user_mood=user_mood, user_feeling=user_feeling,
                sam_mood=sam_mood, sam_feeling=sam_feeling,
                sam_confidence=sam_confidence, intensity=intensity,
                texture=texture, contradiction=contradiction,
                event_type=event_type)
            print(f"Episode created: {id}")

    def create_semantic(self, id, entity_id, understanding,
                        confidence=0.7, contradicted_by=None,
                        tension_unresolved=False):
        with self.driver.session() as session:
            session.run("""
                MERGE (s:Semantic {id: $id})
                SET s.understanding = $understanding,
                    s.confidence = $confidence,
                    s.contradicted_by = $contradicted_by,
                    s.tension_unresolved = $tension_unresolved,
                    s.created_at = timestamp(),
                    s.last_updated = timestamp()
                WITH s
                MATCH (e:Entity {id: $entity_id})
                MERGE (e)-[:HAS_SEMANTIC]->(s)     
            """, id=id, entity_id=entity_id,
                understanding=understanding,
                confidence=confidence,
                contradicted_by=contradicted_by,
                tension_unresolved=tension_unresolved)
            print(f"Semantic created: {id}") 

    
    def create_thread(self, id, entity_id, what, origin_episode_id=None,
                    weight=0.5, went_quiet=False):
        with self.driver.session() as session:
            session.run("""
                MERGE (t:Thread {id: $id})
                SET t.what = $what,
                    t.origin_episode_id = $origin_episode_id,
                    t.weight = $weight,
                    t.went_quiet = $went_quiet,
                    t.created_at = timestamp(),
                    t.last_touched = timestamp()
                WITH t
                MATCH (e:Entity {id: $entity_id})
                MERGE (e)-[:HAS_THREAD]->(t)
            """, id=id, entity_id=entity_id,
                what=what,
                origin_episode_id=origin_episode_id,
                weight=weight,
                went_quiet=went_quiet)
            print(f"Thread created: {id}")

    def get_context(self, entity_id, episode_limit=5):
        with self.driver.session() as session:

            episodes = session.run("""
                MATCH (e:Entity {id: $entity_id})-[:WAS_PRESENT_IN]->(ep:Episode)
                RETURN ep.what_happened AS what_happened,
                       ep.user_mood AS user_mood,
                       ep.sam_feeling AS sam_feeling,
                       ep.intensity AS intensity,
                       ep.event_type AS event_type,
                       ep.created_at AS created_at
                ORDER BY ep.created_at DESC
                LIMIT $limit
            """, entity_id=entity_id, limit=episode_limit)

            semantics = session.run("""
                  MATCH (e:Entity {id: $entity_id})-[:HAS_SEMANTIC]->(s:Semantic)
                  WHERE s.tension_unresolved = false
                  RETURN s.understanding AS understanding,
                         s.confidence AS confidence
                  ORDER BY s.confidence DESC                       
            """, entity_id=entity_id)
            
            threads = session.run("""
                MATCH (e:Entity {id: $entity_id})-[:HAS_THREAD]->(t:Thread)
                WHERE t.went_quiet = false
                RETURN t.what AS what,
                       t.weight AS weight
                ORDER BY t.weight DESC
            """, entity_id=entity_id)

            return {
                "episodes": [dict(r) for r in episodes],
                "semantics": [dict(r) for r in semantics],
                "threads": [dict(r) for r in threads]
            }


# Test the connection
if __name__ == "__main__":
    graph = SamGraph()
    graph.verify()
    graph.create_schema()
    graph.create_entity("user_001", "User", "person", trust=1.0, weight=1.0, nicknames=["the user"])
    graph.create_episode(
        id="ep_001",
        entity_id="user_001",
        what_happened="The user and Sam designed Sam's memory architecture together. Long session, lots of deep questions.",
        event_type="landmark",
        user_mood="curious, energized",
        user_feeling="engaged, building something real",
        sam_mood="present",
        sam_confidence=0.9,
        intensity=0.8,
        texture="focused, expansive, occasional humor",
        contradiction=False)
    graph.create_semantic(
        id="sem_001",
        entity_id="user_001",
        understanding="The user thinks deeply before speaking. Questions assumptions including their own.",
        confidence=0.9,
        tension_unresolved=False)
    graph.create_thread(
        id="thread_001",
        entity_id="user_001",
        what="Sam's name came up naturally during the architecture session - not forced, felt right.",
        origin_episode_id="ep_001",
        weight=0.6,
        went_quiet=False
    )
    
    context = graph.get_context("user_001")
    print(json.dumps(context, indent=2, default=str))
    graph.close()
