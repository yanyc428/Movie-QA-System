from neo4j import GraphDatabase, basic_auth


class open_driver(object):
    def __init__(self):
        self._driver = GraphDatabase.driver("bolt://localhost:7687", auth=basic_auth("neo4j", "neo4j123456"))

    def __enter__(self):
        return self._driver

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._driver.close()


class GraphNodes(object):

    def __init__(self):
        self._actors_cql = 'match (n:Person)-[r:actedin]-(b:Movie) return n.name'
        self._movie_cql = 'match (n:Person)-[r:actedin]-(b:Movie) return b.title'
        self._type_cql = 'match (n:Genre) return n.name'

    def get_movies(self):
        with open_driver() as driver:
            with driver.session(database="neo4j") as session:
                results = session.read_transaction(
                    lambda tx: tx.run(self._movie_cql).data())
                result = set(map(lambda x: x['b.title'], results))
        return result

    def get_actors(self):
        with open_driver() as driver:
            with driver.session(database="neo4j") as session:
                results = session.read_transaction(
                    lambda tx: tx.run(self._actors_cql).data())
                result = set(map(lambda x: x['n.name'], results))
        return result

    def get_type(self):
        with open_driver() as driver:
            with driver.session(database="neo4j") as session:
                results = session.read_transaction(
                    lambda tx: tx.run(self._type_cql).data())
                result = set(map(lambda x: x['n.name'], results))
        return result


if __name__ == '__main__':
    nodes = GraphNodes()
    print(len(nodes.get_actors()))
    print(nodes.get_movies())

