<?php
require '../database/db_connect.php';

if (!isset($_GET['visitor_id'])) {
    http_response_code(400);
    echo json_encode(['error' => 'Missing visitor_id parameter']);
    exit;
}

$visitor_id = intval($_GET['visitor_id']);

$stmt = $pdo->prepare("SELECT id_photo_path FROM visitors WHERE id = ?");
$stmt->execute([$visitor_id]);
$visitor = $stmt->fetch();

if (!$visitor) {
    http_response_code(404);
    echo json_encode(['error' => 'Visitor not found']);
    exit;
}

$id_photo_path = $visitor['id_photo_path'] ?: 'sample_id.png';

// Check if id_photo_path is base64 encoded image data
if (preg_match('/^data:image\/(\w+);base64,/', $id_photo_path, $type)) {
    $data = substr($id_photo_path, strpos($id_photo_path, ',') + 1);
    $data = base64_decode($data);
    if ($data === false) {
        http_response_code(500);
        echo json_encode(['error' => 'Base64 decode failed']);
        exit;
    }
    $mime_type = 'image/' . $type[1];
    header('Content-Type: ' . $mime_type);
    echo $data;
    exit;
}

// Otherwise, treat as file path, try multiple locations
$possible_paths = [
    __DIR__ . '/../uploads/' . ltrim($id_photo_path, '/\\'),
    __DIR__ . '/../app/services/ocr/' . ltrim($id_photo_path, '/\\'),
    __DIR__ . '/../public/' . ltrim($id_photo_path, '/\\'),
    __DIR__ . '/../images/' . ltrim($id_photo_path, '/\\'),
    __DIR__ . '/../' . ltrim($id_photo_path, '/\\')
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
