<?php
require 'php/database/db_connect.php';
require 'php/config/encryption_key.php';

try {
    // Check visitation_requests
    echo "Visitation requests:\n";
    $stmt = $pdo->prepare('SELECT id, first_name, middle_name, last_name, status FROM visitation_requests LIMIT 10');
    $stmt->execute();
    $requests = $stmt->fetchAll(PDO::FETCH_ASSOC);
    foreach ($requests as $r) {
        $name = $r['first_name'] . ' ' . $r['middle_name'] . ' ' . $r['last_name'];
        echo 'ID: ' . $r['id'] . ', Name: ' . $name . ', Status: ' . $r['status'] . '\n';
    }

    // Check if there are approved requests
    echo "\nApproved requests:\n";
    $stmt = $pdo->prepare('SELECT id, first_name, middle_name, last_name, status FROM visitation_requests WHERE status = "Approved" LIMIT 10');
    $stmt->execute();
    $approved = $stmt->fetchAll(PDO::FETCH_ASSOC);
    foreach ($approved as $a) {
        $name = $a['first_name'] . ' ' . $a['middle_name'] . ' ' . $a['last_name'];
        echo 'ID: ' . $a['id'] . ', Name: ' . $name . ', Status: ' . $a['status'] . '\n';
    }
} catch (Exception $e) {
    echo 'Error: ' . $e->getMessage();
}
