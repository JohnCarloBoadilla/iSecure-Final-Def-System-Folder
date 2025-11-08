<?php
require 'php/database/db_connect.php';
require 'php/config/encryption_key.php';

try {
    // Check visitors table
    echo "Visitors table data:\n";
    $stmt = $pdo->query('SELECT id, first_name, middle_name, last_name, contact_number, email, address, status FROM visitors LIMIT 5');
    $visitors = $stmt->fetchAll(PDO::FETCH_ASSOC);
    foreach ($visitors as $v) {
        echo 'ID: ' . $v['id'] . ', Name: ' . $v['first_name'] . ' ' . $v['middle_name'] . ' ' . $v['last_name'] . ', Status: ' . $v['status'] . "\n";
    }

    // Check visitation_requests
    echo "\nVisitation requests:\n";
    $stmt = $pdo->query('SELECT id, first_name, middle_name, last_name, status FROM visitation_requests LIMIT 5');
    $requests = $stmt->fetchAll(PDO::FETCH_ASSOC);
    foreach ($requests as $r) {
        echo 'ID: ' . $r['id'] . ', Name: ' . $r['first_name'] . ' ' . $r['middle_name'] . ' ' . $r['last_name'] . ', Status: ' . $r['status'] . "\n";
    }
} catch (Exception $e) {
    echo 'Error: ' . $e->getMessage();
}
