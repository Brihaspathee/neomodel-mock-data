CREATE FULLTEXT INDEX organization_name_lucene_index
FOR (n:Organization)
ON EACH [n.name]
OPTIONS {
    indexConfig: {
        `fulltext.analyzer`: 'standard',
        `fulltext.eventually_consistent`: false
        }
    }
