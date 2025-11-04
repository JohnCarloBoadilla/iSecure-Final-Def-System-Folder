<?php
require 'php/database/db_connect.php';
try {
    // Find duplicate visitation_ids
    $stmt = $pdo->query("SELECT visitation_id, COUNT(*) as count FROM vehicles WHERE visitation_id IS NOT NULL GROUP BY visitation_id HAVING count > 1");
    $duplicates = $stmt->fetchAll(PDO::FETCH_ASSOC);

    foreach ($duplicates as $dup) {
        // Keep the first one, delete others
        $stmt = $pdo->prepare("DELETE FROM vehicles WHERE visitation_id = ? AND id NOT IN (SELECT MIN(id) FROM vehicles WHERE visitation_id = ?)");
        $stmt->execute([$dup['visitation_id'], $dup['visitation_id']]);
        echo "Cleaned duplicates for visitation_id: " . $dup['visitation_id'] . "\n";
    }

    // Now add the constraint
    $pdo->exec('ALTER TABLE vehicles ADD UNIQUE KEY unique_visitation_id (visitation_id)');
    echo 'Unique constraint added successfully';
} catch (Exception $e) {
    echo 'Error: ' . $e->getMessage();
}
