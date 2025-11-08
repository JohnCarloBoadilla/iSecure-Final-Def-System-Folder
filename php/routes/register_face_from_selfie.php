<?php
header('Content-Type: application/json');
include '../database/db_connect.php';

// --- Configuration ---
$python_executable = realpath(__DIR__ . '/../../../.venv/Scripts/python.exe');
$python_script = realpath(__DIR__ . '/../../../app/services/face_recog/face_authenticator.py');

$response = ['success' => false, 'message' => 'An unknown error occurred.'];

// --- Input Validation ---
$input = json_decode(file_get_contents('php://input'), true);
$visitor_id = $input['visitor_id'] ?? null;

if (!$visitor_id) {
    $response['message'] = 'Missing visitor_id.';
    http_response_code(400);
    echo json_encode($response);
    exit;
}

// --- Database Query ---
try {
    $stmt = $conn->prepare("SELECT selfie_photo_path FROM visitors WHERE id = ?");
    $stmt->bind_param("i", $visitor_id);
    $stmt->execute();
    $result = $stmt->get_result();
    if ($row = $result->fetch_assoc()) {
        $relative_selfie_path = $row['selfie_photo_path'];
        $project_root = realpath(__DIR__ . '/../../..');
        $absolute_selfie_path = $project_root . '/' . $relative_selfie_path;

        if (!file_exists($absolute_selfie_path)) {
            throw new Exception("Selfie file not found at path: " . $absolute_selfie_path);
        }

        // --- Python Script Execution ---
        $command = sprintf(
            '%s %s register --id %s --image %s',
            escapeshellarg($python_executable),
            escapeshellarg($python_script),
            escapeshellarg($visitor_id),
            escapeshellarg($absolute_selfie_path)
        );

        $output = shell_exec($command . ' 2>&1');
        $python_response = json_decode(trim($output), true);

        if (json_last_error() === JSON_ERROR_NONE && isset($python_response['success'])) {
            $response = $python_response;
            if (!$response['success']) http_response_code(400);
        } else {
            throw new Exception("Failed to execute Python script. Output: " . $output);
        }
    } else {
        throw new Exception("Visitor not found.");
    }
} catch (Exception $e) {
    $response['message'] = $e->getMessage();
    http_response_code(500);
}

echo json_encode($response);
