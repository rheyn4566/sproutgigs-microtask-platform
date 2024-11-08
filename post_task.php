<?php
session_start();
require 'db.php';

if ($_SERVER['REQUEST_METHOD'] == 'POST' && $_SESSION['role'] == 'client') {
    $title = $_POST['title'];
    $description = $_POST['description'];
    $budget = $_POST['budget'];
    
    $stmt = $conn->prepare("INSERT INTO tasks (client_id, title, description, budget) VALUES (?, ?, ?, ?)");
    $stmt->bind_param("issd", $_SESSION['user_id'], $title, $description, $budget);
    $stmt->execute();

    echo 'Task posted successfully!';
}
?>
<form method="post">
    Title: <input type="text" name="title" required><br>
    Description: <textarea name="description" required></textarea><br>
    Budget: <input type="number" step="0.01" name="budget" required><br>
    <button type="submit">Post Task</button>
</form>
