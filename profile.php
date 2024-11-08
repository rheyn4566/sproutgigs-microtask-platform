<?php
session_start();
require 'db.php';

if (!isset($_SESSION['user_id'])) {
    die('Unauthorized access');
}

$user_id = $_SESSION['user_id'];

// Fetch user details
$stmt = $conn->prepare("SELECT username, role FROM users WHERE id = ?");
$stmt->bind_param("i", $user_id);
$stmt->execute();
$result = $stmt->get_result();
$user = $result->fetch_assoc();

// Update profile details
if ($_SERVER['REQUEST_METHOD'] == 'POST') {
    $new_username = $_POST['username'];
    $stmt = $conn->prepare("UPDATE users SET username = ? WHERE id = ?");
    $stmt->bind_param("si", $new_username, $user_id);
    $stmt->execute();
    echo 'Profile updated successfully!';
}
?>
<h2>Profile</h2>
<form method="post">
    Username: <input type="text" name="username" value="<?php echo $user['username']; ?>" required><br>
    Role: <?php echo ucfirst($user['role']); ?><br>
    <button type="submit">Update Profile</button>
</form>
