// Delete everything except Product, Network, LegacySystemID attached to them,
// and DataDictionary + anything connected to DataDictionary
MATCH (n)
WHERE NOT (
  n:Product
  OR n:Network
  OR (
    n:LegacySystemID AND (
      (n)<-[:HAS_LEGACY_SYSTEM_ID]-(:Network)
      OR (n)<-[:HAS_LEGACY_SYSTEM_ID]-(:Product)
    )
  )
  OR (
    n:DataDictionary
    OR (n)-[*1..]->(:DataDictionary)
    OR (:DataDictionary)-[*1..]->(n)
  )
)
DETACH DELETE n;
