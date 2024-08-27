document.getElementById("uploadForm").addEventListener("submit", function (e) {
  e.preventDefault();
  let formData = new FormData();
  let file = document.getElementById("fileInput").files[0];
  formData.append("file", file);

  // Show initial status message
  let uploadStatus = document.getElementById("uploadStatus");
  uploadStatus.textContent = "Ingesting into vector db...";

  fetch("/upload", {
    method: "POST",
    body: formData,
  })
    .then((response) => response.json())
    .then((data) => {
      // Update status with the final message
      uploadStatus.textContent = data.text || data.error;
    })
    .catch((error) => {
      console.error("Error:", error);
      uploadStatus.textContent = "An error occurred.";
    });
});

document.getElementById("chatForm").addEventListener("submit", function (e) {
  e.preventDefault();
  let question = document.getElementById("questionInput").value;
  let responseText = document.getElementById("responseText");
  let loadingIndicator = document.getElementById("loadingIndicator");

  // Show loading indicator
  loadingIndicator.classList.remove("hidden");
  responseText.textContent = ""; // Clear previous response

  fetch("/ask", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ question: question }),
  })
    .then((response) => response.json())
    .then((data) => {
      // Hide loading indicator
      loadingIndicator.classList.add("hidden");
      responseText.textContent = data.answer || data.error;
    })
    .catch((error) => {
      console.error("Error:", error);
      loadingIndicator.classList.add("hidden"); // Hide the loading spinner in case of an error
      responseText.textContent = "An error occurred.";
    });
});
