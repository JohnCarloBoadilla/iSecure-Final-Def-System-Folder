<?php
header('Content-Type: application/json');

// --- Configuration ---
$python_executable = realpath(__DIR__ . '/../../../.venv/Scripts/python.exe');
$python_script = realpath(__DIR__ . '/../../../app/services/face_recog/face_authenticator.py');

$response = ['success' => false, 'message' => 'An unknown error occurred.'];

// --- Input Validation ---
if (!isset($_POST['visitor_id']) || !isset($_FILES['image'])) {
    $response['message'] = 'Missing visitor_id or image file.';
    http_response_code(400);
    echo json_encode($response);
    exit;
}

$visitor_id = $_POST['visitor_id'];
$image_file = $_FILES['image'];

// --- File Handling ---
if ($image_file['error'] !== UPLOAD_ERR_OK) {
    $response['message'] = 'File upload error: ' . $image_file['error'];
    http_response_code(400);
    echo json_encode($response);
    exit;
}

$tmp_dir = sys_get_temp_dir();
$tmp_file_path = tempnam($tmp_dir, 'face_auth_') . '.jpg';

if (!move_uploaded_file($image_file['tmp_name'], $tmp_file_path)) {
    $response['message'] = 'Failed to move uploaded file to temporary location.';
    http_response_code(500);
    echo json_encode($response);
    exit;
}

// --- Python Script Execution ---
if (!file_exists($python_executable)) {
    $response['message'] = 'Python executable not found at: ' . $python_executable;
    http_response_code(500);
} elseif (!file_exists($python_script)) {
    $response['message'] = 'Python script not found at: ' . $python_script;
    http_response_code(500);
} else {
    // Build the command for authentication
    $command = sprintf(
        '%s %s authenticate --id %s --image %s',
        escapeshellarg($python_executable),
        escapeshellarg($python_script),
        escapeshellarg($visitor_id), // Pass visitor_id even if not directly used by authenticate_visitor for consistency
        escapeshellarg($tmp_file_path)
    );

    $output = shell_exec($command . ' 2>&1');
    $python_response = json_decode(trim($output), true);

    if (json_last_error() === JSON_ERROR_NONE && isset($python_response['success'])) {
        $response = $python_response;
        if (!$response['success']) {
            http_response_code(401); // Unauthorized if authentication fails
        }
    } else {
        $response['message'] = 'Failed to execute Python script or parse its output.';
        $response['debug_output'] = $output;
        http_response_code(500);
    }
}

// --- Cleanup ---
if (file_exists($tmp_file_path)) {
    unlink($tmp_file_path);
}

echo json_encode($response);
