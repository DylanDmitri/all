import os
import shutil

def listdir(name):
    for fname in os.listdir(name):
        if not fname.startswith('.'):
            yield fname

OUTPUT = '/Users/dg/Desktop/unit_test'
SOURCE = '/Users/dg/Desktop/algo'

for fname in listdir(OUTPUT):
    shutil.rmtree(os.path.join(OUTPUT, fname))

TEST_LOC = 'unit_tests/test_undirected_graph.js'
ALGO_LOC = 'js/undirected_graph.js'


def load(replace_loc=None, replace_text=''):

    for filename in listdir(SOURCE):

        # step 1 copy directory

        shutil.copytree(os.path.join(SOURCE, filename),
                        os.path.join(OUTPUT, filename))

        # possibly step down an additional directory

        inner = os.listdir(os.path.join(OUTPUT, filename))
        if len(inner) <= 2:
            filename = os.path.join(filename, inner[-1])


        # step 2 purge other unit tests

        for item in os.listdir(os.path.join(OUTPUT, filename, 'unit_tests')):
            if not (item == 'test_undirected_graph.js' or item.endswith('.html')):
                os.remove(os.path.join(OUTPUT, filename, 'unit_tests', item))


        # step 3 replace either tests or algorithm

        item = os.path.join(OUTPUT,filename,replace_loc)
        if replace_text == REAL_TEST:
            new_text = open(item).read() + replace_text
        else:
            new_text = replace_text
        open(item, 'w').write(new_text)



REAL_TEST = '''
QUnit.test('special jack test 1', (assert) => {
    const graph = new UndirectedGraph();
    graph.addVertex('a');
    graph.addVertex('b');
    graph.addVertex('c');
    graph.addVertex('d');
    graph.addVertex('e');
    graph.addEdge('a', new UndirectedEdge(1), 'e');
    graph.addEdge('d', new UndirectedEdge(1), 'e');
    graph.addEdge('c', new UndirectedEdge(1), 'd');
    graph.addEdge('b', new UndirectedEdge(1), 'c');
    graph.addEdge('a', new UndirectedEdge(2), 'b');
    assert.deepEqual(shortestUndirectedPath(graph, 'a', (vertex) => vertex === 'b'), ['a', 'b']);
});

QUnit.test('special jack test 2', (assert) => {
    const graph = new UndirectedGraph();
    graph.addVertex('a');
    graph.addVertex('b');
    graph.addVertex('c');
    graph.addEdge('a', new UndirectedEdge(7), 'c');
    graph.addEdge('b', new UndirectedEdge(4), 'c');
    graph.addEdge('a', new UndirectedEdge(12), 'b');
    assert.deepEqual(shortestUndirectedPath(graph, 'a', (vertex) => vertex === 'b'), ['a', 'b']);
});

QUnit.test('special jack test 3', (assert) => {
  const graph = new UndirectedGraph();
  graph.addVertex('a');
  graph.addVertex('b');
  graph.addVertex('c');
  graph.addVertex('d');
  graph.addVertex('e');
  graph.addEdge('a', new UndirectedEdge(2), 'e');
  graph.addEdge('e', new UndirectedEdge(7), 'b');
  graph.addEdge('b', new UndirectedEdge(10), 'c');
  graph.addEdge('e', new UndirectedEdge(10), 'd');
  // the search should find the shortest path in terms of number of vertices, not total weighted length
  assert.deepEqual(shortestUndirectedPath(graph, 'a', (vertex) => vertex === 'e'), ['a', 'e']);
});

'''

DEPTH_FIRST = '''
/* exported UndirectedEdge UndirectedGraph shortestUndirectedPath */
/* globals identity */

class UndirectedEdge {
  constructor(weight) {
    this.weight = weight;
  }

  reverse() {
    return this;
  }
}

class UndirectedGraph {
  constructor() {
    this.vertices = [];
    this.edges = [];
    this.adjacencyMatrix = [];
  }

  addVertex(vertex) {
    this.vertices.push(vertex);
    for (const adjacencyColumn of this.adjacencyMatrix) {
      adjacencyColumn.push(undefined);
      console.assert(adjacencyColumn.length === this.vertices.length, 'Vertex count does not match adjacency matrix height.');
    }
    this.adjacencyMatrix.push(this.vertices.concat().fill(undefined));
    console.assert(this.adjacencyMatrix.length === this.vertices.length, 'Vertex count does not match adjacency matrix width.');
  }

  addEdge(source, edge, destination) {
    const sourceIndex = this.vertices.indexOf(source);
    console.assert(sourceIndex >= 0, `Edge ${edge} added to nonexistent vertex ${source}.`);
    const destinationIndex = this.vertices.indexOf(destination);
    console.assert(destinationIndex >= 0, `Edge ${edge} added to nonexistent vertex ${destination}.`);
    if (sourceIndex !== destinationIndex) {
      console.assert(this.adjacencyMatrix[sourceIndex][destinationIndex] === undefined,
        `Added edge ${edge}, which conflicts with the edge ${this.adjacencyMatrix[sourceIndex][destinationIndex]}.`);
      this.edges.push(edge);
      this.adjacencyMatrix[sourceIndex][destinationIndex] = edge;
      this.adjacencyMatrix[destinationIndex][sourceIndex] = edge.reverse();
    }
  }

  getNeighbors(vertex) {
    const vertexIndex = this.vertices.indexOf(vertex);
    console.assert(vertexIndex >= 0, `Cannot get neighbors of nonexistent vertex ${vertex}.`);
    const adjacencyColumn = this.adjacencyMatrix[vertexIndex];
    const result = [];
    for (let i = this.vertices.length; i--;) {
      if (adjacencyColumn[i] !== undefined) {
        result.push(this.vertices[i]);
      }
    }
    return result;
  }

  getEdge(source, destination) {
    const sourceIndex = this.vertices.indexOf(source);
    console.assert(sourceIndex >= 0, `Cannot get edge incident on nonexistent vertex ${source}.`);
    const destinationIndex = this.vertices.indexOf(destination);
    console.assert(destinationIndex >= 0, `Cannot get edge incident on nonexistent vertex ${destination}.`);
    return this.adjacencyMatrix[sourceIndex][destinationIndex];
  }
}

function shortestUndirectedPath(graph, source, destinationPredicate, projection = identity) {
  const stack = [source];
  const visited = new Set();
  function helper() {
    const endpoint = stack.top();
    if (destinationPredicate(endpoint)) {
      return stack.concat();
    }
    visited.add(projection(endpoint));
    for (const neighbor of graph.getNeighbors(endpoint)) {
      if (!visited.has(projection(neighbor))) {
        stack.push(neighbor);
        const result = helper();
        stack.pop();
        if (result !== undefined) {
          return result;
        }
      }
    }
    return undefined;
  }
  return helper();
}
'''

# load(ALGO_LOC, DEPTH_FIRST)

load(TEST_LOC, REAL_TEST)


# # should fail breadth first
# test = 'personal'
# algo = 'breadth_first'
#
# # should succeed
# test = 'standard_battery'
# algo = 'personal'  # depth first






