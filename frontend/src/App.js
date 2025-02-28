import { useState } from "react";
import QueryForm from "./components/QueryForm";
import ResponseDisplay from "./components/ResponseDisplay";
import "./App.css";

function App() {
  const [query, setQuery] = useState("");
  const [response, setResponse] = useState("");

  const handleQuerySubmit = async () => {
    try {
      const res = await fetch("http://localhost:5000/query", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query }),
      });

      const data = await res.json();
      setResponse(data.response);
      console.log(data.response);
    } catch (error) {
      console.error("Error fetching response:", error);
      setResponse("Error connecting to backend.");
    }
  };

  return (
    <div className="container">
      <h1>Code-RAG Query</h1>
      <QueryForm query={query} setQuery={setQuery} onSubmit={handleQuerySubmit} />
      <ResponseDisplay response={response} />
    </div>
  );
}

export default App;
