#!/bin/bash

# turn on bash's job control
set -m

# Start the primary process and put it in the background
/startup/docker-entrypoint.sh neo4j &

# wait for Neo4j started
wget --quiet --tries=10 --retry-connrefused=on --waitretry=5 -O /dev/null http://localhost:7474

# execute init.cypher
cypher-shell -u "${USERNAME}" -p "${PASSWORD}" -d neo4j --file /var/lib/neo4j/import/init.cypher

# now we bring the primary process back into the foreground
# and leave it there
fg %1
