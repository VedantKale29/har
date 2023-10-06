// Get the video element
const videoElement = document.getElementById("video");

// Check for camera support
if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
    navigator.mediaDevices
        .getUserMedia({ video: true })
        .then(function (stream) {
            // Display the video stream in the video element
            videoElement.srcObject = stream;
        })
        .catch(function (error) {
            console.error("Error accessing the camera:", error);
        });
} else {
    console.error("Camera access not supported by your browser.");
}
