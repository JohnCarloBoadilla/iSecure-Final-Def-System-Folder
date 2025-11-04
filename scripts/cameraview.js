document.addEventListener("DOMContentLoaded", () => {
  /* ---- Logout modal ---- */
  const logoutLink = document.getElementById("logout-link");
  if (logoutLink) {
    logoutLink.addEventListener("click", (ev) => {
      ev.preventDefault();
      const modal = document.getElementById("confirmModal");
      const msgEl = document.getElementById("confirmMessage");
      const yes = document.getElementById("confirmYes");
      const no = document.getElementById("confirmNo");

      msgEl.textContent = "Are you sure you want to log out?";
      modal.classList.add("show");

      yes.onclick = () => { window.location.href = logoutLink.href; };
      no.onclick = () => { modal.classList.remove("show"); };
    });
  }

  /* ---- Camera frames are now streaming via MJPEG ---- */

  function refreshCameraFeed(imgId, url) {
    const img = document.getElementById(imgId);
    if (!img) return;
    setInterval(() => {
      img.src = url + '?t=' + new Date().getTime();
    }, 150); // refresh every 150ms
  }

  refreshCameraFeed('face_recog', 'http://localhost:8000/camera/frame');
  refreshCameraFeed('vehicle_detect', 'http://localhost:8000/camera/frame');
  refreshCameraFeed('ocr_id', 'http://localhost:8000/camera/frame');
});
