<?php
require '../database/db_connect.php';

define('ENC_KEY', 'your-32-character-secret-key');

/**
 * Try to decrypt if data is encrypted, otherwise return as-is.
 */
function tryDecrypt($data) {
    if (!$data) return '';

    // If not valid base64, assume plain text
    $decoded = base64_decode($data, true);
    if ($decoded === false) {
        return $data; // not base64 → plain text
    }

    // Must have at least 17 bytes (16 IV + ciphertext)
    if (strlen($decoded) <= 16) {
        return $data; // too short → plain text
    }

    $iv = substr($decoded, 0, 16);
    $cipher = substr($decoded, 16);

    $decrypted = openssl_decrypt($cipher, 'AES-256-CBC', ENC_KEY, OPENSSL_RAW_DATA, $iv);
    return $decrypted !== false ? $decrypted : $data;
}

try {
    $stmt = $pdo->query("SELECT * FROM users ORDER BY joined_date DESC");
    $rows = $stmt->fetchAll(PDO::FETCH_ASSOC);

    $users = [];
    foreach ($rows as $r) {
        $users[] = [
            "id"          => $r["id"],
            "full_name"   => tryDecrypt($r["full_name"]),
            "email"       => tryDecrypt($r["email"]),
            "rank"        => tryDecrypt($r["rank"]),
            "status"      => tryDecrypt($r["status"]),
            "role"        => tryDecrypt($r["role"]),
            "joined_date" => $r["joined_date"],
            "last_active" => $r["last_active"]
        ];
    }

    header('Content-Type: application/json');
    echo json_encode($users);
} catch (Exception $e) {
    http_response_code(500);
    echo json_encode(["error" => $e->getMessage()]);
}