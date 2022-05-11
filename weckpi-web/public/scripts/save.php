<?php
    header("Content-Type: application/json");
    
    // get the data stored in php://input because data with an other content-type as application/x-www-form-urlencoded
    // or multipart/form-data is not stored in $_POST
    $data = json_decode(file_get_contents("php://input"), true);

    foreach($data["alarmtimes"] as $key => $value) {
        $url = $value["music"]["url"];
        // check if the urls are valid
        if(strpos($url, "http://") || strpos($url, "https://") || strpos($url, "ftp://")) {
            $headers = @get_headers($url);
            if(!$headers || strpos($headers[0], "404")) die(json_encode(["error" => "File not found: $url in $key"]));
        } else {
            if(!file_exists($url)) die(json_encode(["error" => "File not found: $url in $key"]));
        }
    }

    // save data in yaml file
    $yamlresult = yaml_emit_file("/etc/weckpi/config.yaml", $data);

    if(!$yamlresult) die(json_encode(["error" => "Error at parsing data to yaml"]));
    else {
        $file = fopen("/etc/weckpi/settings-changed");
        fclose($file);
        die(json_encode([]))
    }
?>