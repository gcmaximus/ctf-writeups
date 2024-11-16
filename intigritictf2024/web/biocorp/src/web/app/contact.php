<?php include 'header.php'; ?>

<div class="container center-content">
    <h1>Contact Us</h1>
    <p>If you have any questions or would like more information about our services, feel free to reach out to us.</p>

    <section class="contact-info">
        <p><strong>Email:</strong> info@biocorp.co.uk</p>
        <p><strong>Phone:</strong> +1 (800) 555-1234</p>
        <p><strong>Address:</strong> 123 Nuclear Way, Reactor City, UK</p>
    </section>

    <section class="contact-form">
        <h2>Send Us a Message</h2>
        <form action="#" method="post">
            <label for="name">Name:</label>
            <input type="text" id="name" name="name" required>

            <label for="email">Email:</label>
            <input type="email" id="email" name="email" required>

            <label for="message">Message:</label>
            <textarea id="message" name="message" rows="5" required></textarea>

            <button type="submit">Send Message</button>
        </form>
    </section>

    <section class="map">
        <h2>Our Location</h2>
        <iframe
            src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d2996.7196664164853!2d-0.08136292307939136!3d51.51836730990162!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x48761cb3bd814cf3%3A0x35f642aa1d1eac9b!2sThe%20Mayor%20of%20Scaredy%20Cat%20Town!5e1!3m2!1sen!2suk!4v1728940244526!5m2!1sen!2suk"
            width="600"
            height="450"
            style="border:0;"
            allowfullscreen=""
            loading="lazy"></iframe>
    </section>
</div>

<?php include 'footer.php'; ?>
