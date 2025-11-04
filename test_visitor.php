<?php
require 'database/db_connect.php';
require 'utils/encryption.php';
try {
    $stmt = $pdo->prepare("INSERT INTO visitors (first_name, middle_name, last_name, contact_number, email, address, reason, id_photo_path, selfie_photo_path, date, time_in, time_out, status, personnel_related, office_to_visit) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, CURDATE(), NULL, NULL, 'Expected', ?, ?)");
    $stmt->execute([
        Encryption::encrypt('John'),
        Encryption::encrypt('Doe'),
        Encryption::encrypt('Smith'),
        Encryption::encrypt('1234567890'),
        Encryption::encrypt('john@example.com'),
        Encryption::encrypt('123 Main St'),
        'Meeting',
        'path/to/id.jpg',
        'path/to/selfie.jpg',
        'Personnel',
        'Office'
    ]);
    $visitorId = $pdo->lastInsertId();
    echo 'Test visitor inserted with ID: ' . $visitorId;
} catch (Exception $e) {
    echo 'Error: ' . $e->getMessage();
}
