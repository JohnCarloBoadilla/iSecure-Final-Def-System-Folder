<?php
require '../database/db_connect.php';
require '../config/encryption_key.php';
header('Content-Type: application/json');

// Note: visitors table stores data encrypted, decryption needed for display

try {
    $stmt = $pdo->prepare("
        SELECT
            id,
            first_name,
            middle_name,
            last_name,
            contact_number,
            key_card_number,
            time_in,
            time_out,
            status
        FROM visitors
        WHERE time_in IS NOT NULL AND time_out IS NOT NULL AND status != 'Cancelled'
        ORDER BY time_out DESC
    ");
    $stmt->execute();
    $visitors = $stmt->fetchAll(PDO::FETCH_ASSOC);

    // Decrypt sensitive data for display
    foreach ($visitors as &$visitor) {
        $visitor['first_name'] = Encryption::decrypt($visitor['first_name']);
        $visitor['middle_name'] = Encryption::decrypt($visitor['middle_name']);
        $visitor['last_name'] = Encryption::decrypt($visitor['last_name']);
        $visitor['contact_number'] = Encryption::decrypt($visitor['contact_number']);


    }

    echo json_encode($visitors);
} catch (Exception $e) {
    echo json_encode([]);
}
