<?php
session_start();
require_once __DIR__ . '/../database/db_connect.php';

// Check if any admin user exists
try {
    $stmt = $pdo->prepare("SELECT COUNT(*) FROM users WHERE role = 'Admin'");
    $stmt->execute();
    $adminCount = $stmt->fetchColumn();
} catch (PDOException $e) {
    die("Database error during admin check: " . $e->getMessage());
}

// If no admin exists, redirect to seed_admin.php
if ($adminCount == 0) {
    header("Location: routes/seed_admin.php");
    exit;
}

// If admin already exists, redirect to login page
header("Location: /iSecure-Final-Def-System-Folder/php/routes/Pages/login-page.php");
exit;
?>