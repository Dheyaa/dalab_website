<?php
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $name = $_POST["Name"];
    $email = $_POST["Mail"];
    $message = $_POST["Message"];
    $to = "deaa86_arch@hotmail.com"; // Replace with your email address
    $subject = "Contact Form Submission";

    $body = "Name: $name\n";
    $body .= "Email: $email\n";
    $body .= "Message:\n$message";

    if (mail($to, $subject, $body)) {
        echo "Thank you! Your message has been sent.";
    } else {
        echo "Sorry, something went wrong and we couldn't send your message.";
    }
}
?>