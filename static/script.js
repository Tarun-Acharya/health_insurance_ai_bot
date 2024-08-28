document.addEventListener("DOMContentLoaded", function () {
  // Handle file input change event to display file name
  document.getElementById("fileInput").addEventListener("change", function () {
    const file = this.files[0];
    const uploadStatus = document.getElementById("uploadStatus");

    if (file) {
      uploadStatus.textContent = `Selected file: ${file.name}`;
    } else {
      uploadStatus.textContent = "No file selected.";
    }
  });

  // Handle form submission for file upload
  document
    .getElementById("uploadForm")
    .addEventListener("submit", function (e) {
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

  // Handle form submission for chat questions
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

        // Replace **bold** with a marker, like __BOLD_START__text__BOLD_END__
        let formattedText = (data.answer || data.error).replace(
          /\*\*(.*?)\*\*/g,
          "__BOLD_START__$1__BOLD_END__"
        );

        // Use innerText to preserve formatting
        responseText.innerText = formattedText;

        //Replace markers with bold styling
        responseText.innerHTML = responseText.innerHTML
          .replace(/__BOLD_START__/g, "<strong>")
          .replace(/__BOLD_END__/g, "</strong>");
      })
      .catch((error) => {
        console.error("Error:", error);
        loadingIndicator.classList.add("hidden"); // Hide the loading spinner in case of an error
        responseText.innerText = "An error occurred.";
      });
  });
});
