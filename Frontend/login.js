// document.getElementById("loginForm").addEventListener("submit", function (e) {
//   e.preventDefault();
//   const username = document.getElementById("username").value;

//   // Create a data object to send in the request body
//   const data = {
//     username: username,
//   };

//   // Make a POST request using Axios
//   axios
//     .post("/login", data, {
//       headers: {
//         "Content-Type": "application/json",
//       },
//     })
//     .then((response) => {
//       console.log("Response:", response);
//       document.getElementById("message").textContent = response.data.message;
//     })
//     .catch((error) => {
//       console.error("Error:", error);
//       document.getElementById("message").textContent =
//         error.response.data.message;
//     });
// });
