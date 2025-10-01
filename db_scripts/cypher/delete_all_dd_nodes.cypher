// Delete all DataDictionary nodes and everything connected below them
MATCH (n:DataDictionary)
OPTIONAL MATCH (n)-[*]->(child)
DETACH DELETE n, child;