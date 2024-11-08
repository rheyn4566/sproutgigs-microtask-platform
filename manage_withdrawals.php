<?php
session_start();
require 'db.php';

if (!isset($_SESSION['user_id']) || $_SESSION['role'] !== 'admin') {
    die('Unauthorized access');
}

if ($_SERVER['REQUEST_METHOD'] == 'POST') {
    $withdrawal_id = $_POST['withdrawal_id'];
    $action = $_POST['action'];

    if ($action == 'approve') {
        $stmt = $conn->prepare("UPDATE withdrawals SET status = 'approved', processed_at = NOW() WHERE id = ?");
    } elseif ($action == 'reject') {
        $stmt = $conn->prepare("UPDATE withdrawals SET status = 'rejected', processed_at = NOW() WHERE id = ?");
    }
    $stmt->bind_param("i", $withdrawal_id);
    $stmt->execute();

    echo "Withdrawal $action successfully!";
}

// Retrieve pending withdrawals
$stmt = $conn->prepare("SELECT w.id, u.username, w.amount, w.requested_at FROM withdrawals w JOIN users u ON w.user_id = u.id WHERE w.status = 'pending'");
$stmt->execute();
$result = $stmt->get_result();

echo "<h2>Pending Withdrawals</h2>";
while ($withdrawal = $result->fetch_assoc()) {
    echo "<p>User: {$withdrawal['username']}, Amount: \${$withdrawal['amount']}, Requested At: {$withdrawal['requested_at']}</p>";
    echo "<form method='post'>
            <input type='hidden' name='withdrawal_id' value='{$withdrawal['id']}'>
            <button name='action' value='approve'>Approve</button>
            <button name='action' value='reject'>Reject</button>
          </form>";
}
?>
