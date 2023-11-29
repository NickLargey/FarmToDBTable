const hub_county = "SELECT * FROM HUB WHERE hub_county = 'Cumberland'"



document.getElementById("queryForm").addEventListener("submit", function (e) {
  e.preventDefault();
  const query = document.getElementById("query").value;

  // Send a POST request to the Flask API using Axios
  axios
    .post("/api/query", { query: query })
    .then((response) => {
      const resultsContainer = document.getElementById("results");
      resultsContainer.innerHTML = "";

      if (response.data.results.length > 0) {
        response.data.results.forEach((result) => {
          const resultElement = document.createElement("p");
          resultElement.textContent = result;
          resultsContainer.appendChild(resultElement);
        });
      } else {
        resultsContainer.textContent = "No results found.";
      }
    })
    .catch((error) => {
      console.error("Error:", error);
    });
});