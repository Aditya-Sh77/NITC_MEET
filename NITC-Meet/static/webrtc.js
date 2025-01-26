// Select video elements and buttons
const localVideo = document.getElementById("localVideo");
const remoteVideo = document.getElementById("remoteVideo");
const muteButton = document.getElementById("muteButton");
const cameraButton = document.getElementById("cameraButton");
const leaveButton = document.getElementById("leaveButton");
const skipButton = document.getElementById("skipButton");

// Initialize WebRTC and Socket.IO
let peerConnection = new RTCPeerConnection({
  iceServers: [{ urls: "stun:stun.l.google.com:19302" }],
});
const socket = io('http://127.0.0.1:3000');
let localStream;
let isAudioMuted = false;
let isCameraOff = false;

// Get user media (audio and video)
async function getLocalStream() {
  try {
    localStream = await navigator.mediaDevices.getUserMedia({ video: true, audio: true });
    localVideo.srcObject = localStream;

    // Add tracks to the peer connection
    localStream.getTracks().forEach((track) => peerConnection.addTrack(track, localStream));
  } catch (error) {
    console.error("Error accessing media devices:", error);
  }
}

// Handle remote stream
peerConnection.ontrack = (event) => {
  remoteVideo.srcObject = event.streams[0];
};

// Handle ICE candidates
peerConnection.onicecandidate = (event) => {
  if (event.candidate) {
    console.log("ICE candidate:", event.candidate);
    socket.emit("signal", { candidate: event.candidate });
  }

  
};

// Socket.IO signaling
socket.on("signal", async (data) => {
  if (data.action === "new_peer") {
    console.log(`New peer assigned: ${data.peer_id}`);
    createOffer(); // Start a new connection
  }
    
  if (data.action === "no_peer") {
    console.log("No peers available.");
  }
  if (data.candidate) {
    console.log("Received ICE candidate:", data.candidate);
    await peerConnection.addIceCandidate(data.candidate);
  }
  if (data.offer) {
    await peerConnection.setRemoteDescription(new RTCSessionDescription(data.offer));
    const answer = await peerConnection.createAnswer();
    await peerConnection.setLocalDescription(answer);
    socket.emit("signal", { answer });
  }
  if (data.answer) {
    await peerConnection.setRemoteDescription(new RTCSessionDescription(data.answer));
  }
});

// Create and send an offer
async function createOffer() {
  const offer = await peerConnection.createOffer();
  await peerConnection.setLocalDescription(offer);
  socket.emit("signal", { offer });
}

// Initial video chat (first-time connection)
function startInitialConnection() {
   console.log("Starting initial connection..."); 
  // Ask the server for a random peer when the user connects
  socket.emit('request_random_peer');
  console.log("Random peer request sent.");
}

// Handle button actions

cameraButton.addEventListener("click", () => {
  isCameraOff = !isCameraOff;
  localStream.getVideoTracks()[0].enabled = !isCameraOff;
  cameraButton.textContent = isCameraOff ? "Turn On Camera" : "Turn Off Camera";
});

muteButton.addEventListener("click", () => {
  isAudioMuted = !isAudioMuted;
  localStream.getAudioTracks()[0].enabled = !isAudioMuted;
  muteButton.textContent = isAudioMuted ? "Unmute" : "Mute";
});

leaveButton.addEventListener("click", () => {
  // Close the peer connection and navigate to the main page
  peerConnection.close();
  socket.disconnect();

  window.location.href = "/templates/welcome";
});

skipButton.addEventListener("click", () => {
  console.log("Skipping current peer...");
  if (peerConnection) {
    peerConnection.close();
    peerConnection = null;
    console.log("Peer connection closed.");
    
    console.log(connected_users);
  }  
  // Restart the WebRTC connection
  socket.emit("skip");
  setupNewConnection();
});

// Set up a new connection
async function setupNewConnection() {
  peerConnection = new RTCPeerConnection({
    iceServers: [{ urls: "stun:stun.l.google.com:19302" }],
  });
  
  if (localStream) {
    localStream.getTracks().forEach((track) => peerConnection.addTrack(track, localStream));
  }



  peerConnection.ontrack = (event) => {
    remoteVideo.srcObject = event.streams[0];
  };
  peerConnection.onicecandidate = (event) => {
    if (event.candidate) {
      socket.emit("signal", { candidate: event.candidate });
    }
  };
}

// Start the connection
createOffer();
getLocalStream().then(() => {
    setupNewConnection();
    startInitialConnection();
  });


