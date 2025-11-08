<?php
$path = 'public/uploads/selfies/737149ed34be16ffdeba1977392f6903a6f0c96ce8fdc814379b77b20745b4c8.jpg';
$filename = basename($path);
echo 'Filename: ' . $filename . PHP_EOL;
echo 'Full path from fetch_request_image.php: ' . __DIR__ . '/../public/uploads/selfies/' . $filename . PHP_EOL;
echo 'Does file exist? ' . (file_exists(__DIR__ . '/../public/uploads/selfies/' . $filename) ? 'Yes' : 'No') . PHP_EOL;
?>
