<?php
session_start();
require 'db.php';

if (!isset($_SESSION['user_id']) || $_SESSION['role'] !== 'freelancer') {
    die('Unauthorized access');
}

if ($_SERVER['REQUEST_METHOD'] == 'POST') {
    $amount = $_POST['amount'];

    // Check if the freelancer has enough balance
    $stmt = $conn->prepare("SELECT balance FROM users WHERE id = ?");
    $stmt->bind_param("i", $_SESSION['user_id']);
    $stmt->execute();
    $result = $stmt->get_result();
    $user = $result->fetch_assoc();

    if ($user['balance'] >= $amount) {
        // Deduct amount from balance and record the withdrawal request
        $stmt = $conn->prepare("UPDATE users SET balance = balance - ? WHERE id = ?");
        $stmt->bind_param("di", $amount, $_SESSION['user_id']);
        $stmt->execute();

        $stmt = $conn->prepare("INSERT INTO withdrawals (user_id, amount) VALUES (?, ?)");
        $stmt->bind_param("id", $_SESSION['user_id'], $amount);
        $stmt->execute();

        echo 'Withdrawal request submitted!';
    } else {
        echo 'Insufficient balance.';
    }
}
?>
<form method="post">
    Amount: <input type="number" name="amount" step="0.01" required><br>
    <button type="submit">Request Withdrawal</button>
</form>
