import Dashboard from "./components/Dashboard";
import "./App.css";

function App() {
  return (
    <div className="app">
      <header className="app-header">
        <h1>API Rate Limit Visualizer</h1>
        <p className="app-subtitle">Monitor and analyze your API consumption patterns</p>
      </header>
      <main>
        <Dashboard />
      </main>
    </div>
  );
}

export default App;
