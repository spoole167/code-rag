import ReactMarkdown from "react-markdown";

const ResponseDisplay = ({ response }) => {
  return (
    <div style={{ textAlign: "left", padding: "10px", border: "1px solid #ddd", marginTop: "10px" }}>
      <h3>Response:</h3>
      <ReactMarkdown>{response || "_Waiting for response..._"}</ReactMarkdown>
    </div>
  );
};

export default ResponseDisplay;
