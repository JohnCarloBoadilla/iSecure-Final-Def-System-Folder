document.addEventListener("DOMContentLoaded", () => {

  // ----- Buttons & Elements -----
  const nextToVerifyBtn = document.getElementById("nextToVerify");
  const nextToFacialBtn = document.getElementById("nextToFacial");
  const nextToVehicleBtn = document.getElementById("nextToVehicle");
  const nextToIdBtn = document.getElementById("nextToId");
  const skipVehicleBtn = document.getElementById("skipVehicle");
  const rejectBtn = document.getElementById("rejectBtn");
  const markEntryBtn = document.getElementById("markEntryBtn");
  const saveTimeBtn = document.getElementById("saveTimeBtn");
  const logoutLink = document.getElementById("logout-link");
  const idTabImage = document.getElementById("idTabImage");
  const ocrContent = document.getElementById("ocrContent");
  const recognizeFaceBtn = document.getElementById("recognizeFaceBtn");
  const recognizeVehicleBtn = document.getElementById("recognizeVehicleBtn");
  const facialResult = document.getElementById("facialResult");
  const vehicleResult = document.getElementById("vehicleResult");
  const expectedVisitorsTbody = document.querySelector("#expectedVisitorsTable tbody");
  const insideVisitorsTbody = document.querySelector("#insideVisitorsTable tbody");
  const exitedVisitorsTbody = document.querySelector("#exitedVisitorsTable tbody");

  // New elements for facial authentication
  const cameraSourceSelect = document.getElementById("cameraSource");
  const authVideoFeed = document.getElementById("auth-video-feed");
  const cctvFeed = document.getElementById("cctv-feed");
  const authenticateBtn = document.getElementById("authenticate-btn");
  const authResultDiv = document.getElementById("auth-result");

  // Vehicle recognition elements
  const expectedPlateNumberDisplay = document.getElementById("expectedPlateNumberDisplay");
  const cameraFeed = document.getElementById("cameraFeed");
  const recognizedPlateDisplay = document.getElementById("recognizedPlateDisplay");
  const verificationStatus = document.getElementById("verificationStatus");
  const scanPlateBtn = document.getElementById("scanPlateBtn");

  let currentVisitorId = null;
  let currentSelfiePath = null;
  let currentStream = null; // To store the webcam stream

  // ----- Helper Functions -----
  function escapeHtml(s) {
    if (!s) return "";
    return String(s)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }

  function showTab(tabId) {
    const tabTrigger = document.querySelector(`#visitorTab button[data-bs-target="#${tabId}"]`);
    if (tabTrigger) {
      const tab = new bootstrap.Tab(tabTrigger);
      tab.show();
    }
  }

  // Function to stop any active camera stream
  function stopCamera() {
    if (currentStream) {
      currentStream.getTracks().forEach(track => track.stop());
      currentStream = null;
    }
    if (authVideoFeed) authVideoFeed.style.display = 'none';
    if (cctvFeed) cctvFeed.style.display = 'none';
  }

  // Function to start webcam stream
  async function startWebcam() {
    stopCamera();
    try {
      currentStream = await navigator.mediaDevices.getUserMedia({ video: true });
      if (authVideoFeed) {
        authVideoFeed.srcObject = currentStream;
        authVideoFeed.style.display = 'block';
      }
      // Inform backend about camera source
      await fetch(`${API_BASE_URL}/camera/source`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ camera_type: 'facial', source: 'webcam' })
      });
    } catch (err) {
      console.error("Error accessing webcam: ", err);
      if (authResultDiv) authResultDiv.innerHTML = `<div class="alert alert-danger">Error: Could not access webcam.</div>`;
    }
  }

  // Function to start CCTV feed
  async function startCCTVFeed() {
    stopCamera();
    if (cctvFeed) {
      cctvFeed.src = `${API_BASE_URL}/camera/facial/frame`; // Set src to start stream
      cctvFeed.style.display = 'block';
      // Inform backend about camera source
      await fetch(`${API_BASE_URL}/camera/source`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ camera_type: 'facial', source: 'cctv' })
      });
    }
  }

  // Event listener for camera source selection
  cameraSourceSelect?.addEventListener('change', (event) => {
    const selectedSource = event.target.value;
    if (selectedSource === 'webcam') {
      startWebcam();
    } else if (selectedSource === 'cctv') {
      startCCTVFeed();
    }
  });

  async function fetchVisitorDetails(visitorId) {
    try {
      const res = await fetch(`fetch_visitor_details.php?id=${encodeURIComponent(visitorId)}`);
      const visitor = await res.json();

      if (!visitor.success) {
        alert(visitor.message || "Visitor data not found");
        return null;
      }

      return visitor.data;
    } catch (err) {
      console.error(err);
      alert("Failed to fetch visitor details.");
      return null;
    }
  }

    function showVisitorDetails(visitor) {
      // Combine first and last name for Name column
      const fullName = [visitor.first_name, visitor.middle_name,  visitor.last_name].filter(Boolean).join(' ');
      document.getElementById("visitorNameCell").textContent = escapeHtml(fullName);
      document.getElementById("visitorAddressCell").textContent = escapeHtml(visitor.address);
      document.getElementById("visitorContactCell").textContent = escapeHtml(visitor.contact_number);
      document.getElementById("visitorEmailCell").textContent = escapeHtml(visitor.email);
      document.getElementById("visitorDateCell").textContent = escapeHtml(visitor.date || '');
      document.getElementById("visitorTimeCell").textContent = escapeHtml(visitor.time_in || '');
      document.getElementById("visitorPersonnelCell").textContent = escapeHtml(visitor.personnel_related || '');
      document.getElementById("visitorOfficeCell").textContent = escapeHtml(visitor.office_to_visit || '');
      document.getElementById("vehicleOwnerCell").textContent = escapeHtml(visitor.vehicle_owner || fullName);
      document.getElementById("vehicleBrandCell").textContent = escapeHtml(visitor.vehicle_brand || '');
      document.getElementById("vehicleModelCell").textContent = escapeHtml(visitor.vehicle_model || '');
      document.getElementById("vehicleColorCell").textContent = escapeHtml(visitor.vehicle_color || '');
      document.getElementById("plateNumberCell").textContent = escapeHtml(visitor.plate_number || '');
      document.getElementById("visitorIDPhoto").src = visitor.id_photo_path;
      document.getElementById("visitorSelfie").src = visitor.selfie_photo_path;
      // document.getElementById("facialSelfie").src = visitor.selfie_photo_path; // This element doesn't exist
      document.getElementById("expectedPlateNumberDisplay").textContent = visitor.plate_number || ''; // Corrected ID
      idTabImage.src = visitor.id_photo_path;
      currentVisitorId = visitor.id;
      currentSelfiePath = visitor.selfie_photo_path;

    // Hide vehicle columns if no vehicle
    const vehicleColumns = document.querySelectorAll(".visitor-vehicle-column");
    const vehicleHeaders = ["visitorVehicleOwnerHeader", "visitorVehicleBrandHeader", "visitorVehicleModelHeader", "visitorVehicleColorHeader", "visitorPlateNumberHeader"];
    const hasVehicle = visitor.vehicle_brand && visitor.vehicle_brand.trim() !== "";
    vehicleColumns.forEach(col => {
      col.style.display = hasVehicle ? "table-cell" : "none";
    });
    vehicleHeaders.forEach(headerId => {
      const header = document.getElementById(headerId);
      if (header) header.style.display = hasVehicle ? "table-cell" : "none";
    });

    // Show/Hide tabs based on status
    const verifyTabBtn = document.querySelector('#visitorTab button[data-bs-target="#verify"]');
    const facialTabBtn = document.querySelector('#visitorTab button[data-bs-target="#facial"]');
    const vehicleTabBtn = document.querySelector('#visitorTab button[data-bs-target="#vehicle"]');
    const idTabBtn = document.querySelector('#visitorTab button[data-bs-target="#id"]');
    const detailsTabBtn = document.querySelector('#visitorTab button[data-bs-target="#details"]');

    const isReadOnly = visitor.status.toLowerCase() === "inside" || visitor.status.toLowerCase() === "exited";

    [verifyTabBtn, facialTabBtn, vehicleTabBtn, idTabBtn].forEach(tab => {
      if (tab) tab.style.display = isReadOnly ? 'none' : 'block';
    });

    if (detailsTabBtn) {
      detailsTabBtn.style.display = isReadOnly ? 'none' : 'block';
    }

    [nextToVerifyBtn, nextToFacialBtn, nextToVehicleBtn].forEach(btn => {
      if (btn) btn.style.display = isReadOnly ? 'none' : 'inline-block';
    });

    // Conditionally hide/show the Details tab content and container
    const detailsTabContent = document.getElementById('details');
    const visitorTabContent = document.getElementById('visitorTabContent');
    if (detailsTabContent) {
      detailsTabContent.style.display = isReadOnly ? 'none' : 'block';
    }
    if (visitorTabContent) {
      visitorTabContent.style.display = isReadOnly ? 'none' : 'block';
    }

    const detailsTabTriggerEl = document.querySelector('#details-tab');
    if (detailsTabTriggerEl) {
      const tab = bootstrap.Tab.getInstance(detailsTabTriggerEl) || new bootstrap.Tab(detailsTabTriggerEl);
      tab.show();
    }

    // --- New Sequential Flow Logic ---
    // 1. Disable tabs that should not be accessed yet
    document.querySelector('#visitorTab button[data-bs-target="#vehicle"]').disabled = true;
    document.querySelector('#visitorTab button[data-bs-target="#id"]').disabled = true;

    // 2. Ensure the "Next" button on the facial tab is disabled initially
    const nextToVehicleBtnElement = document.getElementById("nextToVehicle"); // Renamed to avoid conflict
    if (nextToVehicleBtnElement) {
        nextToVehicleBtnElement.disabled = true;
    }
    // --- End New Logic ---

    new bootstrap.Modal(document.getElementById("visitorDetailsModal")).show();

    // Ensure visitor details section is shown initially
    const visitorDetailsSection = document.getElementById('visitorDetailsSection');
    if (visitorDetailsSection) visitorDetailsSection.style.display = 'block';
  }

  async function markEntry(visitorId) {
    try {
      const res = await fetch("mark_entry_visitor.php", {
        method: "POST",
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        body: `visitor_id=${encodeURIComponent(visitorId)}`
      });
      const data = await res.json();
      if (data.success) {
        alert("Visitor marked as inside.");
        await loadExpectedVisitors();
        await loadInsideVisitors();
      } else alert(data.message || "Failed to mark entry.");
    } catch (err) {
      console.error(err);
      alert("Error while marking entry.");
    }
  }

  async function markExit(visitorId) {
    try {
      const res = await fetch("mark_exit_visitor.php", {
        method: "POST",
        headers: { "Content-Type": "application/x-www-form-urlencoded" },
        body: `visitor_id=${encodeURIComponent(visitorId)}`
      });
      const data = await res.json();
      if (data.success) {
        alert("Visitor marked as exited.");
        await loadInsideVisitors();
        await loadExitedVisitors();
      } else alert(data.message || "Failed to mark exit.");
    } catch (err) {
      console.error(err);
      alert("Error while marking exit.");
    }
  }

  // ----- Load Tables -----
  async function loadTable(url, tbody, columns) {
    try {
      const res = await fetch(url);
      const data = await res.json();

      tbody.innerHTML = "";
      if (!Array.isArray(data) || data.length === 0) {
        tbody.innerHTML = `<tr><td colspan="${columns}" class="text-center">No records found</td></tr>`;
        return;
      }

      data.forEach(v => {
        const tr = document.createElement("tr");
        tr.innerHTML = `
          <td>${escapeHtml(v.first_name || "")}</td>
          <td>${escapeHtml(v.middle_name || "")}</td>
          <td>${escapeHtml(v.last_name || "")}</td>
          <td>${escapeHtml(v.contact_number || "")}</td>
          ${v.date !== undefined ? `<td>${escapeHtml(v.date || "")}</td>` : ""}
          ${v.key_card_number !== undefined ? `<td>${escapeHtml(v.key_card_number || "")}</td>` : ""}
          ${v.time_in !== undefined ? `<td>${escapeHtml(v.time_in || "")}</td>` : ""}
          ${v.time_out !== undefined ? `<td>${escapeHtml(v.time_out || "")}</td>` : ""}
          <td>${escapeHtml(v.status)}</td>
          <td>
            <button class="btn btn-info btn-sm view-btn" data-id="${v.id}">View</button>
            ${v.time_out == null && v.time_in != null ? `<button class="btn btn-danger btn-sm exit-btn" data-id="${v.id}">Mark Exit</button>` : ""}
          </td>
        `;
        tbody.appendChild(tr);
      });
    } catch (err) {
      console.error(`Error loading table: ${url}`, err);
      tbody.innerHTML = `<tr><td colspan="${columns}" class="text-center text-danger">Failed to load data</td></tr>`;
    }
  }

  const loadExpectedVisitors = () => loadTable("fetch_expected_visitors.php", expectedVisitorsTbody, 7);
  const loadInsideVisitors = () => loadTable("fetch_inside_visitors.php", insideVisitorsTbody, 9);
  const loadExitedVisitors = () => loadTable("fetch_exited_visitors.php", exitedVisitorsTbody, 9);

  // ----- Event Listeners -----
  [nextToVerifyBtn, nextToFacialBtn, nextToVehicleBtn, nextToIdBtn, skipVehicleBtn].forEach(btn => {
    if (!btn) return;
    btn.addEventListener("click", () => showTab(btn.dataset.targetTab || btn.id.replace("nextTo", "").toLowerCase()));
  });

  // Handle tab changes to show/hide visitor details section and manage camera
  document.getElementById('visitorTab').addEventListener('shown.bs.tab', function (event) {
    const target = event.target.getAttribute('data-bs-target');
    const visitorDetailsSection = document.getElementById('visitorDetailsSection');
    if (visitorDetailsSection) {
      visitorDetailsSection.style.display = (target === '#details') ? 'block' : 'none';
    }

    // Stop all camera feeds when switching tabs
    stopCamera();
    // Also reset src to stop the browser from streaming in the background
    // const facialCamera = document.getElementById("facialCamera"); // This element doesn't exist
    // const vehicleCamera = document.getElementById("cameraFeed"); // This is already defined globally
    // if (facialCamera) facialCamera.src = "";
    if (cameraFeed) cameraFeed.src = "";

    // Start the correct camera feed for the active tab
    if (target === '#facial') {
      // if (facialCamera) facialCamera.src = `${API_BASE_URL}/camera/facial/frame`; // This element doesn't exist
      const selectedSource = cameraSourceSelect.value;
      if (selectedSource === 'webcam') {
        startWebcam();
      } else if (selectedSource === 'cctv') {
        startCCTVFeed();
      }
    } else if (target === '#vehicle') {
      // --- New: Conditional Vehicle Logic ---
      const expectedPlate = expectedPlateNumberDisplay.textContent.trim();
      const vehicleRecognitionContainer = document.getElementById("vehicleRecognitionContainer"); // Corrected ID
      // const skipVehicleBtn = document.getElementById("skipVehicle"); // Already defined globally
      // const nextToIdBtn = document.getElementById("nextToId"); // Already defined globally

      document.querySelector('#visitorTab button[data-bs-target="#id"]').disabled = false; // Unlock ID tab

      if (!expectedPlate || expectedPlate === "N/A") {
        // No vehicle, show skip button and hide verification UI
        if(vehicleRecognitionContainer) vehicleRecognitionContainer.style.display = 'none';
        if(skipVehicleBtn) skipVehicleBtn.style.display = 'inline-block';
        if(nextToIdBtn) nextToIdBtn.style.display = 'none'; // Hide regular next button
        // Automatically move to the next tab for a smoother experience
        showTab('id'); 
      } else {
        // Has a vehicle, show verification UI
        if(vehicleRecognitionContainer) vehicleRecognitionContainer.style.display = 'block';
        if(skipVehicleBtn) skipVehicleBtn.style.display = 'none';
        if(nextToIdBtn) nextToIdBtn.style.display = 'inline-block';
        if (cameraFeed) cameraFeed.src = `${API_BASE_URL}/camera/vehicle/frame`;
      }
      // --- End New Logic ---
    }

    // If ID tab is shown, run OCR on the ID image
    if (target === '#id' && idTabImage.src) {
      runOCR(idTabImage.src);
    }
  });

  // Function to capture a frame from the active video source
  async function captureFrame() {
    let videoElement = null;
    let isCCTV = false;

    if (cameraSourceSelect.value === 'webcam' && authVideoFeed.style.display !== 'none') {
      videoElement = authVideoFeed;
    } else if (cameraSourceSelect.value === 'cctv' && cctvFeed.style.display !== 'none') {
      // For CCTV, we need to fetch a single frame from the backend
      isCCTV = true;
    }

    if (isCCTV) {
      const response = await fetch(`${API_BASE_URL}/camera/facial/single_frame`);
      if (!response.ok) throw new Error("Failed to capture frame from CCTV.");
      return await response.blob();
    } else if (videoElement) {
      const canvas = document.createElement('canvas');
      canvas.width = videoElement.videoWidth;
      canvas.height = videoElement.videoHeight;
      const context = canvas.getContext('2d');
      context.drawImage(videoElement, 0, 0, canvas.width, canvas.height);
      return new Promise(resolve => canvas.toBlob(resolve, 'image/jpeg'));
    } else {
      throw new Error("No active camera feed to capture from.");
    }
  }

  // Event listener for the Authenticate button
  authenticateBtn?.addEventListener('click', async () => {
    authenticateBtn.disabled = true; // Disable button during processing
    authenticateBtn.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Authenticating...';
    authResultDiv.innerHTML = "<div class=\"alert alert-info\">Authenticating...</div>";
    try {
      const frameBlob = await captureFrame();
      const formData = new FormData();
      formData.append('file', frameBlob, 'frame.jpg');

      const response = await fetch(`${API_BASE_URL}/authenticate/face`, {
        method: 'POST',
        body: formData
      });
      const result = await response.json();

      if (response.ok && result.authenticated) {
        authResultDiv.innerHTML = `<div class="alert alert-success">Authenticated as: <strong>${escapeHtml(result.visitor_name)}</strong></div>`;
        
        // --- New: Enable next step on success ---
        const nextToVehicleBtnElement = document.getElementById("nextToVehicle"); // Renamed to avoid conflict
        if (nextToVehicleBtnElement) {
            nextToVehicleBtnElement.disabled = false;
        }
        document.querySelector('#visitorTab button[data-bs-target="#vehicle"]').disabled = false;
        // --- End New Logic ---

        // Optionally send a notification to the PHP backend
        await fetch('send_notification.php', {
          method: 'POST', 
          headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
          body: `message=${encodeURIComponent(`Visitor ${result.visitor_name} authenticated successfully.`)}`
        });
      } else {
        authResultDiv.innerHTML = `<div class="alert alert-warning">Authentication failed: ${escapeHtml(result.message || 'Unknown error')}</div>`;
        // Optionally send a notification for failed authentication
        await fetch('send_notification.php', {
          method: 'POST', 
          headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
          body: `message=${encodeURIComponent(`Failed authentication attempt.`)}`
        });
      }
    } catch (error) {
      console.error("Authentication error:", error);
      authResultDiv.innerHTML = `<div class="alert alert-danger">Error during authentication: ${escapeHtml(error.message)}</div>`;
    } finally {
      authenticateBtn.disabled = false; // Re-enable button
      authenticateBtn.innerHTML = 'Authenticate';
    }
  });

  markEntryBtn?.addEventListener("click", () => {
    if (currentVisitorId) markEntry(currentVisitorId);
  });

  saveTimeBtn?.addEventListener("click", () => {
    if (currentVisitorId) markExit(currentVisitorId);
  });

  // Delegate table buttons
  document.addEventListener("click", async e => {
    const id = e.target.dataset.id;
    if (!id) return;

    if (e.target.classList.contains("view-btn")) {
      const visitor = await fetchVisitorDetails(id);
      if (visitor) {
        showVisitorDetails(visitor);
        // Set expected plate number for vehicle tab
        expectedPlateNumberDisplay.textContent = visitor.plate_number || '';
        recognizedPlateDisplay.textContent = "N/A";
        verificationStatus.className = "text-muted";
        verificationStatus.textContent = "Awaiting scan...";
      }
    } else if (e.target.classList.contains("entry-btn")) {
      markEntry(id);
    } else if (e.target.classList.contains("exit-btn")) {
      markExit(id);
    }
  });

  logoutLink?.addEventListener("click", () => {
    if (confirm("Are you sure you want to log out?")) {
      window.location.href = "logout.php";
    }
  });



  // recognizeFaceBtn?.addEventListener("click", async () => { // This button doesn't exist in the current modal structure
  //   if (!currentSelfiePath) {
  //     facialResult.innerHTML = `<div class="alert alert-danger">No selfie path available.</div>`;
  //     return;
  //   }
  //   facialResult.innerHTML = "Processing...";
  //   try {
  //     // Fetch the captured frame
  //     const frameResponse = await fetch(`${API_BASE_URL}/camera/single_frame`);
  //     if (!frameResponse.ok) throw new Error("Failed to capture frame");
  //     const frameBlob = await frameResponse.blob();

  //     // Prepare form data
  //     const formData = new FormData();
  //     formData.append("file", frameBlob, "captured_frame.jpg");
  //     formData.append("selfie_path", currentSelfiePath);

  //     // Send to API
  //     const response = await fetch(`${API_BASE_URL}/real_time_compare/faces`, {
  //       method: "POST",
  //       body: formData
  //     });
  //     const data = await response.json();
  //     if (data.match) {
  //       facialResult.innerHTML = `<div class="alert alert-success">Faces match! Confidence: ${(data.boxes[0]?.confidence * 100 || 0).toFixed(2)}%</div>`;
  //     } else {
  //       facialResult.innerHTML = `<div class="alert alert-warning">Faces do not match.</div>`;
  //     }
  //   } catch (error) {
  //     facialResult.innerHTML = `<div class="alert alert-danger">Error: ${error.message}</div>`;
  //   }
  // });

  scanPlateBtn?.addEventListener("click", async () => {
    const expectedPlate = expectedPlateNumberDisplay.textContent.trim();
    const liveFeedImg = document.getElementById('cameraFeed');
    const recognizedPlateElem = document.getElementById('recognizedPlateDisplay');
    const recognizedVehicleTypeElem = document.getElementById('recognizedVehicleTypeDisplay');
    const verificationStatusElem = document.getElementById('verificationStatus');

    if (!liveFeedImg.src || liveFeedImg.src.endsWith('#')) {
        verificationStatusElem.textContent = "Live feed is not active.";
        verificationStatusElem.className = "text-warning";
        return;
    }

    scanPlateBtn.disabled = true;
    scanPlateBtn.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Scanning...';
    verificationStatusElem.textContent = "Capturing and scanning...";
    verificationStatusElem.className = "text-info";
    recognizedPlateElem.textContent = "N/A";
    recognizedVehicleTypeElem.textContent = "N/A";

    try {
        // Create a canvas to capture the image from the live feed
        const canvas = document.createElement('canvas');
        const context = canvas.getContext('2d');
        const img = new Image();
        img.crossOrigin = "Anonymous"; // Handle potential CORS issues if the feed is from a different origin

        img.onload = () => {
            canvas.width = img.width;
            canvas.height = img.height;
            context.drawImage(img, 0, 0);

            canvas.toBlob(blob => {
                if (!blob) {
                    throw new Error("Canvas to Blob conversion failed.");
                }
                const formData = new FormData();
                formData.append('image', blob, 'capture.jpg');

                // Send the captured image to the backend
                fetch('scan_plate.php', {
                    method: 'POST',
                    body: formData
                })
                .then(response => {
                    if (!response.ok) {
                        throw new Error(`Server error: ${response.statusText}`);
                    }
                    return response.json();
                })
                .then(data => {
                    if (data.error) {
                        throw new Error(data.error);
                    }

                    const recognizedPlate = data.license_plate_number || "Not Found";
                    const recognizedVehicleType = data.vehicle_type || "Not Found";

                    recognizedPlateElem.textContent = recognizedPlate;
                    recognizedVehicleTypeElem.textContent = recognizedVehicleType;

                    // Compare with expected plate
                    if (expectedPlate && recognizedPlate.toLowerCase() === expectedPlate.toLowerCase()) {
                        verificationStatusElem.textContent = "✅ Match!";
                        verificationStatusElem.className = "text-success";
                    } else {
                        verificationStatusElem.textContent = `❌ No Match: Found ${escapeHtml(recognizedPlate)}`;
                        verificationStatusElem.className = "text-danger";
                    }
                })
                .catch(handleScanError)
                .finally(() => {
                    scanPlateBtn.disabled = false;
                    scanPlateBtn.innerHTML = 'Scan Plate';
                });
            }, 'image/jpeg');
        };
        
        img.onerror = () => {
            throw new Error("Failed to load image from the live feed.");
        };

        // Add a cache-busting query parameter to get the latest frame
        liveFeedImg.src = liveFeedImg.src.split('?')[0] + '?' + new Date().getTime();
        img.src = liveFeedImg.src;
    } catch (error) {
        handleScanError(error);
        scanPlateBtn.disabled = false;
        scanPlateBtn.innerHTML = 'Scan Plate';
    }

    function handleScanError(error) {
        console.error("Error during plate recognition:", error);
        verificationStatusElem.textContent = `Error: ${escapeHtml(error.message)}`;
        verificationStatusElem.className = "text-danger";
        recognizedPlateElem.textContent = "Error";
        recognizedVehicleTypeElem.textContent = "Error";
    }
  });

  // Function to convert image blob to PNG
  async function convertToPNG(blob) {
    return new Promise((resolve, reject) => {
      const img = new Image();
      img.onload = () => {
        const canvas = document.createElement('canvas');
        const ctx = canvas.getContext('2d');
        canvas.width = img.width;
        canvas.height = img.height;
        ctx.drawImage(img, 0, 0);
        canvas.toBlob(resolve, 'image/png');
      };
      img.onerror = reject;
      img.src = URL.createObjectURL(blob);
    });
  }

  // Function to run OCR on an image URL
  async function runOCR(imageUrl) {
    // Clear previous OCR content
    ocrContent.innerHTML = '<p class="text-muted">Processing image, please wait...</p>';

    try {
      // Fetch the image as blob
      const response = await fetch(imageUrl);
      if (!response.ok) {
        throw new Error(`Failed to fetch image: ${response.statusText}`);
      }
      const blob = await response.blob();

      // Convert to PNG
      const pngBlob = await convertToPNG(blob);

      // Prepare form data
      const formData = new FormData();
      formData.append("file", pngBlob, "id_image.png");

      const ocrResponse = await fetch(`${API_BASE_URL}/ocr/id`, {
        method: "POST",
        body: formData,
      });

      if (!ocrResponse.ok) {
        throw new Error(`Server error: ${ocrResponse.statusText}`);
      }

      const data = await ocrResponse.json();

      // Display extracted details
      if (data && Object.keys(data).length > 0) {
        let html = "<ul class='list-group'>";
        for (const [key, value] of Object.entries(data)) {
          html += `<li class="list-group-item"><strong>${key}:</strong> ${value || "<em>Not detected</em>"}</li>`;
        }
        html += "</ul>";
        ocrContent.innerHTML = html;
      } else {
        ocrContent.innerHTML = '<p class="text-muted">No details extracted.</p>';
      }
    } catch (error) {
      console.error("Error during OCR request:", error);
      ocrContent.innerHTML = `<p class="text-danger">Error processing image: ${error.message}</p>`;
    }
  }

  // ----- Initial Load -----
  loadExpectedVisitors();
  loadInsideVisitors();
  loadExitedVisitors();
});
