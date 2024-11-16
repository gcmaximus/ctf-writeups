<?php
$ip_address = $_SERVER['HTTP_X_BIOCORP_VPN'] ?? $_SERVER['REMOTE_ADDR'];

if ($ip_address !== '80.187.61.102') {
    echo "<h1>Access Denied</h1>";
    echo "<p>You do not have permission to access this page.</p>";
    exit;
}

if ($_SERVER['REQUEST_METHOD'] === 'POST' && strpos($_SERVER['CONTENT_TYPE'], 'application/xml') !== false) {
    $xml_data = file_get_contents('php://input');
    $doc = new DOMDocument();
    if (!$doc->loadXML($xml_data, LIBXML_NOENT)) {
        echo "<h1>Invalid XML</h1>";
        exit;
    }
} else {
    $xml_data = file_get_contents('data/reactor_data.xml');
    $doc = new DOMDocument();
    $doc->loadXML($xml_data, LIBXML_NOENT);
}

$temperature = $doc->getElementsByTagName('temperature')->item(0)->nodeValue ?? 'Unknown';
$pressure = $doc->getElementsByTagName('pressure')->item(0)->nodeValue ?? 'Unknown';
$control_rods = $doc->getElementsByTagName('control_rods')->item(0)->nodeValue ?? 'Unknown';

include 'header.php';
?>

<div class="container center-content">
    <h1>Welcome to the Control Panel</h1>
    <p>Here you can view reactor values:</p>

    <ul class="reactor-values">
        <li><i class="fas fa-thermometer-half"></i> Temperature: <?php echo htmlspecialchars($temperature); ?> °C</li>
        <li><i class="fas fa-tachometer-alt"></i> Pressure: <?php echo htmlspecialchars($pressure); ?> kPa</li>
        <li><i class="fas fa-cogs"></i> Control Rods: <?php echo htmlspecialchars($control_rods); ?></li>
    </ul>

    <button id="refresh-btn">Refresh Reactor Values</button>
</div>

<script>
    document.getElementById('refresh-btn').addEventListener('click', function () {
        location.reload();
    });
</script>

<?php include 'footer.php'; ?>
