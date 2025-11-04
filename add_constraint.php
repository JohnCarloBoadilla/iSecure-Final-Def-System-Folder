<?php
require 'php/database/db_connect.php';
try {
    $pdo->exec('ALTER TABLE vehicles ADD UNIQUE KEY unique_visitation_id (visitation_id)');
    echo 'Unique constraint added successfully';
} catch (Exception $e) {
    echo 'Error: ' . $e->getMessage();
}
