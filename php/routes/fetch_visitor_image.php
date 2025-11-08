<?php
session_start();
include '../database/db_connect.php';

// Basic security check: ensure user is logged in
if (!isset($_SESSION['user_id'])) {
    http_response_code(403);
    echo "Access denied.";
    exit;
}

// Validate input
$visitor_id = filter_input(INPUT_GET, 'visitor_id', FILTER_VALIDATE_INT);
$type = filter_input(INPUT_GET, 'type', FILTER_SANITIZE_STRING);

if (!$visitor_id || !$type || !in_array($type, ['selfie', 'id'])) {
    http_response_code(400);
    echo "Invalid request.";
    exit;
}

// Determine which column to fetch
$column = ($type === 'selfie') ? 'selfie_photo_path' : 'id_photo_path';

try {
    $stmt = $conn->prepare("SELECT $column FROM visitors WHERE id = ?");
    $stmt->bind_param("i", $visitor_id);
    $stmt->execute();
    $result = $stmt->get_result();

    if ($row = $result->fetch_assoc()) {
        $file_path = $row[$column];
        
        // IMPORTANT: The path stored in the DB is relative to the project root.
        // We need to construct the full server file path.
        // realpath() resolves all symbolic links and '..' etc.
        $base_dir = realpath(__DIR__ . '/../../'); 
        $full_path = $base_dir . '/' . $file_path;

        if (file_exists($full_path)) {
            // Set the content type header and output the file
            $mime_type = mime_content_type($full_path);
            header("Content-Type: $mime_type");
            readfile($full_path);
            exit;
        } else {
            http_response_code(404);
            echo "File not found on server.";
        }
    } else {
        http_response_code(404);
        echo "Visitor record not found.";
    }
    $stmt->close();
} catch (Exception $e) {
    http_response_code(500);
    echo "Server error: " . $e->getMessage();
}

$conn->close();