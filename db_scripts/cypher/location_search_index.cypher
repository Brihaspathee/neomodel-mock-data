CREATE FULLTEXT INDEX location_address_lucene_index
FOR (n:Location)
ON EACH [n.streetAddress]
OPTIONS {
    indexConfig: {
    `fulltext.analyzer`: 'standard',
    `fulltext.eventually_consistent`: false
    }
  }
