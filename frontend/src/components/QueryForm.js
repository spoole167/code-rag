const QueryForm = ({ query, setQuery, onSubmit }) => {
    return (
      <div>
        <input
          type="text"
          value={query}
          placeholder="Enter a query (e.g., Find security bugs)"
          onChange={(e) => setQuery(e.target.value)}
        />
        <button onClick={onSubmit}>Submit</button>
      </div>
    );
  };

  export default QueryForm;
  