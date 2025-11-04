<?php
require '../database/db_connect.php';

define('ENC_KEY', 'MPLC7l9UHbSCjgWOg19TtBj4VPz2leQb');

function encryptData($data) {
    $iv = random_bytes(16);
    $cipher = openssl_encrypt($data, 'AES-256-CBC', ENC_KEY, OPENSSL_RAW_DATA, $iv);
    return base64_encode($iv . $cipher);
}

$data = $_POST; 

if (!$data || empty($data['full_name']) || empty($data['email']) || empty($data['password'])) {
    echo json_encode(["success" => false, "message" => "Missing required fields"]);
    exit;
}

try {
    $stmt = $pdo->prepare("
        INSERT INTO users (id, full_name, email, rank, status, password_hash, role, joined_date, last_active)
        VALUES (UUID(), :full_name, :email, :rank, :status, :role, :password_hash, NOW(), NOW())
    ");
    $stmt->execute([
        ":full_name"     => encryptData($data['full_name']),
        ":email"         => encryptData($data['email']),
        ":rank"          => encryptData($data['rank']),
        ":status"        => encryptData($data['status']),
        ":password_hash" => password_hash($data['password'], PASSWORD_DEFAULT),
        ":role"          => encryptData($data['role']),
        
    ]);

    echo json_encode(["success" => true, "message" => "User added successfully"]);
} catch (Exception $e) {
    echo json_encode(["success" => false, "message" => "DB error: " . $e->getMessage()]);
}
