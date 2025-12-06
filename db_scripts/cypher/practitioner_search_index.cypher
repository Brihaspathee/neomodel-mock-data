CREATE FULLTEXT INDEX practitioner_name_lucene_index
FOR (p:Practitioner)
ON EACH [p.firstName, p.lastName]
OPTIONS {
  indexConfig: {
    `fulltext.analyzer`: 'standard',
    `fulltext.eventually_consistent`: false
  }
}