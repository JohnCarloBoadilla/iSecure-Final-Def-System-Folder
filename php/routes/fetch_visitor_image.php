<?php
require '../database/db_connect.php';

if (!isset($_GET['visitor_id'])) {
    http_response_code(400);
    echo json_encode(['error' => 'Missing visitor_id parameter']);
    exit;
}

$visitor_id = intval($_GET['visitor_id']);
$type = $_GET['type'] ?? 'id'; // Default to 'id', can be 'selfie'

if ($type === 'selfie') {
    $stmt = $pdo->prepare("SELECT selfie_photo_path FROM visitors WHERE id = ?");
} else {
    $stmt = $pdo->prepare("SELECT id_photo_path FROM visitors WHERE id = ?");
}
$stmt->execute([$visitor_id]);
$visitor = $stmt->fetch();

if (!$visitor) {
    http_response_code(404);
    echo json_encode(['error' => 'Visitor not found']);
    exit;
}

$photo_path = $type === 'selfie' ? $visitor['selfie_photo_path'] : $visitor['id_photo_path'];
$photo_path = $photo_path ?: 'sample_id.png';

// Check if photo_path is base64 encoded image data
if (preg_match('/^data:image\/(\w+);base64,/', $photo_path, $matches)) {
    $data = substr($photo_path, strpos($photo_path, ',') + 1);
    $data = base64_decode($data);
    if ($data === false) {
        http_response_code(500);
        echo json_encode(['error' => 'Base64 decode failed']);
        exit;
    }
    $mime_type = 'image/' . $matches[1];
    header('Content-Type: ' . $mime_type);
    echo $data;
    exit;
}

// Extract filename from path if it contains directory prefixes
$filename = basename($photo_path);

// Otherwise, treat as file path, try multiple locations
$possible_paths = [
    __DIR__ . '/../php/uploads/' . ($type === 'selfie' ? 'selfies/' : 'ids/') . $filename,
    __DIR__ . '/../public/uploads/' . ($type === 'selfie' ? 'selfies/' : 'ids/') . $filename,
    __DIR__ . '/uploads/' . ($type === 'selfie' ? 'selfies/' : 'ids/') . ltrim($photo_path, '/\\'),
    __DIR__ . '/../uploads/' . ($type === 'selfie' ? 'selfies/' : 'ids/') . ltrim($photo_path, '/\\'),
    __DIR__ . '/../app/services/ocr/' . ltrim($photo_path, '/\\'),
    __DIR__ . '/../public/' . ltrim($photo_path, '/\\'),
    __DIR__ . '/../public/uploads/' . ($type === 'selfie' ? 'selfies/' : 'ids/') . ltrim($photo_path, '/\\'),
    __DIR__ . '/../images/' . ltrim($photo_path, '/\\'),
    __DIR__ . '/../' . ltrim($photo_path, '/\\')
];

$file_path = null;
foreach ($possible_paths as $path) {
    if (file_exists($path)) {
        $file_path = $path;
        break;
    }
}

if (!$file_path) {
    http_response_code(404);
    echo json_encode(['error' => 'Image file not found in any expected location']);
    exit;
}

$mime_type = mime_content_type($file_path);
header('Content-Type: ' . $mime_type);
readfile($file_path);
exit;
?>
