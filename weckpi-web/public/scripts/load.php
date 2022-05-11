<?php
    header('Content-Type: application/json');
    echo json_encode(yaml_parse(file_get_contents('/etc/weckpi/config.yaml')));
?>
