function processVideo() {
  var videoUrl = document.getElementById("videoUrl").value;
  fetch("/process-video", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ videoUrl: videoUrl }),
  })
    .then((response) => response.blob())
    .then((blob) => {
      // Create a URL for the blob
      var processedVideoUrl = URL.createObjectURL(blob);
      // Optionally, download the video directly
      var a = document.createElement("a");
      a.href = processedVideoUrl;
      a.download = "processedVideo.mp4";
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
    })
    .catch((error) => console.error("Error:", error));
}
