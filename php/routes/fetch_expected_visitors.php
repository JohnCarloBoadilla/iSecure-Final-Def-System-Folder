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
            date,
            status
        FROM visitors
        WHERE time_in IS NULL AND status != 'Cancelled'
        ORDER BY date DESC
    ");
    $stmt->execute();
    $visitors = $stmt->fetchAll(PDO::FETCH_ASSOC);

    // Decrypt sensitive data for display
    foreach ($visitors as &$visitor) {
        $visitor['first_name'];
        $visitor['middle_name'];
        $visitor['last_name'];
        $visitor['contact_number'];
        $visitor['status'] = 'Expected';

        // Construct full name for matching with vehicle_owner (encrypt for database query)
        $full_name = trim($visitor['first_name'] . ' ' . $visitor['middle_name'] . ' ' . $visitor['last_name']);
        $encrypted_full_name = $full_name;

        // Fetch associated vehicle if exists
        $vehicleStmt = $pdo->prepare("
            SELECT vehicle_brand, plate_number, vehicle_color, vehicle_model
            FROM vehicles
            WHERE vehicle_owner = :vehicle_owner AND status = 'Expected'
            LIMIT 1
        ");
        $vehicleStmt->execute([':vehicle_owner' => $encrypted_full_name]);
        $vehicle = $vehicleStmt->fetch(PDO::FETCH_ASSOC);

        if ($vehicle) {
            $visitor['vehicle_brand'] = $vehicle['vehicle_brand'];
            $visitor['plate_number'] = $vehicle['plate_number'];
            $visitor['vehicle_color'] = $vehicle['vehicle_color'];
            $visitor['vehicle_model'] = $vehicle['vehicle_model'];
        } else {
            $visitor['vehicle_brand'] = null;
            $visitor['plate_number'] = null;
            $visitor['vehicle_color'] = null;
            $visitor['vehicle_model'] = null;
        }


    }

    echo json_encode($visitors);
} catch (Exception $e) {
    echo json_encode([]);
}
