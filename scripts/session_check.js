const evtSource = new EventSource("session_watch.php");

evtSource.addEventListener("logout", function(e) {
  alert("⚠️ Your session was terminated please login again.");
  window.location.href = "loginpage.php";
});
