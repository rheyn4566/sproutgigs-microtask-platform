<?php
session_start();
require 'db.php';

if (!isset($_SESSION['user_id'])) {
    die('Unauthorized access');
}

echo "<h2>Dashboard</h2>";

if ($_SESSION['role'] == 'client') {
    echo "<p>Your Posted Tasks</p>";
    // Fetch and display client tasks
} elseif ($_SESSION['role'] == 'freelancer') {
    echo "<p>Your Bids</p>";
    // Fetch and display freelancer bids
}
?>
