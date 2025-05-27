<?php
// guardar.php
ini_set('display_errors', 0);
ini_set('log_errors',    1);
error_reporting(E_ALL);

//Limpia datos anteriores
if (ob_get_length()) ob_clean();

//Ruta
define('BASE_DIR', __DIR__);
$propDir = BASE_DIR . '/';    

// Subir archivo
if (isset($_GET['upload'])) {
    header('Content-Type: application/json; charset=utf-8');

    $nombre = trim($_POST['nombre'] ?? '');
    $tipo   = $_POST['tipo'] ?? '';       // 'fotos' o 'apoyos'
    if (!$nombre || !in_array($tipo,['fotos','apoyos'])) {
        http_response_code(400);
        echo json_encode(['ok'=>false,'error'=>'Parámetros inválidos.']);
        exit;
    }
    $safeUser = preg_replace('/[^A-Za-z0-9_\-]/','_',$nombre);
    $userFolder = BASE_DIR . "/{$safeUser}";
    if (!is_dir($userFolder)) {
        if (!mkdir($userFolder,0755,true)) {
            http_response_code(500);
            echo json_encode(['ok'=>false,'error'=>'No se creó carpeta usuario.']);
            exit;
        }
    }
    if (!isset($_FILES['archivo'])) {
        http_response_code(400);
        echo json_encode(['ok'=>false,'error'=>'No hay archivo enviado.']);
        exit;
    }
    $f = $_FILES['archivo'];
    if ($f['error'] !== UPLOAD_ERR_OK) {
        http_response_code(400);
        echo json_encode(['ok'=>false,'error'=>"Error upload code {$f['error']}"]);
        exit;
    }
    // Genera un nombre
    $ext = pathinfo($f['name'], PATHINFO_EXTENSION);
    $uniq = uniqid("{$tipo}_", true).($ext? ".{$ext}":'');
    $dest = "{$userFolder}/{$uniq}";
    if (move_uploaded_file($f['tmp_name'], $dest)) {
        echo json_encode(['ok'=>true,'file'=> $uniq]);
    } else {
        http_response_code(500);
        echo json_encode(['ok'=>false,'error'=>'No se movió el archivo.']);
    }
    exit;
}

// Guardado de metadatos de archivos o imagéens
header('Content-Type: application/json; charset=utf-8');
$raw = file_get_contents('php://input');
$data = json_decode($raw,true);
if (!$data) {
    http_response_code(400);
    echo json_encode(['ok'=>false,'error'=>'JSON inválido o vacío.']);
    exit;
}
$nombre = trim($data['nombre'] ?? '');
if ($nombre==='') {
    http_response_code(400);
    echo json_encode(['ok'=>false,'error'=>'Falta campo nombre.']);
    exit;
}
$safeUser = preg_replace('/[^A-Za-z0-9_\-]/','_',$nombre);
$userFolder = BASE_DIR . "/{$safeUser}";
if (!is_dir($userFolder)) {
    if (!mkdir($userFolder,0755,true)) {
        http_response_code(500);
        echo json_encode(['ok'=>false,'error'=>'No se creó carpeta usuario.']);
        exit;
    }
}
// Prepara archivo JSON
$ts = date('Ymd_His');
$fn = "{$safeUser}_{$ts}.json";
$fp = "{$userFolder}/{$fn}";
if (file_put_contents($fp, json_encode($data, JSON_UNESCAPED_UNICODE|JSON_PRETTY_PRINT))) {
    echo json_encode(['ok'=>true,'archivo'=> "{$safeUser}/{$fn}"]);
} else {
    http_response_code(500);
    echo json_encode(['ok'=>false,'error'=>'Error al escribir JSON.']);
}
exit;
