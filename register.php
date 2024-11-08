<?php
session_start();
require 'db.php';

if ($_SERVER['REQUEST_METHOD'] == 'POST') {
    $username = $_POST['username'];
    $password = password_hash($_POST['password'], PASSWORD_BCRYPT);
    $role = $_POST['role'];
    $referral_code = uniqid();

    $stmt = $conn->prepare("INSERT INTO users (username, password, role, referral_code) VALUES (?, ?, ?, ?)");
    $stmt->bind_param("ssss", $username, $password, $role, $referral_code);
    $stmt->execute();
    echo 'Registration successful!';
}
?>
<form method="post">
    Username: <input type="text" name="username" required><br>
    Password: <input type="password" name="password" required><br>
    Role: <select name="role">
        <option value="client">Client</option>
        <option value="freelancer">Freelancer</option>
    </select><br>
    <button type="submit">Register</button>
</form>
