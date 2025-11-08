# Facial Scanning Fixes TODO

## 1. Fix JS Conflict in landingpage.js
- [ ] Add null checks for facial scanning elements (`facial-photos`, `facial-scan-btn`, etc.) to prevent TypeError on pages without them

## 2. Investigate Flask App Status
- [ ] Check if Flask app is running on localhost:8000
- [ ] Test `/register/face` endpoint manually
- [ ] Verify database connection in Flask app

## 3. Verify Database Setup
- [ ] Ensure `visitor_sessions` table exists and has correct structure
- [ ] Check database connection from PHP side

## 4. Test Facial Scanning Functionality
- [ ] Test facial scanning on visit-page.php after fixes
- [ ] Verify photo upload and database storage
- [ ] Confirm submit button enables after scan completion
