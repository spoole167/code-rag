const API_BASE_URL = "http://localhost:5000";

export const queryRAG = async (queryText) => {
  try {
    const res = await fetch(`${API_BASE_URL}/query`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ query: queryText }),
    });
    return await res.json();
  } catch (error) {
    console.error("API Error:", error);
    return { response: "Error connecting to backend." };
  }
};
    