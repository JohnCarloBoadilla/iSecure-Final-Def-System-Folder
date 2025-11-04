<?php
require 'php/database/db_connect.php';

// Add facial_photos column to visitation_requests table
try {
    $sql = "ALTER TABLE visitation_requests ADD COLUMN facial_photos TEXT DEFAULT NULL AFTER valid_id_path";
    $pdo->exec($sql);
    echo "Column 'facial_photos' added successfully to visitation_requests table.\n";
} catch (PDOException $e) {
    if ($e->getCode() == '42S21') {
        echo "Column 'facial_photos' already exists in visitation_requests table.\n";
    } else {
        echo "Error adding column: " . $e->getMessage() . "\n";
    }
}

// Add facial_photos column to visitors table
try {
    $sql = "ALTER TABLE visitors ADD COLUMN facial_photos TEXT DEFAULT NULL AFTER selfie_photo_path";
    $pdo->exec($sql);
    echo "Column 'facial_photos' added successfully to visitors table.\n";
} catch (PDOException $e) {
    if ($e->getCode() == '42S21') {
        echo "Column 'facial_photos' already exists in visitors table.\n";
    } else {
        echo "Error adding column: " . $e->getMessage() . "\n";
    }
}

echo "Database alteration completed.\n";
?>
