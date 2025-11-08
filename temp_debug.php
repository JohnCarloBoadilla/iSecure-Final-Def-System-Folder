<?php
require 'php/database/db_connect.php';
$stmt = $pdo->query('SELECT id, id_photo_path, selfie_photo_path FROM visitors');
$visitors = $stmt->fetchAll(PDO::FETCH_ASSOC);
foreach ($visitors as $v) {
    echo 'ID: ' . $v['id'] . ', ID Photo: ' . $v['id_photo_path'] . ', Selfie: ' . $v['selfie_photo_path'] . PHP_EOL;
}
