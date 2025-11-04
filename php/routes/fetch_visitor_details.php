<?php
require '../database/db_connect.php';
require '../config/encryption_key.php';
header('Content-Type: application/json');

$id = $_GET['id'] ?? null;
if (!$id) {
    echo json_encode(['success' => false, 'message' => 'Missing ID']);
    exit;
}

try {
    $stmt = $pdo->prepare("
        SELECT
            v.id,
            v.first_name,
            v.middle_name,
            v.last_name,
            v.contact_number,
            v.email,
            v.address,
            v.reason,
            v.id_photo_path,
            v.selfie_photo_path,
            v.date,
            v.time_in,
            v.time_out,
            v.status,
            v.personnel_related,
            v.office_to_visit
        FROM visitors v
        WHERE v.id = :id
    ");

    $stmt->execute([':id' => $id]);
    $visitor = $stmt->fetch(PDO::FETCH_ASSOC);

    if ($visitor) {
        // Decrypt sensitive data for display
        $visitor['first_name'];
        $visitor['middle_name'];
        $visitor['last_name'];
        $visitor['contact_number'];
        $visitor['email'];
        $visitor['address'];
        $visitor['office_to_visit'];

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
            $visitor['vehicle_owner'] = $full_name;
            $visitor['vehicle_brand'] = $vehicle['vehicle_brand'];
            $visitor['plate_number'] = $vehicle['plate_number'];
            $visitor['vehicle_color'] = $vehicle['vehicle_color'];
            $visitor['vehicle_model'] = $vehicle['vehicle_model'];
        } else {
            $visitor['vehicle_owner'] = null;
            $visitor['vehicle_brand'] = null;
            $visitor['plate_number'] = null;
            $visitor['vehicle_color'] = null;
            $visitor['vehicle_model'] = null;
        }

        echo json_encode(['success' => true, 'data' => $visitor]);
    } else {
        echo json_encode(['success' => false, 'message' => 'Visitor not found']);
    }
} catch (Exception $e) {
    echo json_encode(['success' => false, 'message' => 'Query error: ' . $e->getMessage()]);
}
