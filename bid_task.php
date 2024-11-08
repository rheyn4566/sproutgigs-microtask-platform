<?php
session_start();
require 'db.php';

if ($_SESSION['role'] !== 'freelancer') {
    die('Unauthorized access');
}

$task_id = $_GET['task_id'];

if ($_SERVER['REQUEST_METHOD'] == 'POST') {
    $bid_amount = $_POST['bid_amount'];
    $stmt = $conn->prepare("INSERT INTO bids (task_id, freelancer_id, bid_amount) VALUES (?, ?, ?)");
    $stmt->bind_param("iid", $task_id, $_SESSION['user_id'], $bid_amount);
    $stmt->execute();
    echo 'Bid submitted successfully!';
}
?>
<form method="post">
    Bid Amount: <input type="number" name="bid_amount" step="0.01" required><br>
    <button type="submit">Place Bid</button>
</form>
