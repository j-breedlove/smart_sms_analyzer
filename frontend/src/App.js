import React, { useState, useEffect } from 'react';
import axios from 'axios';

function App() {
  const [data, setData] = useState(null);

  useEffect(() => {
    // Making a GET request to the Flask backend
    axios.get('http://localhost:5000/api/test')
        .then((response) => {
          setData(response.data.message);
        })
        .catch((error) => {
          console.error("Error fetching the data", error);
        });
  }, []);

  return (
      <div>
        {data ? data : "Loading..."}
      </div>
  );
}

export default App;
