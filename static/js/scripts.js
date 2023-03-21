document.addEventListener("DOMContentLoaded", () => {

  const uploadForm = document.getElementById("upload-form");
  const audioInput = document.getElementById("audio");
  const chooseBtn = document.getElementById("choose-btn");
  const submitBtn = document.getElementById("submit-btn");
  const loadingIcon = document.getElementById("loading-icon");
  const processingText = document.getElementById("processing-text");
  const downloadLink = document.getElementById("download-link");
  const dropArea = document.getElementById("drop-area");
  const link = document.getElementById("link");
  const loadingText = document.getElementById("loading-text");
  const resetBtn = document.getElementById("reset-btn");



  // Show loading icon and hide other elements
function showProcessing() {
  chooseBtn.classList.add("hidden");
  submitBtn.classList.add("hidden");
  loadingIcon.classList.remove("hidden");
  processingText.classList.add("hidden");
  downloadLink.classList.add("hidden");
  loadingText.classList.remove("hidden");
  loadingText.classList.remove("text-gray-500", "text-sm", "mt-2"); // remove these classes
  loadingIcon.classList.add("animate-spin", "h-5", "w-5", "mr-3");
  chooseBtn.classList.add("cursor-not-allowed", "opacity-50");
  submitBtn.classList.add("cursor-not-allowed", "opacity-50");
}


  // Show processing text and hide other elements
  // function showProcessing() {
  //   console.log('showProcessing');
  //   loadingIcon.classList.add("hidden");
  //   processingText.classList.remove("hidden");
  // }

  // Show submit button and hide other elements
  function showSubmitBtn() {
  console.log('showSubmitBtn');
    console.log(submitBtn.classList);
    resetBtn.classList.remove("hidden");
  processingText.classList.add("hidden");
  if (submitBtn.classList.contains("hidden")) {
    submitBtn.classList.remove("hidden");
  }
}

  // Show download link
 function showDownloadLink(url) {
   downloadLink.href = "/download/transcription"
  //  url;
  loadingIcon.classList.add("hidden");
  processingText.classList.add("hidden");
  downloadLink.classList.remove("hidden");
}


  // Show notification message
  function showNotification(message) {
    console.log('showNotification');
    document.getElementById("notification-text").textContent = message;
    document.getElementById("notification").classList.remove("hidden");
    document.getElementById("transcription").classList.remove("hidden");
  }

  // Drag and drop file functionality
  dropArea.addEventListener("dragenter", (e) => {
    e.preventDefault();
    dropArea.classList.add("hover");
  });

  dropArea.addEventListener("dragleave", (e) => {
    e.preventDefault();
    dropArea.classList.remove("hover");
  });

  dropArea.addEventListener("dragover", (e) => {
    e.preventDefault();
  });

  dropArea.addEventListener("drop", (e) => {
    e.preventDefault();
    dropArea.classList.remove("hover");
    const file = e.dataTransfer.files[0];
    // document.getElementById("audio").files = [file];
    document.getElementById("audio").files = e.dataTransfer.files;

    uploadForm.dispatchEvent(new Event("submit"));
  });

  // Choose file button functionality
  chooseBtn.addEventListener("click", () => {
    audioInput.click();
  });

  audioInput.addEventListener("change", () => {
    uploadForm.dispatchEvent(new Event("submit"));
  });
//   function showTranscription(transcription) {
//   const transcriptionText = document.getElementById("transcription-text");
//   transcriptionText.textContent = transcription;
//   document.getElementById("transcription").classList.remove("hidden");
// }
  // Reset functionality
  resetBtn.addEventListener("click", () => {
    audioInput.value = "";
    document.getElementById("bar").style.width = "0%";
    document.getElementById("transcription-text").textContent = "";
    document.getElementById("processing-text").classList.add("hidden");
    document.getElementById("transcription").classList.add("hidden");
    document.getElementById("submit-btn").classList.add("hidden");
    document.getElementById("choose-btn").classList.remove("hidden");
    document.getElementById("download-link").classList.add("hidden");
    document.getElementById("notification").classList.add("hidden");
    document.getElementById("loading-text").classList.add("hidden");
    
    chooseBtn.classList.remove("cursor-not-allowed", "opacity-50");

    // choose-btn
    resetBtn.classList.add("hidden");
  });
// Form submit functionality
uploadForm.addEventListener("submit", (e) => {
  e.preventDefault();
  const formData = new FormData(uploadForm);
  const xhr = new XMLHttpRequest();
  xhr.open("POST", "/api/transcribe");
  xhr.upload.addEventListener("progress", (event) => {
    // showLoading();
    const percent = (event.loaded / event.total) * 100;
    document.getElementById("bar").style.width = percent + "%";
  });
  xhr.onreadystatechange = () => {
    if (xhr.readyState === 4) {
      if (xhr.status === 200) {
        const response = xhr.responseText;
        const url = response.match(/href=['"]?([^'">]+)['"]?/)[1];
        showDownloadLink(url);
        showSubmitBtn();
        showNotification("Transcription complete!");
      } else {
        showNotification("Error: " + xhr.statusText);
      }
    } else {
      // showLoading();
      showNotification("Uploading...");
    }
  };
  showProcessing();
  xhr.send(formData)
});
});
