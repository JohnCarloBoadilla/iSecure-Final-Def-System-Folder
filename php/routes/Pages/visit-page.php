<?php
session_start();
require '../../database/db_connect.php';

function generateRandomToken($length = 64) {
    return bin2hex(random_bytes($length / 2));
}

$token = $_SESSION['user_token'] ?? null;

if (!$token) {
    $token = generateRandomToken(64);
    $_SESSION['user_token'] = $token;

    $expiry = date("Y-m-d H:i:s", strtotime("+45 minutes"));
    $stmt = $pdo->prepare("INSERT INTO visitor_sessions (user_token, created_at, expires_at) VALUES (?, CURRENT_TIMESTAMP(), ?)");
    $stmt->execute([$token, $expiry]);
}

?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="icon" type="image/png" href="/iSecure-Final-Def-System-Folder/images/logo/5thFighterWing-logo.png">
    <title>5th Fighter Wing</title>
    <link href="/iSecure-Final-Def-System-Folder/src/output.css" rel="stylesheet" >
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Oswald:wght@200..700&display=swap" rel="stylesheet">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/7.0.1/css/all.min.css">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/flatpickr/dist/flatpickr.min.css">

</head>

<body class="min-h-screen flex flex-col">
<header class="w-full bg-white border-b border-[#E4E4E4] relative z-50">
    <div class="flex flex-col sm:flex-row justify-between items-center px-6 sm:px-[119px] py-[27px]">
    <!-- Left Side: Logo + Title + Menu Button -->
    <div class="flex items-center justify-between w-full sm:w-auto">
      <!-- 5th Fighter Wing Logo -->
      <div class="flex items-center">
        <img src="/iSecure-Final-Def-System-Folder/images/logo/5thFighterWing-logo.png" alt="5th Fighter Wing Logo"
          class="w-[65px] h-[65px] object-contain mr-5 sm:mr-8" />
      </div>

      <!-- Title + Menu Button -->
      <div class="flex items-center space-x-6">
        <h1
        class="font-[Oswald] font-semibold text-[26px] sm:text-[37px] text-[#003673] whitespace-nowrap leading-none tracking-wide drop-shadow-[0_2px_4px_rgba(0,0,0,0.25)]">
        5TH FIGHTER WING
        </h1>

        <!-- Hamburger Button -->
        <button id="menu-btn" class="sm:hidden flex flex-col space-y-1.5 ml-3 focus:outline-none relative z-50">
          <span class="block w-6 h-0.5 bg-[#003673] transition-all duration-300"></span>
          <span class="block w-6 h-0.5 bg-[#003673] transition-all duration-300"></span>
          <span class="block w-6 h-0.5 bg-[#003673] transition-all duration-300"></span>
        </button>
      </div>
    </div>

    <!-- Right Logos (includes PAF) -->
    <div class="flex items-center space-x-3 mt-4 sm:mt-0">
      <img src="/iSecure-Final-Def-System-Folder/images/logo/PAF-logo.png" alt="PAF Logo" class="w-[65px] h-[65px] object-contain" />
      <img src="/iSecure-Final-Def-System-Folder/images/logo/TS-logo.png" alt="TS Logo" class="w-[65px] h-[65px] object-contain" />
      <img src="/iSecure-Final-Def-System-Folder/images/logo/BP-logo.png" alt="BP Logo" class="w-[65px] h-[65px] object-contain" />
    </div>
  </div>

  <!-- Desktop Navbar -->
  <nav class="hidden sm:flex justify-center items-center w-full h-[75px] bg-[#F8FAFC] border-y border-[#E4E4E4]">
    <ul class="flex space-x-[40px]">
      <li><a href="/iSecure-Final-Def-System-Folder/php/routes/Pages/home-page.php" class="text-[20px] text-[#5E7EA2] font-medium transition-all duration-200 hover:text-[#003673] hover:text-[23px]">HOME</a></li>
      <li><a href="/iSecure-Final-Def-System-Folder/php/routes/Pages/about-us-page.php" class="text-[20px] text-[#5E7EA2] font-medium transition-all duration-200 hover:text-[#003673] hover:text-[23px]">ABOUT US</a></li>
      <li><a href="/iSecure-Final-Def-System-Folder/php/routes/Pages/news-page.php" class="text-[20px] text-[#5E7EA2] font-medium transition-all duration-200 hover:text-[#003673] hover:text-[23px]">NEWS</a></li>
      <li><a href="/iSecure-Final-Def-System-Folder/php/routes/Pages/advisory-page.php" class="text-[20px] text-[#5E7EA2] font-medium transition-all duration-200 hover:text-[#003673] hover:text-[23px]">ADVISORY</a></li>
      <li><a href="/iSecure-Final-Def-System-Folder/php/routes/Pages/visit-page.php" class="text-[20px] text-[#5E7EA2] font-medium transition-all duration-200 hover:text-[#003673] hover:text-[23px]">VISIT US</a></li>
      <li><a href="/iSecure-Final-Def-System-Folder/php/routes/Pages/contact-page.php" class="text-[20px] text-[#5E7EA2] font-medium transition-all duration-200 hover:text-[#003673] hover:text-[23px]">CONTACT US</a></li>
    </ul>
  </nav>

  <!-- Mobile Navbar (Dropdown Modal Style) -->
  <nav
    id="mobile-menu"
    class="absolute top-full left-0 w-full bg-[#F8FAFC] border-y border-[#E4E4E4] hidden opacity-0 translate-y-[-10px] transition-all duration-300 ease-in-out"
  >
    <ul class="flex flex-col items-center py-5 space-y-5">
      <li><a href="/iSecure-Final-Def-System-Folder/php/routes/Pages/home-page.php" class="text-[18px] text-[#5E7EA2] font-medium hover:text-[#003673] transition">HOME</a></li>
      <li><a href="/iSecure-Final-Def-System-Folder/php/routes/Pages/about-us-page.php" class="text-[18px] text-[#5E7EA2] font-medium hover:text-[#003673] transition">ABOUT US</a></li>
      <li><a href="/iSecure-Final-Def-System-Folder/php/routes/Pages/news-page.php" class="text-[18px] text-[#5E7EA2] font-medium hover:text-[#003673] transition">NEWS</a></li>
      <li><a href="/iSecure-Final-Def-System-Folder/php/routes/Pages/advisory-page.php" class="text-[18px] text-[#5E7EA2] font-medium hover:text-[#003673] transition">ADVISORY</a></li>
      <li><a href="/iSecure-Final-Def-System-Folder/php/routes/Pages/visit-page.php" class="text-[18px] text-[#5E7EA2] font-medium hover:text-[#003673] transition">VISIT US</a></li>
      <li><a href="/iSecure-Final-Def-System-Folder/php/routes/Pages/contact-page.php" class="text-[18px] text-[#5E7EA2] font-medium hover:text-[#003673] transition">CONTACT US</a></li>
    </ul>
  </nav>
</header>

<main class="flex flex-col items-center justify-center px-4 py-12">
  <h1 class="text-[36px] sm:text-[45px] font-[Oswald] font-semibold text-[#003673] mb-12 sm:mr-[790px] sm:text-4xl">
    Schedule A Visit with Us
  </h1>

  <div class="bg-white w-full max-w-5xl p-8 rounded-xl shadow-[0_4px_25px_rgba(0,0,0,0.1)] border border-gray-200">
    <form class="space-y-8" action="../visitation_submit.php" method="POST" enctype="multipart/form-data">

      <!-- Header -->
      <div>
        <p class="text-sm text-gray-600 mb-4">
          Please complete all the required fields, information will be verified upon arrival.
        </p>
      </div>

      <!-- Personal Information -->
      <section>
        <h2 class="text-[#003673] font-semibold text-sm mb-3">Personal Information</h2>
        <div class="grid grid-cols-1 sm:grid-cols-3 gap-4">
          <div>
            <label class="block text-sm font-semibold mb-1">Last Name <span class="text-red-500">*</span></label>
            <input type="text" name="last_name" class="w-full border border-gray-300 rounded-md px-3 py-2 focus:ring-2 focus:ring-[#003673] focus:outline-none" required>
          </div>
          <div>
            <label class="block text-sm font-semibold mb-1">First Name <span class="text-red-500">*</span></label>
            <input type="text" name="first_name" class="w-full border border-gray-300 rounded-md px-3 py-2 focus:ring-2 focus:ring-[#003673] focus:outline-none" required>
          </div>
          <div>
            <label class="block text-sm font-semibold mb-1">Middle Name <span class="text-red-500">*</span></label>
            <input type="text" name="middle_name" class="w-full border border-gray-300 rounded-md px-3 py-2 focus:ring-2 focus:ring-[#003673] focus:outline-none">
          </div>
        </div>

        <div class="grid grid-cols-2 gap-4 mt-4">
  <!-- Valid ID Upload -->
  <div class="w-full">
    <label class="block text-sm font-semibold mb-1">
      Valid ID Image <span class="text-red-500">*</span>
    </label>
    <label
      for="valid-id"
      class="flex items-center justify-center w-full border border-gray-300 rounded-md py-3 cursor-pointer hover:border-[#003673] transition text-gray-700 font-medium"
    >
      <i class="fa-regular fa-id-card mr-2 text-gray-600"></i>
      <span>Upload Valid ID</span>
    </label>
    <input id="valid-id" name="valid_id" type="file" class="hidden" required />
  </div>

  <!-- Facial Scanning -->
  <div class="w-full">
    <label class="block text-sm font-semibold mb-1">
      Facial Scanning <span class="text-red-500">*</span>
    </label>
    <button
      type="button"
      id="facial-scan-btn"
      class="flex items-center justify-center w-full border border-gray-300 rounded-md py-3 cursor-pointer hover:border-[#003673] transition text-gray-700 font-medium bg-white"
    >
      <i class="fa-solid fa-camera mr-2 text-gray-600"></i>
      <span>Start Facial Scan</span>
    </button>
    <input id="facial-photos" name="facial_photos" type="hidden" />
  </div>
</div>
      </section>

      <!-- Contact Information -->
      <section>
        <h2 class="text-[#003673] font-semibold text-sm mb-3">Contact Information</h2>
        <div class="mb-4">
          <label class="block text-sm font-semibold mb-1">Home Address <span class="text-red-500">*</span></label>
          <input type="text" name="home_address" class="w-full border border-gray-300 rounded-md px-3 py-2 focus:ring-2 focus:ring-[#003673] focus:outline-none" required>
        </div>
        <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
          <div>
            <label class="block text-sm font-semibold mb-1">Contact Number <span class="text-red-500">*</span></label>
            <input type="tel" name="contact_number" class="w-full border border-gray-300 rounded-md px-3 py-2 focus:ring-2 focus:ring-[#003673] focus:outline-none" required>
          </div>
          <div>
            <label class="block text-sm font-semibold mb-1">Email</label>
            <input type="email" name="email" class="w-full border border-gray-300 rounded-md px-3 py-2 focus:ring-2 focus:ring-[#003673] focus:outline-none">
          </div>
        </div>
      </section>

      <!-- Vehicle Information -->
      <section>
        <h2 class="text-[#003673] font-semibold text-sm mb-3">Vehicle Information</h2>
        <div class="mb-4">
          <p class="text-sm font-semibold mb-1">Will you bring a vehicle? <span class="text-red-500">*</span></p>
          <div class="flex space-x-6 text-sm">
            <label class="flex items-center space-x-2">
            <input type="radio" name="has_vehicle" value="yes" class="text-[#003673]" required>
              <span>Yes</span>
            </label>
            <label class="flex items-center space-x-2">
              <input type="radio" name="has_vehicle" value="no" class="text-[#003673]" required>
              <span>No</span>
            </label>
          </div>
        </div>

        <div id="vehicle-fields" class="hidden">
          <div class="grid grid-cols-1 sm:grid-cols-3 gap-4">
            <div>
              <label class="block text-sm font-semibold mb-1">Vehicle Brand</label>
              <input type="text" name="vehicle_brand" class="w-full border border-gray-300 rounded-md px-3 py-2 focus:ring-2 focus:ring-[#003673] focus:outline-none">
            </div>
            <div>
              <label class="block text-sm font-semibold mb-1">Vehicle Type</label>
              <input type="text" name="vehicle_type" class="w-full border border-gray-300 rounded-md px-3 py-2 focus:ring-2 focus:ring-[#003673] focus:outline-none">
            </div>
            <div>
              <label class="block text-sm font-semibold mb-1">Vehicle Color</label>
              <input type="text" name="vehicle_color" class="w-full border border-gray-300 rounded-md px-3 py-2 focus:ring-2 focus:ring-[#003673] focus:outline-none">
            </div>
          </div>

          <div class="mt-4">
            <label class="block text-sm font-semibold mb-1">License Plate Number</label>
            <input type="text" name="license_plate" class="w-full border border-gray-300 rounded-md px-3 py-2 focus:ring-2 focus:ring-[#003673] focus:outline-none">
          </div>
        </div>
      </section>

      <!-- Visit Details -->
      <section>
        <h2 class="text-[#003673] font-semibold text-sm mb-3">Visit Details</h2>
        <div class="mb-4">
          <label class="block text-sm font-semibold mb-1">Name of the Contact Personnel <span class="text-red-500">*</span></label>
          <input type="text" name="contact_personnel" class="w-full border border-gray-300 rounded-md px-3 py-2 focus:ring-2 focus:ring-[#003673] focus:outline-none" required>
          <p class="text-xs text-gray-500 mt-1">Write the name of the Personnel that you will meet prior to the Visit.</p>
        </div>

        <div class="mb-4">
          <label class="block text-sm font-semibold mb-1">Facility that will be Visited in the Base <span class="text-red-500">*</span></label>
          <select name="office_to_visit" class="w-full border border-gray-300 rounded-md px-3 py-2 focus:ring-2 focus:ring-[#003673] focus:outline-none" required>
            <option value="" disabled selected>Please select a facility</option>
            <option value="ICT Facility">ICT Facility</option>
            <option value="Training Facility">Training Facility</option>
            <option value="Personnels Office">Personnels Office</option>
          </select>
        </div>

        <div class="mb-4">
          <label class="block text-sm font-semibold mb-1">Visit Date <span class="text-red-500">*</span></label>
          <input type="text" id="visit-date" name="visit_date" class="w-full border border-gray-300 rounded-md px-3 py-2 focus:ring-2 focus:ring-[#003673] focus:outline-none" placeholder="Select a date" required>
          <p class="text-xs text-gray-500 mt-1">
            Below are the list of dates highligted in green that are available for a scheduled visitation.
          </p>
        </div>

        <div class="mb-4">
          <label class="block text-sm font-semibold mb-1">Visit Time <span class="text-red-500">*</span></label>
          <input type="text" id="visit-time" name="visit_time" class="w-full border border-gray-300 rounded-md px-3 py-2 focus:ring-2 focus:ring-[#003673] focus:outline-none" placeholder="Select a time" required>
          <p class="text-xs text-gray-500 mt-1">
            The only available time for visitation is from 7:00 AM to 7:00 PM.
          </p>
        </div>
      </section>

      <!-- Submit Button -->
      <button type="submit" class="w-full bg-[#003673] text-white font-semibold py-3 rounded-md hover:bg-[#002a59] transition">
        Submit Visitation Request
      </button>

      <p class="text-[12px] text-gray-500 leading-relaxed mt-4 text-center">
        By submitting this form, you agree to comply with all security protocols and regulations of the 5th Fighter Wing Base.<br>
        *Upon submission, the request will be properly evaluated. Once approved you will be notified through email.<br>
        *If you have a scheduled visit and will not be able to attend please submit a cancellation request in the contact us page prior to the scheduled date of visitation.
      </p>
    </form>
  </div>
</main>


<footer class="bg-[#003366] text-white h-[395px] flex items-center border-t border-white/10 mt-auto">
  <div class="container bg-[#003366] mx-auto px-[75px] flex flex-col md:flex-row items-center md:items-center justify-between text-center md:text-left gap-10 w-full p-[20px]">
    
    <!-- Left Section -->
    <div class="flex flex-col items-center md:items-start space-y-3">
      <div class="flex space-x-3">
        <img src="/iSecure-Final-Def-System-Folder/images/logo/5thFighterWing-logo.png" alt="Logo 1" class="h-[70px] w-auto">
        <img src="/iSecure-Final-Def-System-Folder/images/logo/BP-logo.png" alt="Logo 2" class="h-[70px] w-auto">
        <img src="/iSecure-Final-Def-System-Folder/images/logo/PAF-logo.png" alt="Logo 3" class="h-[70px] w-auto">
      </div>
      <p class="text-sm leading-tight mt-2">
        Copyright © Basa Air Base 5th Fighter Wing.<br>
        All Rights Reserved
      </p>
    </div>

    <!-- Center Section -->
    <div class="flex flex-col items-center space-y-3">
      <p class="text-base font-medium">Follow our Socials:</p>
      <div class="flex space-x-5 text-[30px]">
        <a href="#" class="hover:text-gray-300"><i class="fab fa-facebook"></i></a>
        <a href="#" class="hover:text-gray-300"><i class="fab fa-instagram"></i></a>
        <a href="#" class="hover:text-gray-300"><i class="fab fa-x-twitter"></i></a>
        <a href="#" class="hover:text-gray-300"><i class="fab fa-youtube"></i></a>
      </div>
    </div>

    <!-- Right Section -->
    <div class="flex flex-col items-center md:items-end space-y-3">
      <p class="text-base font-medium">DEVELOPED BY:</p>
      <div class="flex items-center space-x-3">
        <img src="/iSecure-Final-Def-System-Folder/images/logo/PAMSU-logo.png" alt="PSU Logo 1" class="h-[70px] w-auto">
        <img src="/iSecure-Final-Def-System-Folder/images/logo/CCS-logo.png" alt="PSU Logo 2" class="h-[70px] w-auto">
      </div>
      <p class="text-sm leading-tight text-center md:text-right">
        CCS Students of<br>Pampanga State University
      </p>
    </div>

  </div>
</footer>



<!-- Facial Scanning Modal -->
<div id="facial-scan-modal" class="fixed inset-0 bg-black bg-opacity-50 hidden z-50">
  <div class="flex items-center justify-center min-h-screen p-4">
    <div class="bg-white rounded-lg shadow-xl max-w-4xl w-full max-h-[90vh] overflow-hidden">
      <div class="flex justify-between items-center p-6 border-b">
        <h3 class="text-xl font-semibold text-[#003673]">Facial Scanning</h3>
        <button id="close-facial-modal" class="text-gray-500 hover:text-gray-700">
          <i class="fas fa-times text-2xl"></i>
        </button>
      </div>
      <div class="p-6">
        <!-- Facial scanning content will be inserted here -->
        <div id="facial-scan-content" class="text-center">
          <p class="text-gray-600 mb-4">Facial scanning interface will be loaded here.</p>
          <p class="text-sm text-gray-500">Please insert your Python facial scanning program in this modal.</p>
        </div>
      </div>
      <div class="flex justify-end space-x-3 p-6 border-t">
        <button id="cancel-facial-scan" class="px-4 py-2 bg-gray-300 text-gray-700 rounded-md hover:bg-gray-400 transition">
          Cancel
        </button>
        <button id="complete-facial-scan" class="px-4 py-2 bg-[#003673] text-white rounded-md hover:bg-[#002a59] transition">
          Complete Scan
        </button>
      </div>
    </div>
  </div>
</div>

</body>
<!-- <script src="https://cdn.tailwindcss.com"></script> -->
<script src="https://cdn.jsdelivr.net/npm/flatpickr"></script>
<script src="/iSecure-Final-Def-System-Folder/scripts/landingpage.js"></script>
</html>
