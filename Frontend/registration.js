// document
//   .getElementById("registrationForm")
//   .addEventListener("submit", function (e) {
//     e.preventDefault();
//     const username = document.getElementById("username").value;
//     // const password = document.getElementById("password").value;

//     // Create a data object to send in the request body
//     const data = {
//       username: username,
//       // password: password,
//     };

//     // Make a POST request using Axios
//     axios
//       .post("/register", data, {
//         headers: {
//           "Content-Type": "application/json",
//         },
//       })
//       .then((response) => {
//         document.getElementById("message").textContent = response.data.message;
//       })
//       .catch((error) => {
//         console.error("Error:", error);
//         document.getElementById("message").textContent =
//           error.response.data.message;
//       });
//   });
