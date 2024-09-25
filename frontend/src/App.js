import React, { useState, useEffect } from 'react';
import './App.css';

function App() {
  const [graph, setGraph] = useState(null);
  const [poslanec, setPoslanec] = useState(null);
  const [hlasovani, setHlasovani] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    // Fetch graph data
    fetch('http://localhost:5000/api/data/graph')
      .then(response => {
        if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
        return response.json();
      })
      .then(data => setGraph(data))
      .catch(error => {
        console.error('Error fetching graph:', error);
        setError(error.message);
      });

    // Fetch a sample poslanec (ID 1 for example)
    fetch('http://localhost:5000/api/poslanec/1')
      .then(response => {
        if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
        return response.json();
      })
      .then(data => setPoslanec(data))
      .catch(error => console.error('Error fetching poslanec:', error));

    // Fetch a sample hlasovani (ID 1 for example)
    fetch('http://localhost:5000/api/hlasovani/77760')
      .then(response => {
        if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
        return response.json();
      })
      .then(data => setHlasovani(data))
      .catch(error => console.error('Error fetching hlasovani:', error));
  }, []);

  const limitedGraph = graph ? Object.fromEntries(
    Object.entries(graph).slice(0, 2).map(([hlasovaniId, poslanci]) => [
      hlasovaniId,
      Object.fromEntries(Object.entries(poslanci).slice(0, 2))
    ])
  ) : null;

  return (
    <div className="App">
      <header className="App-header">
        <h1>Parliament Data Viewer</h1>

        {error && <p>Error: {error}</p>}

        {limitedGraph && (
          <div>
            <h2>Graph Data (first 2 hlasovani, first 2 poslanci each)</h2>
            <pre>
              {JSON.stringify(limitedGraph, null, 2)}
            </pre>
          </div>
        )}

        {poslanec && (
          <div>
            <h2>Sample Poslanec</h2>
            <p>ID: {poslanec.id}</p>
            <p>Name: {poslanec.name}</p>
          </div>
        )}

        {hlasovani && (
          <div>
            <h2>Sample Hlasovani</h2>
            <p>ID: {hlasovani.id}</p>
            <p>Name: {hlasovani.name}</p>
          </div>
        )}

        {!graph && !poslanec && !hlasovani && <p>Loading...</p>}
      </header>
    </div>
  );
}

export default App;