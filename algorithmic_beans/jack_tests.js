QUnit.module('transit.js');
/* globals QUnit Vertex UndirectedEdge UndirectedGraph SimulationEvent City Route Bus Passenger */
/* eslint-disable no-magic-numbers, no-underscore-dangle */

function waypoints(route) {
  const result = [];
  for (const waypoint of route.waypoints) {
    result.push(waypoint[1].vertex);
  }
  return result.sort();
}

function arcs(route) {
  const result = [];
  for (const arc of route.arcs) {
    result.push(`${arc.source !== undefined ? arc.source.vertex : ''}→${arc.destination.vertex}`);
  }
  return result.sort();
}

QUnit.test('identify longest journey(s)', assert => {
  const a = new Vertex('a');
  const b = new Vertex('b');
  const c = new Vertex('c');
  const graph = new UndirectedGraph();
  graph.addVertex(a);
  graph.addVertex(b);
  graph.addVertex(c);
  graph.addEdge(a, new UndirectedEdge(2), b);
  graph.addEdge(b, new UndirectedEdge(7), c);
  const city = new City(graph, graph);
  const passenger = new Passenger(city, 'p', 3.0, a);
  const passenger2 = new Passenger(city, 'p2', 3.0, a);
  passenger.source = a;
  passenger2.source = a;
  passenger.destination = c;
  passenger2.destination = b;
  passenger._plan();
  passenger2._plan();
  let arr = city.getLongestJourneys(1)
  assert.deepEqual(arr, [passenger]);
  assert.deepEqual(city.getLongestJourneys(2), [passenger2, passenger]);
});
QUnit.test('get an array of 1 passenger with the longest journey', (assert) => {
  const a = new Vertex('a');
  const b = new Vertex('b');
  const c = new Vertex('c');
  const d = new Vertex('d');
  const e = new Vertex('e');

  const graph = new UndirectedGraph();
  graph.addVertex(a);
  graph.addVertex(b);
  graph.addVertex(c);
  graph.addVertex(d);
  graph.addVertex(e);
  graph.addEdge(a, new UndirectedEdge(2.0), b);
  graph.addEdge(b, new UndirectedEdge(6.0), c);
  graph.addEdge(c, new UndirectedEdge(10.0), d);
  graph.addEdge(d, new UndirectedEdge(2.0), e);

  const city = new City(graph, graph);

  const passenger = new Passenger(city, 'p', 3.0, a);
  passenger.source = a;
  passenger.destination = c;
  passenger._plan();
  assert.deepEqual(passenger.duration, 8.0);

  const passenger2 = new Passenger(city, 'p2', 3.0, b);
  passenger2.source = b;
  passenger2.destination = c;
  passenger2._plan();
  assert.deepEqual(passenger2.duration, 6.0);

  //passenger3 has the longest duration at 20.0, so getLongestJourneys should return them
  const passenger3 = new Passenger(city, 'p3', 2.0, a);
  passenger3.source = a;
  passenger3.destination = e;
  passenger3._plan();
  assert.deepEqual(passenger3.duration, 20.0);

  const passenger4 = new Passenger(city, 'p4', 0.5, b);
  passenger4.source = b;
  passenger4.destination = e;
  passenger4._plan();
  assert.deepEqual(passenger4.duration, 18.0);

  assert.deepEqual(city.getLongestJourneys(1), [passenger3]);
});
QUnit.test('get an array of the 2 passengers with the longest journies', (assert) => {
  const a = new Vertex('a');
  const b = new Vertex('b');
  const c = new Vertex('c');
  const d = new Vertex('d');
  const e = new Vertex('e');

  const graph = new UndirectedGraph();
  graph.addVertex(a);
  graph.addVertex(b);
  graph.addVertex(c);
  graph.addVertex(d);
  graph.addVertex(e);
  graph.addEdge(a, new UndirectedEdge(2.0), b);
  graph.addEdge(b, new UndirectedEdge(6.0), c);
  graph.addEdge(c, new UndirectedEdge(10.0), d);
  graph.addEdge(d, new UndirectedEdge(2.0), e);

  const city = new City(graph, graph);

  const passenger = new Passenger(city, 'p', 3.0, a);
  passenger.source = a;
  passenger.destination = c;
  passenger._plan();
  assert.deepEqual(passenger.duration, 8.0);

  const passenger2 = new Passenger(city, 'p2', 3.0, b);
  passenger2.source = b;
  passenger2.destination = c;
  passenger2._plan();
  assert.deepEqual(passenger2.duration, 6.0);

  //passenger3 has the longest duration at 20.0, so getLongestJourneys should contain them
  const passenger3 = new Passenger(city, 'p3', 2.0, a);
  passenger3.source = a;
  passenger3.destination = e;
  passenger3._plan();
  assert.deepEqual(passenger3.duration, 20.0);

  //passenger4 has the second longest duration at 18.0, so getLongestJourneys should also contain them
  const passenger4 = new Passenger(city, 'p4', 0.5, b);
  passenger4.source = b;
  passenger4.destination = e;
  passenger4._plan();
  assert.deepEqual(passenger4.duration, 18.0);

  assert.deepEqual(city.getLongestJourneys(2), [passenger4, passenger3]);
});
QUnit.test('get longest journey 1', (assert) => {
  const a = new Vertex('a');
  const b = new Vertex('b');
  const c = new Vertex('c');
  const d = new Vertex('d');
  const graph = new UndirectedGraph();
  graph.addVertex(a);
  graph.addVertex(b);
  graph.addVertex(c);
  graph.addVertex(d);
  graph.addEdge(a, new UndirectedEdge(1.0), b);
  graph.addEdge(b, new UndirectedEdge(1.0), c);
  graph.addEdge(c, new UndirectedEdge(1.0), d);
  const city = new City(graph, graph);
  const passenger1 = new Passenger(city, 'p1', 3.0, a); //eta = 2
  passenger1.source = a;
  passenger1.destination = c;
  passenger1._plan();
  const passenger2 = new Passenger(city, 'p2', 3.0, a); //eta = 1
  passenger2.source = a;
  passenger2.destination = b;
  passenger2._plan();
  const passenger3 = new Passenger(city, 'p3', 3.0, a); //eta = 3
  passenger3.source = a;
  passenger3.destination = d;
  passenger3._plan();

  let passengers = [passenger1, passenger2, passenger3];
  var result = city.getLongestJourneys(1)
  assert.deepEqual(result, [passenger3]);
});

QUnit.test('get longest journey 2', (assert) => {
  const a = new Vertex('a');
  const b = new Vertex('b');
  const c = new Vertex('c');
  const d = new Vertex('d');
  const graph = new UndirectedGraph();
  graph.addVertex(a);
  graph.addVertex(b);
  graph.addVertex(c);
  graph.addVertex(d);
  graph.addEdge(a, new UndirectedEdge(1.0), b);
  graph.addEdge(b, new UndirectedEdge(1.0), c);
  graph.addEdge(c, new UndirectedEdge(1.0), d);
  const city = new City(graph, graph);
  const passenger1 = new Passenger(city, 'p1', 3.0, a); //eta = 2
  passenger1.source = a;
  passenger1.destination = c;
  passenger1._plan();
  const passenger2 = new Passenger(city, 'p2', 3.0, a); //eta = 1
  passenger2.source = a;
  passenger2.destination = b;
  passenger2._plan();
  const passenger3 = new Passenger(city, 'p3', 3.0, a); //eta = 3
  passenger3.source = a;
  passenger3.destination = d;
  passenger3._plan();

  let passengers = [passenger1, passenger2, passenger3];
  var result = city.getLongestJourneys(2)
  assert.deepEqual(result, [passenger1,passenger3]);
});

QUnit.test('get longest journey 3', (assert) => {
  const a = new Vertex('a');
  const b = new Vertex('b');
  const c = new Vertex('c');
  const d = new Vertex('d');
  const e = new Vertex('e');
  const graph = new UndirectedGraph();
  graph.addVertex(a);
  graph.addVertex(b);
  graph.addVertex(c);
  graph.addVertex(d);
  graph.addVertex(e);
  graph.addEdge(a, new UndirectedEdge(1.0), b);
  graph.addEdge(b, new UndirectedEdge(1.0), c);
  graph.addEdge(c, new UndirectedEdge(1.0), d);
  graph.addEdge(d, new UndirectedEdge(1.0), e);
  const city = new City(graph, graph);
  const passenger1 = new Passenger(city, 'p1', 3.0, a); //eta = 2
  passenger1.source = a;
  passenger1.destination = c;
  passenger1._plan();
  const passenger2 = new Passenger(city, 'p2', 3.0, a); //eta = 1
  passenger2.source = a;
  passenger2.destination = b;
  passenger2._plan();
  const passenger3 = new Passenger(city, 'p3', 3.0, a); //eta = 3
  passenger3.source = a;
  passenger3.destination = d;
  passenger3._plan();
  const passenger4 = new Passenger(city, 'p4', 3.0, a); //eta = 4
  passenger4.source = a;
  passenger4.destination = e;
  passenger4._plan();

  let passengers = [passenger1, passenger2, passenger3, passenger4];
  var result = city.getLongestJourneys(2)
  console.log(result);
  assert.deepEqual(result, [passenger3 ,passenger4]);
});

QUnit.test('get longest journey 4', (assert) => {
  const a = new Vertex('a');
  const b = new Vertex('b');
  const c = new Vertex('c');
  const d = new Vertex('d');
  const e = new Vertex('e');
  const graph = new UndirectedGraph();
  graph.addVertex(a);
  graph.addVertex(b);
  graph.addVertex(c);
  graph.addVertex(d);
  graph.addVertex(e);
  graph.addEdge(a, new UndirectedEdge(1.0), b);
  graph.addEdge(b, new UndirectedEdge(1.0), c);
  graph.addEdge(c, new UndirectedEdge(1.0), d);
  graph.addEdge(d, new UndirectedEdge(1.0), e);
  const city = new City(graph, graph);
  const passenger1 = new Passenger(city, 'p1', 3.0, a); //eta = 2
  passenger1.source = a;
  passenger1.destination = c;
  passenger1._plan();
  const passenger2 = new Passenger(city, 'p2', 3.0, a); //eta = 1
  passenger2.source = a;
  passenger2.destination = b;
  passenger2._plan();
  const passenger3 = new Passenger(city, 'p3', 3.0, a); //eta = 3
  passenger3.source = a;
  passenger3.destination = d;
  passenger3._plan();
  const passenger4 = new Passenger(city, 'p4', 3.0, a); //eta = 4
  passenger4.source = a;
  passenger4.destination = e;
  passenger4._plan();

  let passengers = [passenger1, passenger2, passenger3, passenger4];
  var result = city.getLongestJourneys(3)
  console.log(result);
  assert.deepEqual(result, [passenger1, passenger3 ,passenger4]);
});
// My First Unit Test for getLongestJourneys
QUnit.test('Find 2 longest journeys', (assert) => {
  const a = new Vertex('a');
  const b = new Vertex('b');
  const c = new Vertex('c');
  const d = new Vertex('d');
  const graph = new UndirectedGraph();
  graph.addVertex(a);
  graph.addVertex(b);
  graph.addVertex(c);
  graph.addVertex(d);
  graph.addEdge(a, new UndirectedEdge(1), b);
  graph.addEdge(b, new UndirectedEdge(1), c);
  graph.addEdge(c, new UndirectedEdge(1), d);
  const city = new City(graph, graph);
  const passenger1 = new Passenger(city, 'p1', 3.0, a);
  const passenger2 = new Passenger(city, 'p2', 3.0, a);
  const passenger3 = new Passenger(city, 'p3', 3.0, a);
  passenger1.source = a;
  passenger1.destination = b;
  passenger2.source = a;
  passenger2.destination = c;
  passenger3.source = a;
  passenger3.source = d;
  passenger1._plan();
  passenger2._plan();
  passenger3._plan();
  // the search should find the shortest path in terms of number of vertices, not total weighted length
  assert.deepEqual(city.getLongestJourneys(2), [passenger2,passenger3]);
});

// My First Unit Test for getLongestJourneys
QUnit.test('Find 3 longest journeys', (assert) => {
  const a = new Vertex('a');
  const b = new Vertex('b');
  const c = new Vertex('c');
  const graph = new UndirectedGraph();
  graph.addVertex(a);
  graph.addVertex(b);
  graph.addVertex(c);
  graph.addEdge(a, new UndirectedEdge(2), b);
  graph.addEdge(b, new UndirectedEdge(7), c);
  graph.addEdge(a, new UndirectedEdge(10), c);
  const city = new City(graph, graph);
  const passenger1 = new Passenger(city, 'p1', 3.0, a);
  const passenger2 = new Passenger(city, 'p2', 3.0, a);
  const passenger3 = new Passenger(city, 'p3', 3.0, b);
  passenger1.source = a;
  passenger1.destination = b;
  passenger2.source = a;
  passenger2.destination = c;
  passenger3.source = b;
  passenger3.source = c;
  passenger1._plan();
  passenger2._plan();
  passenger3._plan();
  // the search should find the shortest path in terms of number of vertices, not total weighted length
  assert.deepEqual(city.getLongestJourneys(3), [passenger1,passenger2,passenger3]);
});
QUnit.test('Get the longest journey', (assert) => {
  const a = new Vertex('a');
  const b = new Vertex('b');
  const c = new Vertex('c');
  const graph = new UndirectedGraph();
  graph.addVertex(a);
  graph.addVertex(b);
  graph.addVertex(c);
  graph.addEdge(a, new UndirectedEdge(2), b);
  graph.addEdge(b, new UndirectedEdge(10), c);
  const city = new City(graph, graph);
  const passenger = new Passenger(city, 'p', 3.0, a);
  const passenger2 = new Passenger(city, 'p2', 5.0, a);
  const passenger3 = new Passenger(city, 'p3', 2000.0, a);
  console.log(city.getLongestJourneys(1));
  assert.deepEqual(city.getLongestJourneys(1), [passenger3]);
});

QUnit.test('Get more than one longest journey', (assert) => {
  const a = new Vertex('a');
  const b = new Vertex('b');
  const c = new Vertex('c');
  const graph = new UndirectedGraph();
  graph.addVertex(a);
  graph.addVertex(b);
  graph.addVertex(c);
  graph.addEdge(a, new UndirectedEdge(2), b);
  graph.addEdge(b, new UndirectedEdge(10), c);
  const city = new City(graph, graph);
  const passenger = new Passenger(city, 'p', 3.0, a);
  const passenger2 = new Passenger(city, 'p2', 1000.0, a);
  const passenger3 = new Passenger(city, 'p3', 2000.0, a);
  console.log(city.getLongestJourneys(1));
  assert.deepEqual(city.getLongestJourneys(2), [passenger2, passenger3]);
});
QUnit.test('Try to get too many longest journeys', (assert) => {
  const a = new Vertex('a');
  const b = new Vertex('b');
  const c = new Vertex('c');
  const graph = new UndirectedGraph();
  graph.addVertex(a);
  graph.addVertex(b);
  graph.addVertex(c);
  graph.addEdge(a, new UndirectedEdge(2), b);
  graph.addEdge(b, new UndirectedEdge(10), c);
  const city = new City(graph, graph);
  const passenger = new Passenger(city, 'p', 3.0, a);
  const passenger2 = new Passenger(city, 'p2', 1000.0, a);
  const passenger3 = new Passenger(city, 'p3', 2000.0, a);
  console.log(city.getLongestJourneys(1));
  assert.deepEqual(city.getLongestJourneys(8), undefined);
});
QUnit.test('Try to get zero longest journeys', (assert) => {
  const a = new Vertex('a');
  const b = new Vertex('b');
  const c = new Vertex('c');
  const graph = new UndirectedGraph();
  graph.addVertex(a);
  graph.addVertex(b);
  graph.addVertex(c);
  graph.addEdge(a, new UndirectedEdge(2), b);
  graph.addEdge(b, new UndirectedEdge(10), c);
  const city = new City(graph, graph);
  const passenger = new Passenger(city, 'p', 3.0, a);
  const passenger2 = new Passenger(city, 'p2', 1000.0, a);
  const passenger3 = new Passenger(city, 'p3', 2000.0, a);
  console.log(city.getLongestJourneys(1));
  assert.deepEqual(city.getLongestJourneys(0), undefined);
});
QUnit.test("getLongestJourneys returns an empty list if array is empty", (assert) => {
  const walkGraph = new UndirectedGraph();
  const driveGraph = new UndirectedGraph();
  const city = new City(walkGraph, driveGraph);

  assert.deepEqual(city.getLongestJourneys(5), []);
})

QUnit.test("getLongestJourneys returns just the one passenger in an array if we ask for the longest journey for a list of size one", (assert) => {
  //Create graph
  const a = new Vertex('a');
  const b = new Vertex('b');
  const walkGraph = new UndirectedGraph();
  walkGraph.addVertex(a);
  walkGraph.addVertex(b);
  walkGraph.addEdge(a, new UndirectedEdge(1), b);

  //Create city
  const driveGraph = new UndirectedGraph();
  const city = new City(walkGraph, driveGraph);

  //Initialize passenger
  const p1 = new Passenger(city, 'p1', 3.0, a);
  p1.source = a;
  p1.destination = b;
  p1.start();

  assert.deepEqual(city.getLongestJourneys(1), [p1]);
});

QUnit.test("getLongestJourneys returns maximum the number of passengers in the list", (assert) => {
  //Create graph
  const a = new Vertex('a');
  const b = new Vertex('b');
  const walkGraph = new UndirectedGraph();
  walkGraph.addVertex(a);
  walkGraph.addVertex(b);
  walkGraph.addEdge(a, new UndirectedEdge(1), b);

  //Create city
  const driveGraph = new UndirectedGraph();
  const city = new City(walkGraph, driveGraph);

  //Initialize passenger
  const p1 = new Passenger(city, 'p1', 3.0, a);
  p1.source = a;
  p1.destination = b;
  p1.start();

  assert.deepEqual(city.getLongestJourneys(10), [p1]);
});

QUnit.test("getLongestJourneys returns an empty list if we ask for the largest zero journeys", (assert) => {
  //Create graph
  const a = new Vertex('a');
  const b = new Vertex('b');
  const walkGraph = new UndirectedGraph();
  walkGraph.addVertex(a);
  walkGraph.addVertex(b);
  walkGraph.addEdge(a, new UndirectedEdge(1), b);

  //Create city
  const driveGraph = new UndirectedGraph();
  const city = new City(walkGraph, driveGraph);

  //Initialize passenger
  const p1 = new Passenger(city, 'p1', 3.0, a);
  p1.source = a;
  p1.destination = b;
  p1.start();

  assert.deepEqual(city.getLongestJourneys(0), []);
});

QUnit.test("getLongestJourneys returns the passengers with the k longest journeys (extreme example)", (assert) => {
  //Create graph
  const walkGraph = new UndirectedGraph();
  var vertices = [new Vertex('v0')];
  walkGraph.addVertex(vertices[0]);
  for (var i = 1; i < 100; i++) {
    vertices[i] = new Vertex('v' + i);
    walkGraph.addVertex(vertices[i]);
    walkGraph.addEdge(vertices[i-1], new UndirectedEdge(1), vertices[i]);
  }

  //Create city
  const driveGraph = new UndirectedGraph();
  const city = new City(walkGraph, driveGraph);

  //Initialize passengers
  var passengers = [];
  for (var i = 0; i < 100; i += 2) {
    var p = new Passenger(city, 'p' + i, 3.0, vertices[i]);
    p.source = vertices[i];
    p.destination = vertices[99];
    p.start();
    passengers[i] = p;
  }

  //Calculate and test result
  const testCount = 23;
  var result = city.getLongestJourneys(testCount);
  assert.equal(result.length, 23);
  assert.ok(passengers.slice(0,23).every(p=>result.includes(p)));
});

QUnit.test('getLongestJourneys returns the passengers with the k longest journeys (realistic example)', (assert) => {
  //Create graph
  const a = new Vertex('a');
  const b = new Vertex('b');
  const c = new Vertex('c');
  const d = new Vertex('d');
  const e = new Vertex('e');
  const f = new Vertex('f');
  const g = new Vertex('g');
  const h = new Vertex('h');
  const i = new Vertex('i');
  const walkGraph = new UndirectedGraph();
  walkGraph.addVertex(a);
  walkGraph.addVertex(b);
  walkGraph.addVertex(c);
  walkGraph.addVertex(d);
  walkGraph.addVertex(e);
  walkGraph.addVertex(f);
  walkGraph.addVertex(g);
  walkGraph.addVertex(h);
  walkGraph.addVertex(i);
  walkGraph.addEdge(a, new UndirectedEdge(1), b);
  walkGraph.addEdge(b, new UndirectedEdge(3), c);
  walkGraph.addEdge(c, new UndirectedEdge(5), d);
  walkGraph.addEdge(d, new UndirectedEdge(9), e);
  walkGraph.addEdge(d, new UndirectedEdge(1), f);
  walkGraph.addEdge(e, new UndirectedEdge(1), f);
  walkGraph.addEdge(g, new UndirectedEdge(8), h);
  walkGraph.addEdge(h, new UndirectedEdge(6), i);

  //Create city
  const driveGraph = new UndirectedGraph();
  const city = new City(walkGraph, driveGraph);

  //Initialize passengers
  var p1 = new Passenger(city, 'p1', 3.0, a); //Path length: 9
  p1.source = a;
  p1.destination = d;
  p1.start();
  var p2 = new Passenger(city, 'p2', 3.0, e); //Path length: 9
  p2.source = e;
  p2.destination = d;
  p2.start();
  var p3 = new Passenger(city, 'p3', 3.0, f); //Path length: 1
  p3.source = f;
  p3.destination = e;
  p3.start();
  var p4 = new Passenger(city, 'p4', 3.0, g); //Path length: 14
  p4.source = g;
  p4.destination = i;
  p4.start();

  //Calculate and test result
  var result = city.getLongestJourneys(3);
  assert.equal(result.length, 3);
  assert.ok([p1, p2, p4].every(p=>result.includes(p)));
});
QUnit.test('getLongestJourneys for one passenger', (assert) => {
  const a = new Vertex('a');
  const b = new Vertex('b');
  const graph = new UndirectedGraph();
  graph.addVertex(a);
  graph.addVertex(b);
  graph.addEdge(a, new UndirectedEdge(2), b);
  const city = new City(graph, graph);
  const passenger = new Passenger(city, 'p', 1.0, a);
  passenger.source = a;
  passenger.destination = b;
  passenger._plan();
  const list = city.getLongestJourneys(1);
  assert.deepEqual([passenger], list);
});

QUnit.test('getLongestJourneys for two passengers', (assert) => {
  const a = new Vertex('a');
  const b = new Vertex('b');
  const c = new Vertex('c');
  const graph = new UndirectedGraph();
  graph.addVertex(a);
  graph.addVertex(b);
  graph.addVertex(c);
  graph.addEdge(a, new UndirectedEdge(2), b);
  graph.addEdge(b, new UndirectedEdge(3), c);
  const city = new City(graph, graph);
  const passenger1 = new Passenger(city, 'p', 1.0, a);
  passenger1.source = a;
  passenger1.destination = b;
  passenger1._plan();
  const passenger2 = new Passenger(city, 'q', 2.0, a);
  passenger2.source = a;
  passenger2.destination = c;
  passenger2._plan();
  const list = city.getLongestJourneys(2);
  assert.deepEqual([passenger2, passenger1], list);
});

QUnit.test('getLongestJourneys for three passengers', (assert) => {
  const a = new Vertex('a');
  const b = new Vertex('b');
  const c = new Vertex('c');
  const graph = new UndirectedGraph();
  graph.addVertex(a);
  graph.addVertex(b);
  graph.addVertex(c);
  graph.addEdge(a, new UndirectedEdge(2), b);
  graph.addEdge(b, new UndirectedEdge(3), c);
  const city = new City(graph, graph);
  const passenger1 = new Passenger(city, 'p', 1.0, a);
  passenger1.source = a;
  passenger1.destination = b;
  passenger1._plan();
  const passenger2 = new Passenger(city, 'q', 2.0, a);
  passenger2.source = a;
  passenger2.destination = c;
  passenger2._plan();
  const passenger3 = new Passenger(city, 'r', 2.0, b);
  passenger3.source = b;
  passenger3.destination = c;
  passenger3._plan();
  const list = city.getLongestJourneys(3);
  assert.deepEqual([passenger3, passenger2, passenger1], list);
});

QUnit.test('getLongestJourneys for two passengers with three in city', (assert) => {
  const a = new Vertex('a');
  const b = new Vertex('b');
  const c = new Vertex('c');
  const graph = new UndirectedGraph();
  graph.addVertex(a);
  graph.addVertex(b);
  graph.addVertex(c);
  graph.addEdge(a, new UndirectedEdge(2), b);
  graph.addEdge(b, new UndirectedEdge(3), c);
  const city = new City(graph, graph);
  const passenger1 = new Passenger(city, 'p', 1.0, a);
  passenger1.source = a;
  passenger1.destination = b;
  passenger1._plan();
  const passenger2 = new Passenger(city, 'q', 1.0, a);
  passenger2.source = a;
  passenger2.destination = c;
  passenger2._plan();
  const passenger3 = new Passenger(city, 'r', 1.0, b);
  passenger3.source = b;
  passenger3.destination = c;
  passenger3._plan();
  const list = city.getLongestJourneys(2);
  assert.deepEqual([passenger2, passenger3], list);
});
QUnit.test('simulates finding top-k passenger with longest journey', (assert) => {
  const a = new Vertex('a');
  const b = new Vertex('b');
  const c = new Vertex('c');
  const d = new Vertex('d');
  const e = new Vertex('e');
  const f = new Vertex('f');
  const graph = new UndirectedGraph();
  graph.addVertex(a);
  graph.addVertex(b);
  graph.addVertex(c);
  graph.addVertex(d);
  graph.addVertex(e);
  graph.addVertex(f);
  graph.addEdge(a, new UndirectedEdge(5), b);
  graph.addEdge(b, new UndirectedEdge(9), c);
  graph.addEdge(c, new UndirectedEdge(12), d);
  graph.addEdge(d, new UndirectedEdge(8), e);
  graph.addEdge(e, new UndirectedEdge(17), f)
  const city = new City(graph, graph);
  const passengerOne = new Passenger(city, 'A', 0.0, a);
  const passengerTwo = new Passenger(city, 'B', 0.0, b);
  const passengerThree = new Passenger(city, 'C', 0.0, c);
  const passengerFour = new Passenger(city, 'D', 0.0, d);
  const passengerFive = new Passenger(city, 'E', 0.0, e);
  city.addPassenger(passengerOne);
  city.addPassenger(passengerTwo);
  city.addPassenger(passengerThree);
  city.addPassenger(passengerFour);
  city.addPassenger(passengerFive);
  passengerOne.source = a;
  passengerTwo.source = b;
  passengerThree.source = c;
  passengerFour.source = d;
  passengerFive.source = e;
  passengerOne.destination = b;
  passengerTwo.destination = c;
  passengerThree.destination = d;
  passengerFour.destination = e;
  passengerFive.destination = f;
  passengerOne.start();
  passengerTwo.start();
  passengerThree.start();
  passengerFour.start();
  passengerFive.start();
  assert.deepEqual(city.getLongestJourneys(1)[0].name, 'E');
});

QUnit.test('simulates finding top-k list of passengers with longest journeys', (assert) => {
  const a = new Vertex('a');
  const b = new Vertex('b');
  const c = new Vertex('c');
  const d = new Vertex('d');
  const e = new Vertex('e');
  const f = new Vertex('f');
  const graph = new UndirectedGraph();
  graph.addVertex(a);
  graph.addVertex(b);
  graph.addVertex(c);
  graph.addVertex(d);
  graph.addVertex(e);
  graph.addVertex(f);
  graph.addEdge(a, new UndirectedEdge(5), b);
  graph.addEdge(b, new UndirectedEdge(9), c);
  graph.addEdge(c, new UndirectedEdge(12), d);
  graph.addEdge(d, new UndirectedEdge(8), e);
  graph.addEdge(e, new UndirectedEdge(17), f)
  const city = new City(graph, graph);
  const passengerOne = new Passenger(city, 'A', 0.0, a);
  const passengerTwo = new Passenger(city, 'B', 0.0, b);
  const passengerThree = new Passenger(city, 'C', 0.0, c);
  const passengerFour = new Passenger(city, 'D', 0.0, d);
  const passengerFive = new Passenger(city, 'E', 0.0, e);
  passengerOne.source = a;
  passengerTwo.source = b;
  passengerThree.source = c;
  passengerFour.source = d;
  passengerFive.source = e;
  passengerOne.destination = b;
  passengerTwo.destination = c;
  passengerThree.destination = d;
  passengerFour.destination = e;
  passengerFive.destination = f;
  passengerOne.start();
  passengerTwo.start();
  passengerThree.start();
  passengerFour.start();
  passengerFive.start();
  var result = city.getLongestJourneys(2);
  assert.deepEqual(result.length,2);
  assert.ok([passengerThree, passengerFive].every(p=>result.includes(p)));
});
QUnit.test('Unit test for getLongestJourneys #1', (assert) => {
  const a = new Vertex('a');
  const b = new Vertex('b');
  const c = new Vertex('c');
  const d = new Vertex('d');
  const e = new Vertex('e');
  const graph = new UndirectedGraph();
  graph.addVertex(a);
  graph.addVertex(b);
  graph.addVertex(c);
  graph.addVertex(d);
  graph.addVertex(e);
  graph.addEdge(a, new UndirectedEdge(1), b);
  graph.addEdge(b, new UndirectedEdge(1), c);
  graph.addEdge(c, new UndirectedEdge(1), d);
  graph.addEdge(d, new UndirectedEdge(1), e);
  const city = new City(graph, graph);
  const passengerOne = new Passenger(city, 'p1', 3.0, a);
  passengerOne.source = a;
  passengerOne.destination = b;
  passengerOne._plan();
  const passengerTwo = new Passenger(city, 'p2', 3.0, a);
  passengerTwo.source = a;
  passengerTwo.destination = c;
  passengerTwo._plan();
  const passengerThree = new Passenger(city, 'p3', 3.0, a);
  passengerThree.source = a;
  passengerThree.destination = d;
  passengerThree._plan();
  const passengerFour = new Passenger(city, 'p4', 3.0, a);
  passengerFour.source = a;
  passengerFour.destination = e;
  passengerFour._plan();
  var result = city.getLongestJourneys(2);
  console.log(result);
  assert.deepEqual(result, [passengerThree, passengerFour]);
});

QUnit.test('Unit test for getLongestJourneys #2', (assert) => {
  const a = new Vertex('a');
  const b = new Vertex('b');
  const c = new Vertex('c');
  const d = new Vertex('d');
  const e = new Vertex('e');
  const f = new Vertex('f');
  const graph = new UndirectedGraph();
  graph.addVertex(a);
  graph.addVertex(b);
  graph.addVertex(c);
  graph.addVertex(d);
  graph.addVertex(e);
  graph.addVertex(f);
  graph.addEdge(a, new UndirectedEdge(1), b);
  graph.addEdge(b, new UndirectedEdge(1), c);
  graph.addEdge(c, new UndirectedEdge(1), d);
  graph.addEdge(d, new UndirectedEdge(1), e);
  graph.addEdge(e, new UndirectedEdge(1), f);
  const city = new City(graph, graph);
  const passengerOne = new Passenger(city, 'p1', 3.0, a);
  passengerOne.source = a;
  passengerOne.destination = b;
  passengerOne._plan();
  const passengerTwo = new Passenger(city, 'p2', 3.0, a);
  passengerTwo.source = a;
  passengerTwo.destination = c;
  passengerTwo._plan();
  const passengerThree = new Passenger(city, 'p3', 3.0, a);
  passengerThree.source = a;
  passengerThree.destination = d;
  passengerThree._plan();
  const passengerFour = new Passenger(city, 'p4', 3.0, a);
  passengerFour.source = a;
  passengerFour.destination = e;
  passengerFour._plan();
  const passengerFive = new Passenger(city, 'p5', 3.0, a);
  passengerFive.source = a;
  passengerFive.destination = f;
  passengerFive._plan();
  var result = city.getLongestJourneys(3);
  console.log(result);
  assert.deepEqual(result, [passengerThree, passengerFour, passengerFive]);
});
QUnit.test('find the passenger(s) with the longest journey', (assert) => {
  const a = new Vertex('a');
  const b = new Vertex('b');
  const c = new Vertex('c');
  const d = new Vertex('d');
  const e = new Vertex('e');
  const f = new Vertex('f');
  const g = new Vertex('g');
  const h = new Vertex('h');
  const graph = new UndirectedGraph();
  graph.addVertex(a);
  graph.addVertex(b);
  graph.addVertex(c);
  graph.addVertex(d);
  graph.addVertex(e);
  graph.addVertex(f);
  graph.addVertex(g);
  graph.addVertex(h);
  graph.addEdge(a, new UndirectedEdge(9), b);
  graph.addEdge(b, new UndirectedEdge(5), c);
  graph.addEdge(c, new UndirectedEdge(8), d);
  graph.addEdge(a, new UndirectedEdge(2), d);
  graph.addEdge(e, new UndirectedEdge(4), b);
  graph.addEdge(f, new UndirectedEdge(1), c);
  graph.addEdge(a, new UndirectedEdge(5), g);
  graph.addEdge(g, new UndirectedEdge(7), c);
  graph.addEdge(h, new UndirectedEdge(9), b);
  const city = new City(graph, graph);
  const passenger1 = new Passenger(city, '1', 7.0, d);
  const passenger2 = new Passenger(city, '2', 52.0, h);
  const passenger3 = new Passenger(city, '3', 1.0, a);
  const passenger4 = new Passenger(city, '4', 7.0, c);
  const passenger5 = new Passenger(city, '5', 13.5, e);
  const passenger6 = new Passenger(city, '6', 68.3, b);
  const passenger7 = new Passenger(city, '7', 12.0, g);
  const passenger8 = new Passenger(city, '8', 4.0, f);
  assert.deepEqual(city.getLongestJourney(4), [passenger7, passenger5, passenger2, passenger6]);
});

QUnit.test('no longest journey should be found', (assert) => {
  assert.throws(() => {
    const a = new Vertex('a');
    const b = new Vertex('b');
    const c = new Vertex('c');
    const d = new Vertex('d');
    const graph = new UndirectedGraph();
    graph.addVertex(a);
    graph.addVertex(b);
    graph.addVertex(c);
    graph.addVertex(d);
    graph.addEdge(a, new UndirectedEdge(9), b);
    graph.addEdge(b, new UndirectedEdge(5), c);
    graph.addEdge(c, new UndirectedEdge(8), d);
    graph.addEdge(a, new UndirectedEdge(2), d);
    const city = new City(graph, graph);
    const passenger1 = new Passenger(city, '1', undefined, d);
    const passenger2 = new Passenger(city, '2', undefined, b);
    const passenger3 = new Passenger(city, '3', undefined, a);
    const passenger4 = new Passenger(city, '4', undefined, c);
    assert.deepEqual(city.getLongestJourney(2), []);
  });
});
QUnit.test('This Tests the Longest Journey Function', (assert) => {
  const a = new Vertex('a');
  const b = new Vertex('b');
  const c = new Vertex('c');
  const d = new Vertex('d');
  const graph = new UndirectedGraph();
  graph.addVertex(a);
  graph.addVertex(b);
  graph.addVertex(c);
  graph.addVertex(d);
  graph.addEdge(a, new UndirectedEdge(2), b);
  graph.addEdge(b, new UndirectedEdge(2), c);
  graph.addEdge(c, new UndirectedEdge(2), d);
  const city = new City(graph, graph);
  const p = new Passenger(city, 'p', 3.0, a);
  p.source = a;
  p.destination = b;
  p._plan();
  const p1 = new Passenger(city, 'p', 3.0, a);
  p1.source = a;
  p1.destination = c;
  p1._plan();
  const p2 = new Passenger(city, 'p', 3.0, a);
  p2.source = a;
  p2.destination = d;
  p2._plan();
  assert.deepEqual(city.getLongestJourney(1), [p2]);
});

QUnit.test('This Tests the Longest Journey Function #2', (assert) => {
  const a = new Vertex('a');
  const b = new Vertex('b');
  const c = new Vertex('c');
  const graph = new UndirectedGraph();
  graph.addVertex(a);
  graph.addVertex(b);
  graph.addVertex(c);
  graph.addEdge(a, new UndirectedEdge(2), b);
  graph.addEdge(b, new UndirectedEdge(7), c);
  graph.addEdge(a, new UndirectedEdge(10), c);
  const city = new City(graph, graph);
  const p = new Passenger(city, 'p', 3.0, a);
  p.source = a;
  p.destination = c;
  p._plan();
  const p1 = new Passenger(city, 'p', 3.0, b);
  p1.source = b;
  p1.destination = c;
  p1._plan();
  const p2 = new Passenger(city, 'p', 3.0, a);
  p2.source = a;
  p2.destination = b;
  p2._plan();
  assert.deepEqual(city.getLongestJourney(2), [p, p1]);
});

QUnit.test('get a list of the 2 passengers with the longest journeys to make in a list of 3 passengers', (assert) => {
  const a = new Vertex('a');
  const b = new Vertex('b');
  const c = new Vertex('c');
  const d = new Vertex('d');
  const e = new Vertex('e');
  const graph = new UndirectedGraph();
  graph.addVertex(a);
  graph.addVertex(b);
  graph.addVertex(c);
  graph.addVertex(d);
  graph.addEdge(a, new UndirectedEdge(2), b);
  graph.addEdge(b, new UndirectedEdge(3), c);
  graph.addEdge(c, new UndirectedEdge(4), d);
  const city = new City(graph, graph);
  const p1 = new Passenger(city, 'p1', 0, a);
  p1.source = a;
  p1.destination = b;
  const p2 = new Passenger(city, 'p2', 0, b);
  p2.source = b;
  p2.destination = c;
  const p3 = new Passenger(city, 'p3', 0, c);
  p3.source = c;
  p3.destination = d;
  p1.start();
  p2.start();
  p3.start();
  var list = city.getLongestJourneys(2);
  console.log(list);
  assert.deepEqual(list.length, 2);
  assert.ok([p2, p3].every(p=>list.includes(p)));
});

QUnit.test('get a list of the 2 passengers with the longest journeys to make in a list of 6 passengers', (assert) => {
  const a = new Vertex('a');
  const b = new Vertex('b');
  const c = new Vertex('c');
  const d = new Vertex('d');
  const e = new Vertex('e');
  const f = new Vertex('f');
  const g = new Vertex('g');
  const graph = new UndirectedGraph();
  graph.addVertex(a);
  graph.addVertex(b);
  graph.addVertex(c);
  graph.addVertex(d);
  graph.addVertex(e);
  graph.addVertex(f);
  graph.addVertex(g);
  graph.addEdge(a, new UndirectedEdge(1), b);
  graph.addEdge(b, new UndirectedEdge(3), c);
  graph.addEdge(c, new UndirectedEdge(4), d);
  graph.addEdge(d, new UndirectedEdge(12), e);
  graph.addEdge(e, new UndirectedEdge(8), f);
  graph.addEdge(f, new UndirectedEdge(6), g);
  const city = new City(graph, graph);
  const p1 = new Passenger(city, 'p1', 0, a);
  p1.source = a;
  p1.destination = b;
  const p2 = new Passenger(city, 'p2', 0, b);
  p2.source = b;
  p2.destination = c;
  const p3 = new Passenger(city, 'p3', 0, c);
  p3.source = c;
  p3.destination = d;
  const p4 = new Passenger(city, 'p4', 0, d);
  p4.source = d;
  p4.destination = e;
  const p5 = new Passenger(city, 'p5', 0, e);
  p5.source = e;
  p5.destination = f;
  const p6 = new Passenger(city, 'p6', 0, f);
  p6.source = f;
  p6.destination = g;
  p1.start();
  p2.start();
  p3.start();
  p4.start();
  p5.start();
  p6.start();
  var list = city.getLongestJourneys(3);
  console.log(list);
  assert.deepEqual(list.length, 3);
  assert.ok([p4, p5, p6].every(p=>list.includes(p)));
});


QUnit.test('test getLongestJourneys with count = 1', (assert) => {
  const a = new Vertex('a');
  const b = new Vertex('b');
  const c = new Vertex('c');
  const d = new Vertex('d');
  const e = new Vertex('e');
  const walkGraph = new UndirectedGraph();
  walkGraph.addVertex(a);
  walkGraph.addVertex(b);
  walkGraph.addVertex(c);
  walkGraph.addVertex(d);
  walkGraph.addVertex(e);
  walkGraph.addEdge(a, new UndirectedEdge(10), b);
  walkGraph.addEdge(b, new UndirectedEdge(13), c);
  walkGraph.addEdge(c, new UndirectedEdge(16), d);
  walkGraph.addEdge(d, new UndirectedEdge(19), e);
  const driveGraph = new UndirectedGraph();
  driveGraph.addVertex(a);
  driveGraph.addVertex(b);
  driveGraph.addVertex(c);
  driveGraph.addVertex(d);
  driveGraph.addVertex(e);
  driveGraph.addEdge(a, new UndirectedEdge(3), b);
  driveGraph.addEdge(b, new UndirectedEdge(3), c);
  driveGraph.addEdge(c, new UndirectedEdge(3), d);
  driveGraph.addEdge(a, new UndirectedEdge(3), d);
  driveGraph.addEdge(d, new UndirectedEdge(3), e);
  const city = new City(walkGraph, driveGraph);
  const route = new Route(city, a, e);
  route.patch(a, b, c, d, e);
  const passAToC = new Passenger(city, 'p', 3.0, a);
  passAToC.source = a;
  passAToC.destination = c;
  passAToC._plan();
  const passBToE = new Passenger(city, 'p', 3.0, b);
  passBToE.source = b;
  passBToE.destination = e;
  passBToE._plan();
  const passAToD = new Passenger(city, 'p', 3.0, a);
  passAToD.source = a;
  passAToD.destination = d;
  passAToD._plan();
  var longestJourneys = city.getLongestJourneys(1);
  assert.deepEqual(longestJourneys.length, 1);
  assert.deepEqual(longestJourneys[0].duration, 48);
});

QUnit.test('test getLongestJourneys with count = 2', (assert) => {
  const a = new Vertex('a');
  const b = new Vertex('b');
  const c = new Vertex('c');
  const d = new Vertex('d');
  const e = new Vertex('e');
  const walkGraph = new UndirectedGraph();
  walkGraph.addVertex(a);
  walkGraph.addVertex(b);
  walkGraph.addVertex(c);
  walkGraph.addVertex(d);
  walkGraph.addVertex(e);
  walkGraph.addEdge(a, new UndirectedEdge(10), b);
  walkGraph.addEdge(b, new UndirectedEdge(13), c);
  walkGraph.addEdge(c, new UndirectedEdge(16), d);
  walkGraph.addEdge(d, new UndirectedEdge(19), e);
  const driveGraph = new UndirectedGraph();
  driveGraph.addVertex(a);
  driveGraph.addVertex(b);
  driveGraph.addVertex(c);
  driveGraph.addVertex(d);
  driveGraph.addVertex(e);
  driveGraph.addEdge(a, new UndirectedEdge(3), b);
  driveGraph.addEdge(b, new UndirectedEdge(3), c);
  driveGraph.addEdge(c, new UndirectedEdge(3), d);
  driveGraph.addEdge(a, new UndirectedEdge(3), d);
  driveGraph.addEdge(d, new UndirectedEdge(3), e);
  const city = new City(walkGraph, driveGraph);
  const route = new Route(city, a, e);
  route.patch(a, b, c, d, e);
  const passAToC = new Passenger(city, 'p', 3.0, a);
  passAToC.source = a;
  passAToC.destination = c;
  passAToC._plan();
  const passBToE = new Passenger(city, 'p', 3.0, b);
  passBToE.source = b;
  passBToE.destination = e;
  passBToE._plan();
  const passAToD = new Passenger(city, 'p', 3.0, a);
  passAToD.source = a;
  passAToD.destination = d;
  passAToD._plan();
  var longestJourneys = city.getLongestJourneys(2);

  //check that it returns the correct number of passengers
  assert.deepEqual(longestJourneys.length, 2);
  // check that the list contains just one instance of the passenger with the longest duration
  assert.deepEqual(longestJourneys.filter(function(pass){
	  return pass.duration == 48;
  }).length, 1);

  // check that the list contains just one instance of the passenger with the second longest duration
  assert.deepEqual(longestJourneys.filter(function(pass){
	  return pass.duration == 39;
  }).length, 1);
});//Added for HW 5
QUnit.test('get worst passenger durrations', (assert) => {
  const a = new Vertex('a');
  const b = new Vertex('b');
  const c = new Vertex('c');
  const d = new Vertex('d');
  const graph = new UndirectedGraph();
  graph.addVertex(a);
  graph.addVertex(b);
  graph.addVertex(c);
  graph.addVertex(d);
  graph.addEdge(a, new UndirectedEdge(5), b);
  graph.addEdge(b, new UndirectedEdge(5), c);
  graph.addEdge(c, new UndirectedEdge(7), d);
  const city = new City(graph, graph);
  const passenger1 = new Passenger(city, 'p1', 3.0, a);
  const passenger2 = new Passenger(city, 'p2', 3.0, a);
  const passenger3 = new Passenger(city, 'p3', 3.0, a);

  passenger1.source = a;
  passenger1.destination = b;
  passenger1._plan(); //duration = 5
  passenger2.source = a;
  passenger2.destination = c;
  passenger2._plan(); //duration = 10
  passenger3.source = a;
  passenger3.destination = d;
  passenger3._plan(); //duration = 17

  assert.deepEqual(city.getLongestJourneys(2),new Array(passenger3, passenger2));
});

//Added for HW 5
QUnit.test('get worst passenger durrations: ask for too many', (assert) => {
  const a = new Vertex('a');
  const b = new Vertex('b');
  const c = new Vertex('c');
  const d = new Vertex('d');
  const graph = new UndirectedGraph();
  graph.addVertex(a);
  graph.addVertex(b);
  graph.addVertex(c);
  graph.addVertex(d);
  graph.addEdge(a, new UndirectedEdge(5), b);
  graph.addEdge(b, new UndirectedEdge(5), c);
  graph.addEdge(c, new UndirectedEdge(7), d);
  const city = new City(graph, graph);
  const passenger1 = new Passenger(city, 'p1', 3.0, a);
  const passenger2 = new Passenger(city, 'p2', 3.0, a);
  const passenger3 = new Passenger(city, 'p3', 3.0, a);

  passenger1.source = a;
  passenger1.destination = b;
  passenger1._plan();
  passenger2.source = a;
  passenger2.destination = c;
  passenger2._plan();
  passenger3.source = a;
  passenger3.destination = d;
  passenger3._plan();

  assert.deepEqual(city.getLongestJourneys(4),undefined);
});QUnit.test('verify getLongestJourney retrieves the 2 most inconvenienced passengers (non-trivial)', (assert) => {
    const a = new Vertex('a');
    const b = new Vertex('b');
    const c = new Vertex('c');
    const d = new Vertex('d');
    const walkGraph = new UndirectedGraph();
    walkGraph.addVertex(a);
    walkGraph.addVertex(b);
    walkGraph.addVertex(c);
    walkGraph.addVertex(d);
    const driveGraph = new UndirectedGraph();
    driveGraph.addVertex(a);
    driveGraph.addVertex(b);
    driveGraph.addVertex(c);
    driveGraph.addVertex(d);
    driveGraph.addEdge(a, new UndirectedEdge(2), b);
    driveGraph.addEdge(b, new UndirectedEdge(4), c);
    driveGraph.addEdge(c, new UndirectedEdge(3), d);
    driveGraph.addEdge(b, new UndirectedEdge(1), d);
    const city = new City(walkGraph, driveGraph);
    const route = new Route(city, a, b);
    const route1 = new Route(city, b, c);
    const route2 = new Route(city, c, d);
    const passenger = new Passenger(city, 'p', 3.0, a);
    passenger.source = a;
    passenger.destination = b;
    passenger.start();
    const passenger1 = new Passenger(city, 'p', 3.0, a);
    passenger1.source = a;
    passenger1.destination = c;
    passenger1.start();
    const passenger2 = new Passenger(city, 'p', 3.0, a);
    passenger2.source = a;
    passenger2.destination = d;
    passenger2.start();
    let correct = [];
    correct.push(passenger1);
    correct.push(passenger2);
    assert.deepEqual(city.getLongestJourneys(2), correct);
});

QUnit.test('verify getLongestJourney retrieves the 0 most inconvenienced passengers (trivial)', (assert) => {
    const a = new Vertex('a');
    const b = new Vertex('b');
    const c = new Vertex('c');
    const d = new Vertex('d');
    const walkGraph = new UndirectedGraph();
    walkGraph.addVertex(a);
    walkGraph.addVertex(b);
    walkGraph.addVertex(c);
    walkGraph.addVertex(d);
    const driveGraph = new UndirectedGraph();
    driveGraph.addVertex(a);
    driveGraph.addVertex(b);
    driveGraph.addVertex(c);
    driveGraph.addVertex(d);
    driveGraph.addEdge(a, new UndirectedEdge(2), b);
    driveGraph.addEdge(b, new UndirectedEdge(4), c);
    driveGraph.addEdge(c, new UndirectedEdge(3), d);
    driveGraph.addEdge(b, new UndirectedEdge(1), d);
    const city = new City(walkGraph, driveGraph);
    const route = new Route(city, a, b);
    const route1 = new Route(city, b, c);
    const route2 = new Route(city, c, d);
    const passenger = new Passenger(city, 'p', 3.0, a);
    passenger.source = a;
    passenger.destination = b;
    passenger.start();
    const passenger1 = new Passenger(city, 'p', 3.0, a);
    passenger1.source = a;
    passenger1.destination = c;
    passenger1.start();
    const passenger2 = new Passenger(city, 'p', 3.0, a);
    passenger2.source = a;
    passenger2.destination = d;
    passenger2.start();
    assert.deepEqual(city.getLongestJourneys(0), undefined);
});

QUnit.test('Longest Journeys returns proper result.', (assert) => {
    const a = new Vertex('a');
    const b = new Vertex('b');
    const c = new Vertex('c');
    const d = new Vertex('d');
    const e = new Vertex('e');
    const walkGraph = new UndirectedGraph();
    walkGraph.addVertex(a);
    walkGraph.addVertex(b);
    walkGraph.addVertex(c);
    walkGraph.addVertex(d);
    walkGraph.addVertex(e);
    walkGraph.addEdge(a, new UndirectedEdge(4), b);
    walkGraph.addEdge(b, new UndirectedEdge(14), c);
    walkGraph.addEdge(c, new UndirectedEdge(14), d);
    walkGraph.addEdge(d, new UndirectedEdge(12), e);
    const driveGraph = new UndirectedGraph();
    driveGraph.addVertex(a);
    driveGraph.addVertex(b);
    driveGraph.addVertex(c);
    driveGraph.addVertex(d);
    driveGraph.addVertex(e);
    driveGraph.addEdge(b, new UndirectedEdge(7), c);
    driveGraph.addEdge(c, new UndirectedEdge(7), d);
    driveGraph.addEdge(d, new UndirectedEdge(7), e);
    driveGraph.addEdge(e, new UndirectedEdge(7), b);
    const city = new City(walkGraph, driveGraph);
    const route = new Route(city, b, e);
    route.patch(b, c, d, e);
    const x = new Bus(route.getArc(e)); // eslint-disable-line no-unused-vars
    const passenger1 = new Passenger(city, 'p1', 3.0, a);
    const passenger2 = new Passenger(city, 'p2', 6.0, a);
    const passenger3 = new Passenger(city, 'p3', 100.0, a);
    const passenger4 = new Passenger(city, 'p4', 6.0, a);
    const passenger5 = new Passenger(city, 'p5', 6.0, a);

    let result = city.getLongestJourneys(1);

    assert.deepEqual(result[0], passenger3);
});

QUnit.test('Longest Journeys with improper value returns undefined', (assert) => {
    const a = new Vertex('a');
    const b = new Vertex('b');
    const c = new Vertex('c');
    const d = new Vertex('d');
    const e = new Vertex('e');
    const walkGraph = new UndirectedGraph();
    walkGraph.addVertex(a);
    walkGraph.addVertex(b);
    walkGraph.addVertex(c);
    walkGraph.addVertex(d);
    walkGraph.addVertex(e);
    walkGraph.addEdge(a, new UndirectedEdge(4), b);
    walkGraph.addEdge(b, new UndirectedEdge(14), c);
    walkGraph.addEdge(c, new UndirectedEdge(14), d);
    walkGraph.addEdge(d, new UndirectedEdge(12), e);
    const driveGraph = new UndirectedGraph();
    driveGraph.addVertex(a);
    driveGraph.addVertex(b);
    driveGraph.addVertex(c);
    driveGraph.addVertex(d);
    driveGraph.addVertex(e);
    driveGraph.addEdge(b, new UndirectedEdge(7), c);
    driveGraph.addEdge(c, new UndirectedEdge(7), d);
    driveGraph.addEdge(d, new UndirectedEdge(7), e);
    driveGraph.addEdge(e, new UndirectedEdge(7), b);
    const city = new City(walkGraph, driveGraph);
    const route = new Route(city, b, e);
    route.patch(b, c, d, e);
    const x = new Bus(route.getArc(e)); // eslint-disable-line no-unused-vars
    const passenger1 = new Passenger(city, 'p1', 3.0, a);
    const passenger2 = new Passenger(city, 'p2', 6.0, a);
    const passenger3 = new Passenger(city, 'p3', 100.0, a);
    const passenger4 = new Passenger(city, 'p4', 6.0, a);
    const passenger5 = new Passenger(city, 'p5', 6.0, a);

    let result = city.getLongestJourneys(10);

    assert.deepEqual(result, undefined);
});
QUnit.test('get the longest journey from a list of a single passenger', (assert) => {
  const a = new Vertex('a');
  const b = new Vertex('b');
  const c = new Vertex('c');
  const d = new Vertex('d');
  const graph = new UndirectedGraph();
  graph.addVertex(a);
  graph.addVertex(b);
  graph.addVertex(c);
  graph.addVertex(d);
  graph.addEdge(a, new UndirectedEdge(10), b);
  graph.addEdge(b, new UndirectedEdge(4), c);
  graph.addEdge(c, new UndirectedEdge(7), d);
  const city = new City(graph, graph);
  const passenger = new Passenger(city, 'p', 3.0, a);
  passenger.source = a;
  passenger.destination = d;
  passenger._plan();
  assert.deepEqual(city.getLongestJourneys(1)[0].planDuration, passenger.planDuration);
});

QUnit.test('get the longest journey from a list of multiple passengers', (assert) => {
  const a = new Vertex('a');
  const b = new Vertex('b');
  const c = new Vertex('c');
  const d = new Vertex('d');
  const graph = new UndirectedGraph();
  graph.addVertex(a);
  graph.addVertex(b);
  graph.addVertex(c);
  graph.addVertex(d);
  graph.addEdge(a, new UndirectedEdge(10), b);
  graph.addEdge(b, new UndirectedEdge(4), c);
  graph.addEdge(c, new UndirectedEdge(7), d);
  const city = new City(graph, graph);
  const p1 = new Passenger(city, 'p1', 3.0, a);
  p1.source = a;
  p1.destination = b;
  p1._plan();
  const p2 = new Passenger(city, 'p2', 3.0, a);
  p2.source = a;
  p2.destination = c;
  p2._plan();
  const p3 = new Passenger(city, 'p3', 3.0, a);
  p3.source = a;
  p3.destination = d;
  p3._plan();
  let journeys = city.getLongestJourneys(2);
  assert.deepEqual(journeys[0].planDuration, p3.planDuration);
  assert.deepEqual(journeys[1].planDuration, p2.planDuration);
});QUnit.test('get the k passengers with the longest journeys 1', (assert) => {
  const a = new Vertex('a');
  const b = new Vertex('b');
  const c = new Vertex('c');
  const d = new Vertex('d');
  const graph = new UndirectedGraph();
  graph.addVertex(a);
  graph.addVertex(b);
  graph.addVertex(c);
  graph.addVertex(d);
  graph.addEdge(a, new UndirectedEdge(2.0), b);
  graph.addEdge(b, new UndirectedEdge(7.0), c);
  graph.addEdge(c, new UndirectedEdge(5.0), d);
  const city = new City(graph, graph);
  const passenger1 = new Passenger(city, 'Joe', 3.0, a);
  const passenger2 = new Passenger(city, 'Huffin\' Mark', 3.0, b);
  const passenger3 = new Passenger(city, 'Santiago', 3.0, c);
  passenger1.source = a;
  passenger1.destination = d;
  passenger2.source = b;
  passenger2.destination = d;
  passenger3.source = c;
  passenger3.destination = d;
  passenger1.start();
  passenger2.start();
  passenger3.start();
  var result = city.getLongestJourneys(2);
  assert.deepEqual(result.length, 2);
  assert.ok([passenger1, passenger2].every(passengerInArray=>result.includes(passengerInArray)));
});

QUnit.test('get the k passengers with the longest journeys 2', (assert) => {
  const a = new Vertex('a');
  const b = new Vertex('b');
  const c = new Vertex('c');
  const d = new Vertex('d');
  const e = new Vertex('e');
  const graph = new UndirectedGraph();
  graph.addVertex(a);
  graph.addVertex(b);
  graph.addVertex(c);
  graph.addVertex(d);
  graph.addVertex(e);
  graph.addEdge(a, new UndirectedEdge(2.0), b);
  graph.addEdge(b, new UndirectedEdge(7.0), c);
  graph.addEdge(c, new UndirectedEdge(5.0), d);
  graph.addEdge(d, new UndirectedEdge(4.0), a);
  const city = new City(graph, graph);
  const passenger1 = new Passenger(city, 'Joe', 3.0, a);
  const passenger2 = new Passenger(city, 'Huffin\' Mark', 3.0, a);
  const passenger3 = new Passenger(city, 'Santiago', 3.0, a);
  passenger1.source = a;
  passenger1.destination = d;
  passenger2.source = a;
  passenger2.destination = c;
  passenger3.source = a;
  passenger3.destination = b;
  passenger1.start();
  passenger2.start();
  passenger3.start();
  var result = city.getLongestJourneys(1);
  assert.deepEqual(result.length, 1);
  assert.ok([passenger2].every(passengerInArray=>result.includes(passengerInArray)));
});QUnit.test('test getLongestJourneys by selecting the top one of two passengers', (assert) => {
  const a = new Vertex('a');
  const b = new Vertex('b');
  const c = new Vertex('c');
  const d = new Vertex('d');
  const e = new Vertex('e');
  const graph = new UndirectedGraph();
  graph.addVertex(a);
  graph.addVertex(b);
  graph.addVertex(c);
  graph.addVertex(d);
  graph.addVertex(e);
  graph.addEdge(a, new UndirectedEdge(4), b);
  graph.addEdge(b, new UndirectedEdge(3), c);
  graph.addEdge(c, new UndirectedEdge(2), d);
  graph.addEdge(d, new UndirectedEdge(1), e);
  const city = new City(graph, graph);
  const passengers = [new Passenger(city, 'p0', 2.0, a), new Passenger(city, 'p1', 2.0, a)];
  passengers[0].source = a;
  passengers[1].source = a;
  passengers[0].destination = b;
  passengers[1].destination = e;
  passengers[0].start();
  passengers[1].start();
  assert.deepEqual(city.getLongestJourneys(1)[0].name, passengers[1].name);
});

QUnit.test('test getLongestJourneys by selecting the top two of three passengers', (assert) => {
  const a = new Vertex('a');
  const b = new Vertex('b');
  const c = new Vertex('c');
  const d = new Vertex('d');
  const e = new Vertex('e');
  const graph = new UndirectedGraph();
  graph.addVertex(a);
  graph.addVertex(b);
  graph.addVertex(c);
  graph.addVertex(d);
  graph.addVertex(e);
  graph.addEdge(a, new UndirectedEdge(4), b);
  graph.addEdge(b, new UndirectedEdge(3), c);
  graph.addEdge(c, new UndirectedEdge(2), d);
  graph.addEdge(d, new UndirectedEdge(1), e);
  const city = new City(graph, graph);
  const passengers = [new Passenger(city, 'p0', 2.0, a), new Passenger(city, 'p1', 2.0, a), new Passenger(city, 'p2', 2.0, a)];
  passengers[0].source = a;
  passengers[1].source = a;
  passengers[2].source = a;
  passengers[0].destination = b;
  passengers[1].destination = c;
  passengers[2].destination = d;
  passengers.forEach(function(p){p.start()});
  let journeys = city.getLongestJourneys(2);
  assert.deepEqual(journeys[0].name, passengers[1].name);
  assert.deepEqual(journeys[1].name, passengers[2].name);

});

QUnit.test('longest journey test #1', (assert) => {
  const a = new Vertex('a');
  const b = new Vertex('b');
  const c = new Vertex('c');
  const graph = new UndirectedGraph();
  graph.addVertex(a);
  graph.addVertex(b);
  graph.addVertex(c);
  graph.addEdge(a, new UndirectedEdge(2), b);
  graph.addEdge(b, new UndirectedEdge(7), c);
  graph.addEdge(a, new UndirectedEdge(10), c);
  const city = new City(graph, graph);
  const passenger = new Passenger(city, 'p', 3.0, a);
  passenger.source = a;
  passenger.destination = c;
  passenger._plan();
  const passenger1 = new Passenger(city, 'p', 3.0, b);
  passenger1.source = b;
  passenger1.destination = c;
  passenger1._plan();
  const passenger2 = new Passenger(city, 'p', 3.0, a);
  passenger2.source = a;
  passenger2.destination = b;
  passenger2._plan();
  assert.deepEqual(city.getLongestJourneys(1), [passenger]);
});

QUnit.test('longest journey test #2', (assert) => {
  const a = new Vertex('a');
  const b = new Vertex('b');
  const c = new Vertex('c');
  const graph = new UndirectedGraph();
  graph.addVertex(a);
  graph.addVertex(b);
  graph.addVertex(c);
  graph.addEdge(a, new UndirectedEdge(2), b);
  graph.addEdge(b, new UndirectedEdge(7), c);
  graph.addEdge(a, new UndirectedEdge(10), c);
  const city = new City(graph, graph);
  const passenger = new Passenger(city, 'p', 3.0, a);
  passenger.source = a;
  passenger.destination = c;
  passenger._plan();
  const passenger1 = new Passenger(city, 'p', 3.0, b);
  passenger1.source = b;
  passenger1.destination = c;
  passenger1._plan();
  const passenger2 = new Passenger(city, 'p', 3.0, a);
  passenger2.source = a;
  passenger2.destination = b;
  passenger2._plan();
  assert.deepEqual(city.getLongestJourneys(2), [passenger, passenger1]);
});
QUnit.test('Test getLongestJourney with no duplicates', (assert) => {
  const a = new Vertex('a');
  const b = new Vertex('b');
  const c = new Vertex('c');
  const d = new Vertex('d');
  const e = new Vertex('e');
  const graph = new UndirectedGraph();
  graph.addVertex(a);
  graph.addVertex(b);
  graph.addVertex(c);
  graph.addVertex(d);
  graph.addVertex(e);
  graph.addEdge(a, new UndirectedEdge(1), b);
  graph.addEdge(b, new UndirectedEdge(1), c);
  graph.addEdge(c, new UndirectedEdge(1), d);
  graph.addEdge(d, new UndirectedEdge(1), e);
  const city = new City(graph, graph);

  const passenger1 = new Passenger(city, 'p1', 3.0, a);
  passenger1.source = a;
  passenger1.destination = c;
  passenger1._plan();

  const passenger2 = new Passenger(city, 'p2', 2.0, a);
  passenger2.source = a;
  passenger2.destination = d;
  passenger2._plan();

  const passenger3 = new Passenger(city, 'p3', 4.0, a);
  passenger3.source = a;
  passenger3.destination = e;
  passenger3._plan();

  assert.deepEqual(city.getLongestJourneys(1).map(passenger => passenger.planDuration), [4]);
  assert.deepEqual(city.getLongestJourneys(2).map(passenger => passenger.planDuration), [4, 3]);
});

QUnit.test('Test getLongestJourney with duplicates', (assert) => {
  const a = new Vertex('a');
  const b = new Vertex('b');
  const c = new Vertex('c');
  const d = new Vertex('d');
  const e = new Vertex('e');
  const graph = new UndirectedGraph();
  graph.addVertex(a);
  graph.addVertex(b);
  graph.addVertex(c);
  graph.addVertex(d);
  graph.addVertex(e);
  graph.addEdge(a, new UndirectedEdge(1), b);
  graph.addEdge(b, new UndirectedEdge(1), c);
  graph.addEdge(c, new UndirectedEdge(1), d);
  graph.addEdge(d, new UndirectedEdge(1), e);
  const city = new City(graph, graph);

  const passenger1 = new Passenger(city, 'p1', 3.0, a);
  passenger1.source = a;
  passenger1.destination = e;
  passenger1._plan();

  const passenger2 = new Passenger(city, 'p2', 2.0, a);
  passenger2.source = a;
  passenger2.destination = e;
  passenger2._plan();

  const passenger3 = new Passenger(city, 'p3', 4.0, a);
  passenger3.source = a;
  passenger3.destination = c;
  passenger3._plan();

  const passenger4 = new Passenger(city, 'p4', 2.0, a);
  passenger4.source = a;
  passenger4.destination = c;
  passenger4._plan();

  assert.deepEqual(city.getLongestJourneys(1).map(passenger => passenger.planDuration), [4]);
  assert.deepEqual(city.getLongestJourneys(2).map(passenger => passenger.planDuration), [4, 4]);
  assert.deepEqual(city.getLongestJourneys(3).map(passenger => passenger.planDuration), [4, 4, 2]);
});
QUnit.test('find the top three passengers with the longest journeys', (assert) => {
    const a = new Vertex('a');
    const b = new Vertex('b');
    const c = new Vertex('c');
    const d = new Vertex('d');
    const walkGraph = new UndirectedGraph();
    walkGraph.addVertex(a);
    walkGraph.addVertex(b);
    walkGraph.addVertex(c);
    walkGraph.addVertex(d);
    walkGraph.addEdge(a, new UndirectedEdge(4), b);
    walkGraph.addEdge(b, new UndirectedEdge(15), c);
    walkGraph.addEdge(c, new UndirectedEdge(26), d);
    const city = new City(walkGraph);
    const passenger1 = new Passenger(city, 'p1', 3.0, a);
    passenger1.source = a;
    passenger1.destination = b;
    passenger1.start();
    const passenger2 = new Passenger(city, 'p2', 3.0, a);
    passenger2.source = a;
    passenger2.destination = c;
    passenger2.start();
    const passenger3 = new Passenger(city, 'p3', 3.0, a);
    passenger3.source = a;
    passenger3.destination = d;
    passenger3.start();
    const passenger4 = new Passenger(city, 'p4', 3.0, a);
    passenger4.source = b;
    passenger4.destination = c;
    passenger4.start();
    const passenger5 = new Passenger(city, 'p5', 3.0, a);
    passenger5.source = b;
    passenger5.destination = d;
    passenger5.start();
    var longestJourneys = city.getLongestJourneys(3);
    assert.deepEqual(longestJourneys.indexOf(passenger2) > -1, true);
    assert.deepEqual(longestJourneys.indexOf(passenger3) > -1, true);
    assert.deepEqual(longestJourneys.indexOf(passenger5) > -1, true);
    assert.deepEqual(longestJourneys.indexOf(passenger1) > -1, false);
    assert.deepEqual(longestJourneys.indexOf(passenger4) > -1, false);
});

QUnit.test('the length of the array of longest journeys is of the desired length', (assert) => {
    const a = new Vertex('a');
    const b = new Vertex('b');
    const c = new Vertex('c');
    const d = new Vertex('d');
    const walkGraph = new UndirectedGraph();
    walkGraph.addVertex(a);
    walkGraph.addVertex(b);
    walkGraph.addVertex(c);
    walkGraph.addVertex(d);
    walkGraph.addEdge(a, new UndirectedEdge(4), b);
    walkGraph.addEdge(b, new UndirectedEdge(15), c);
    walkGraph.addEdge(c, new UndirectedEdge(26), d);
    const city = new City(walkGraph);
    const passenger1 = new Passenger(city, 'p1', 3.0, a);
    passenger1.source = a;
    passenger1.destination = b;
    passenger1.start();
    const passenger2 = new Passenger(city, 'p2', 3.0, a);
    passenger2.source = a;
    passenger2.destination = c;
    passenger2.start();
    const passenger3 = new Passenger(city, 'p3', 3.0, a);
    passenger3.source = a;
    passenger3.destination = d;
    passenger3.start();
    const passenger4 = new Passenger(city, 'p4', 3.0, a);
    passenger4.source = b;
    passenger4.destination = c;
    passenger4.start();
    const passenger5 = new Passenger(city, 'p5', 3.0, a);
    passenger5.source = b;
    passenger5.destination = d;
    passenger5.start();
    var longestJourneys0 = city.getLongestJourneys(0);
    assert.deepEqual(longestJourneys0.length, 0);
    var longestJourneys1 = city.getLongestJourneys(1);
    assert.deepEqual(longestJourneys1.length, 1);
    var longestJourneys2 = city.getLongestJourneys(2);
    assert.deepEqual(longestJourneys2.length, 2);
    var longestJourneys3 = city.getLongestJourneys(3);
    assert.deepEqual(longestJourneys3.length, 3);
    var longestJourneys4 = city.getLongestJourneys(4);
    assert.deepEqual(longestJourneys4.length, 4);
    var longestJourneys5 = city.getLongestJourneys(5);
    assert.deepEqual(longestJourneys5.length, 5);
});
QUnit.test('GET LONGEST JOURNEY PART TWO', (assert) => {
  const a = new Vertex('a');
  const b = new Vertex('b');
  const d = new Vertex('d');
  const graph = new UndirectedGraph();
  graph.addVertex(a);
  graph.addVertex(b);
  graph.addVertex(d);
  graph.addEdge(a, new UndirectedEdge(2), b);
  graph.addEdge(b, new UndirectedEdge(7), d);
  graph.addEdge(a, new UndirectedEdge(12), d);
  const city = new City(graph, graph);
  const passenger = new Passenger(city, 'p', 6.0, a);
  const passenger2 = new Passenger(city, 'p2', 5.0, a);
  const passenger3 = new Passenger(city, 'p3', 7.0, a);
  passenger.source = a;
  passenger.destination = d;
  passenger2.source = a;
  passenger2.destination = d;
  passenger3.source = a;
  passenger3.destination = d;
  // passenger2.source = b;
  // passenger2.destination = c;
  passenger._plan();
  // city.getLongestJourneys(1);
  console.log(city._passengers[0].duration);
  console.log(city._passengers[1].duration);
  console.log(city._passengers[2].duration);



  assert.deepEqual(city.getLongestJourneys(2), [passenger2, passenger3]);
});

QUnit.test('Get Longest journeys part 1', (assert) => {
  const a = new Vertex('a');
  const b = new Vertex('b');
  const c = new Vertex('c');
  const graph = new UndirectedGraph();
  graph.addVertex(a);
  graph.addVertex(b);
  graph.addVertex(c);
  graph.addEdge(a, new UndirectedEdge(2), b);
  graph.addEdge(b, new UndirectedEdge(7), c);
  graph.addEdge(a, new UndirectedEdge(12), c);
  const city = new City(graph, graph);
  const passenger = new Passenger(city, 'p', 6.0, a);
  const passenger2 = new Passenger(city, 'p2', 5.0, a);
  const passenger3 = new Passenger(city, 'p3', 7.0, a);
  passenger.source = a;
  passenger.destination = c;
  passenger2.source = a;
  passenger2.destination = c;
  passenger3.source = a;
  passenger3.destination = c;
  // passenger2.source = b;
  // passenger2.destination = c;
  passenger._plan();
  // city.getLongestJourneys(1);
  console.log(city._passengers[0].duration);
  console.log(city._passengers[1].duration);
  console.log(city._passengers[2].duration);



  assert.deepEqual(city.getLongestJourneys(2), [passenger2, passenger3]);
  //assert.deepEqual(instructions(passenger.plan, city), ['walk to c at time 10']);
});
QUnit.test('find the kth longest journeys of passengers in a city', (assert) => {
  const a = new Vertex('a');
  const b = new Vertex('b');
  const c = new Vertex('c');
  const d = new Vertex('d');
  const e = new Vertex('e');
  const f = new Vertex('f');
  const graph = new UndirectedGraph();
  graph.addVertex(a);
  graph.addVertex(b);
  graph.addVertex(c);
  graph.addVertex(d);
  graph.addVertex(e);
  graph.addVertex(f);
  graph.addEdge(a, new UndirectedEdge(1), b);
  graph.addEdge(b, new UndirectedEdge(1), c);
  graph.addEdge(c, new UndirectedEdge(1), d);
  graph.addEdge(d, new UndirectedEdge(1), e);
  graph.addEdge(e, new UndirectedEdge(1), f);
  const city = new City(graph, graph);

  const p2 = new Passenger(city, 'p2', 3.0, b);
  const p5 = new Passenger(city, 'p5', 3.0, e);
  const p1 = new Passenger(city, 'p1', 3.0, a);
  const p3 = new Passenger(city, 'p3', 3.0, c);
  const p4 = new Passenger(city, 'p4', 3.0, d);


  p2.source = b;
  p2.destination = f;
  p2._plan();

  p5.source = e;
  p5.destination = f;
  p5._plan();

  p1.source = a;
  p1.destination = f;
  p1._plan();

  p3.source = c;
  p3.destination = f;
  p3._plan();

  p4.source = d;
  p4.destination = f;
  p4._plan();

  assert.equal(p1.duration, 5);
  assert.equal(p2.duration, 4);
  assert.equal(p3.duration, 3);
  assert.equal(p4.duration, 2);
  assert.equal(p5.duration, 1);

  let result = city.getLongestJourneys(3);
  for(let i = 0; i < result.length; i++){
	  result[i] = result[i].duration;
  }
  assert.ok(result.indexOf(3) !== -1);
  assert.ok(result.indexOf(4) !== -1);
  assert.ok(result.indexOf(5) !== -1);
});

QUnit.test('find the kth longest journeys of passengers when k is invalid', (assert) => {
  const a = new Vertex('a');
  const b = new Vertex('b');
  const c = new Vertex('c');
  const d = new Vertex('d');
  const e = new Vertex('e');
  const f = new Vertex('f');
  const graph = new UndirectedGraph();
  graph.addVertex(a);
  graph.addVertex(b);
  graph.addVertex(c);
  graph.addVertex(d);
  graph.addVertex(e);
  graph.addVertex(f);
  graph.addEdge(a, new UndirectedEdge(1), b);
  graph.addEdge(b, new UndirectedEdge(1), c);
  graph.addEdge(c, new UndirectedEdge(1), d);
  graph.addEdge(d, new UndirectedEdge(1), e);
  graph.addEdge(e, new UndirectedEdge(1), f);
  const city = new City(graph, graph);

  const p2 = new Passenger(city, 'p2', 3.0, b);
  const p5 = new Passenger(city, 'p5', 3.0, e);
  const p1 = new Passenger(city, 'p1', 3.0, a);
  const p3 = new Passenger(city, 'p3', 3.0, c);
  const p4 = new Passenger(city, 'p4', 3.0, d);


  p2.source = b;
  p2.destination = f;
  p2._plan();

  p5.source = e;
  p5.destination = f;
  p5._plan();

  p1.source = a;
  p1.destination = f;
  p1._plan();

  p3.source = c;
  p3.destination = f;
  p3._plan();

  p4.source = d;
  p4.destination = f;
  p4._plan();

  assert.equal(p1.duration, 5);
  assert.equal(p2.duration, 4);
  assert.equal(p3.duration, 3);
  assert.equal(p4.duration, 2);
  assert.equal(p5.duration, 1);

  let result = city.getLongestJourneys(-1);
  assert.equal(result, undefined);
  result = city.getLongestJourneys(city.population+1);
  assert.equal(result, undefined);
});
QUnit.test('Get k passengers with longest journeys', (assert) => {
    const a = new Vertex('a');
  const b = new Vertex('b');
  const c = new Vertex('c');
  const d = new Vertex('d');
  const e = new Vertex('e');
  const walkGraph = new UndirectedGraph();
  walkGraph.addVertex(a);
  walkGraph.addVertex(b);
  walkGraph.addVertex(c);
  walkGraph.addVertex(d);
  walkGraph.addVertex(e);
  walkGraph.addEdge(a, new UndirectedEdge(4), b);
  walkGraph.addEdge(b, new UndirectedEdge(14), c);
  walkGraph.addEdge(c, new UndirectedEdge(14), d);
  walkGraph.addEdge(d, new UndirectedEdge(12), e);
  const driveGraph = new UndirectedGraph();
  driveGraph.addVertex(a);
  driveGraph.addVertex(b);
  driveGraph.addVertex(c);
  driveGraph.addVertex(d);
  driveGraph.addVertex(e);
  driveGraph.addEdge(b, new UndirectedEdge(7), c);
  driveGraph.addEdge(c, new UndirectedEdge(7), d);
  driveGraph.addEdge(d, new UndirectedEdge(7), e);
  driveGraph.addEdge(e, new UndirectedEdge(7), b);
  const city = new City(walkGraph, driveGraph);
  const route = new Route(city, b, e);
  route.patch(b, c, d, e);
  const x = new Bus(route.getArc(e)); // eslint-disable-line no-unused-vars
  const jim = new Passenger(city, 'Jim', 3.0, a);
  jim.source = a;
  jim.destination = d;
  jim._plan();
  const mary = new Passenger(city, 'Mary', 3.0, a);
  mary.source = a;
  mary.destination = b;
  mary._plan();
  const sam = new Passenger(city, 'Sam', 3.0, b);
  sam.source = b;
  sam.destination = e;
  sam._plan();
  const alex = new Passenger(city, 'Alex', 3.0, a);
  alex.source = b;
  alex.destination = c;
  alex._plan();
  var journeys = city.getLongestJourneys(2);
  assert.deepEqual(journeys, [alex, mary]);
});

QUnit.test('getLongestJourneys returns a list of the passenger\'s with the longest journeys (1 of 2 passengers)', (assert) => {
  const a = new Vertex('a');
  const b = new Vertex('b');
  const c = new Vertex('c');
  const graph = new UndirectedGraph();
  graph.addVertex(a);
  graph.addVertex(b);
  graph.addVertex(c);
  graph.addEdge(a, new UndirectedEdge(4), b);
  graph.addEdge(b, new UndirectedEdge(5), c);
  const city = new City(graph, graph);
  const passenger = new Passenger(city, 'p', 5.0, a);
  passenger.source = a;
  passenger.destination = b;
  passenger._plan();
  const passenger2 = new Passenger(city, 'p2', 3.0, c);
  passenger2.source = c;
  passenger2.destination = b;
  passenger2._plan();
  assert.deepEqual(city.getLongestJourneys(1).map((el) => [el.name, el.durationOfPlan]), [passenger2].map((el) => [el.name, el.durationOfPlan]));
});

QUnit.test('getLongestJourneys returns a list of the passenger\'s with the longest journeys (2 of 3 passengers)', (assert) => {
  const a = new Vertex('a');
  const b = new Vertex('b');
  const c = new Vertex('c');
  const d = new Vertex('d');
  const graph = new UndirectedGraph();
  graph.addVertex(a);
  graph.addVertex(b);
  graph.addVertex(c);
  graph.addVertex(d);
  graph.addEdge(a, new UndirectedEdge(4), b);
  graph.addEdge(b, new UndirectedEdge(5), c);
  graph.addEdge(c, new UndirectedEdge(5), d);
  graph.addEdge(a, new UndirectedEdge(7), d);
  const city = new City(graph, graph);
  const passenger = new Passenger(city, 'p', 5.0, a);
  passenger.source = a;
  passenger.destination = b;
  passenger._plan();
  const passenger2 = new Passenger(city, 'p2', 3.0, c);
  passenger2.source = c;
  passenger2.destination = b;
  passenger2._plan();
  const passenger3 = new Passenger(city, 'p3', 4.0, a);
  passenger3.source = a;
  passenger3.destination = d;
  passenger3._plan();
  assert.deepEqual(city.getLongestJourneys(2).map((el) => [el.name, el.durationOfPlan]), [passenger3, passenger2].map((el) => [el.name, el.durationOfPlan]));
});
QUnit.test('simulate a set of 5 passengers with set times ensure that only three are returned when count = 3 all passengers have the same time', (assert) => {
  //We need a city object as the getLongestJourneys belongs to the city
  const a = new Vertex('a');
  const b = new Vertex('c');
  const walkGraph = new UndirectedGraph();
  walkGraph.addVertex(a);
  walkGraph.addVertex(b);
  const driveGraph = new UndirectedGraph();
  driveGraph.addVertex(a);
  driveGraph.addVertex(b);
  driveGraph.addEdge(a, new UndirectedEdge(2), b);
  const city = new City(walkGraph, driveGraph);

  // we are only verifiying that the quick select works therefore we can just mock the passengers
  class passengerMock {
    constructor(duration) {
      this.duration = duration
    }
  }
  let passenger1 = new passengerMock(100)
  let passenger2 = new passengerMock(100)
  let passenger3 = new passengerMock(100)
  let passegner4 = new passengerMock(100)
  let passenger5 = new passengerMock(100)
  let passengers = [passenger1,passenger2,passenger3,passegner4,passenger5]

  let passengerArray = city.getLongestJourneys(3, passengers)

  //ensure that only three elements are returned
  assert.deepEqual(passengerArray.length, 3)

  //ensure that three elements with duration 100 are returned
  let totalDuration = 0;
  for(let i = 0; i < passengerArray.length; i++) {
    totalDuration += passengerArray[i].duration
  }

  assert.deepEqual(totalDuration, 300)
});

QUnit.test('simulate a set of 10 passengers with set times ensure that only one is returned when count = 1 all passengers have durations that are not integers', (assert) => {
  //We need a city object as the getLongestJourneys belongs to the city
  const a = new Vertex('a');
  const b = new Vertex('c');
  const walkGraph = new UndirectedGraph();
  walkGraph.addVertex(a);
  walkGraph.addVertex(b);
  const driveGraph = new UndirectedGraph();
  driveGraph.addVertex(a);
  driveGraph.addVertex(b);
  driveGraph.addEdge(a, new UndirectedEdge(2), b);
  const city = new City(walkGraph, driveGraph);

  // we are only verifiying that the quick select works therefore we can just mock the passengers
  class passengerMock {
    constructor(duration) {
      this.duration = duration
    }
  }
  let passenger1 = new passengerMock(1.01)
  let passenger2 = new passengerMock(10.11)
  let passenger3 = new passengerMock(100.32)
  let passegner4 = new passengerMock(101.56)
  let passenger5 = new passengerMock(103.6413)
  let passenger6 = new passengerMock(105.5131)
  let passenger7 = new passengerMock(43.3145)
  let passenger8 = new passengerMock(32.14414)
  let passegner9 = new passengerMock(53.13431)
  let passenger10 = new passengerMock(67.1343)
  let passengers = [passenger1,passenger2,passenger3,passegner4,passenger5,passenger6,passenger7,passenger8,passegner9,passenger10]

  let passengerArray = city.getLongestJourneys(1, passengers)

  // ensure that only one element is returned
  assert.deepEqual(passengerArray.length, 1)

  // ensure that the duration of the only element is 105.5131 we can guarantee that we only have one element and thus not have to take the sum, because of the assert above.

  assert.deepEqual(passengerArray[0].duration, 105.5131)
});
QUnit.test('get longest plans in simple city', (assert) => {
  const a = new Vertex('a');
  const b = new Vertex('b');
  const c = new Vertex('c');
  const d = new Vertex('d');
  const e = new Vertex('e');
  const graph = new UndirectedGraph();
  graph.addVertex(a);
  graph.addVertex(b);
  graph.addVertex(c);
  graph.addVertex(d);
  graph.addVertex(e);
  graph.addEdge(a, new UndirectedEdge(3), b);
  graph.addEdge(b, new UndirectedEdge(3), c);
  graph.addEdge(c, new UndirectedEdge(3), d);
  graph.addEdge(d, new UndirectedEdge(3), e);
  const city = new City(graph, graph);
  const p1 = new Passenger(city, 'p1', 3.0, a);
  p1.source = a;
  p1.destination = e;
  p1._plan();
  const p2 = new Passenger(city, 'p2', 3.0, b);
  p2.source = b;
  p2.destination = e;
  p2._plan();
  const p3 = new Passenger(city, 'p3', 3.0, b);
  p3.source = b;
  p3.destination = e;
  p3._plan();
  const p4 = new Passenger(city, 'p4', 3.0, b);
  p4.source = c;
  p4.destination = e;
  p4._plan();

  //sort by plan duration first, then by name so ties sort correctly
  const passengerCompare = (p1, p2) => p1.planDuration - p2.planDuration != 0 ? p1.planDuration - p2.planDuration : p1.name < p2.name;
  assert.deepEqual(city.getLongestJourneys(0).sort(passengerCompare), []);
  assert.deepEqual(city.getLongestJourneys(1).sort(passengerCompare), [p1]);
  assert.deepEqual(city.getLongestJourneys(3).sort(passengerCompare), [p1, p2, p3].sort(passengerCompare));
  assert.deepEqual(city.getLongestJourneys(4).sort(passengerCompare), [p1, p2, p3, p4].sort(passengerCompare));
  assert.deepEqual(city.getLongestJourneys(5).sort(passengerCompare), [p1, p2, p3, p4].sort(passengerCompare));
});
QUnit.test('simulate longest journeys', (assert) => {
  const a = new Vertex('a');
  const b = new Vertex('b');
  const c = new Vertex('c');
  const d = new Vertex('d');
  const graph = new UndirectedGraph();
  graph.addVertex(a);
  graph.addVertex(b);
  graph.addVertex(c);
  graph.addVertex(d);
  graph.addEdge(a, new UndirectedEdge(4), b);
  graph.addEdge(b, new UndirectedEdge(15), c);
  graph.addEdge(c, new UndirectedEdge(15), d);
  const city = new City(graph, graph);

  const passenger1 = new Passenger(city, 'p1 - 2', 2, a);
  const passenger2 = new Passenger(city, 'p2 - 1.5', 1.5, b);
  const passenger3 = new Passenger(city, 'p3 - 5', 5, b);
  const passenger4 = new Passenger(city, 'p4 - 3', 3, c);
  const passenger5 = new Passenger(city, 'p5 - 1', 1, d);
  const passenger6 = new Passenger(city, 'p6 - 0.5', 0.5, a);
  // sorted = [p6, p5, p2, p1, p4, p3]

  assert.deepEqual(city.getLongestJourney(2), [passenger4, passenger3]);
  assert.deepEqual(city.getLongestJourney(1), [passenger3]);
  assert.deepEqual(city.getLongestJourney(5), [passenger5, passenger2, passenger1, passenger4, passenger3]);
});
