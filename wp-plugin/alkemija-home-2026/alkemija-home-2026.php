<?php
/*
Plugin Name: Alkemija Naslovnica 2026
Description: Nova naslovnica alkemija.hr (EN na /, HR na /hr/, IT na /it/) iz samostalnih HTML datoteka u /pages/. Stara Elementor naslovnica (stranica 1479) ostaje netaknuta i prikazuje se na /home-2/ (noindex). ROLLBACK: deaktiviraj ovaj plugin — sve se vraća kako je bilo.
Version: 1.0.4
Author: Alkemija
Source: https://github.com/kaidoalen/alkemija-hr-redizajn-preview
*/
if (!defined('ABSPATH')) exit;

function alk26_path() {
    return strtolower(trim((string) parse_url($_SERVER['REQUEST_URI'] ?? '', PHP_URL_PATH), '/'));
}

/* /home-2/ -> render the old Elementor homepage (page 1479) exactly as before. */
add_filter('request', function ($qv) {
    if (is_admin()) return $qv;
    if (alk26_path() === 'home-2') return array('page_id' => 1479);
    return $qv;
}, 1);
add_filter('redirect_canonical', function ($url) {
    return alk26_path() === 'home-2' ? false : $url;
});
add_filter('wp_robots', function ($r) {
    if (alk26_path() === 'home-2') { $r['noindex'] = true; $r['nofollow'] = true; unset($r['max-image-preview']); }
    return $r;
}, 99);

/* Keep GA4 + Alkemija outbound/mail_id tracking: copy only those scripts from wp_head/wp_footer. */
function alk26_tracking($hook) {
    ob_start();
    if ($hook === 'head') wp_head(); else wp_footer();
    $html = ob_get_clean();
    $out = '';
    if (preg_match_all('#<script\b[^>]*>.*?</script>#is', $html, $m)) {
        foreach ($m[0] as $s) {
            if (preg_match('#googletagmanager\.com/gtag|gtag\(|__akMID|__akOutbound#', $s)) $out .= $s . "\n";
        }
    }
    return $out;
}

/* Serve the new homepage: / (EN), /hr/ (HR), /it/ (IT). */
add_action('template_redirect', function () {
    if (is_admin() || is_preview() || isset($_GET['elementor-preview']) || isset($_GET['preview']) || isset($_GET['p']) || isset($_GET['page_id']) || isset($_GET['s'])) return;
    if (($_SERVER['REQUEST_METHOD'] ?? 'GET') !== 'GET' && ($_SERVER['REQUEST_METHOD'] ?? '') !== 'HEAD') return;
    $path = alk26_path();
    $map = array('' => 'en', 'hr' => 'hr', 'it' => 'it');
    if (!array_key_exists($path, $map)) return;
    if ($path === '' && !is_front_page()) return;
    $file = __DIR__ . '/pages/' . $map[$path] . '.html';
    if (!is_readable($file)) return;
    $html = file_get_contents($file);
    $head = alk26_tracking('head');
    $foot = alk26_tracking('footer');
    if ($head) $html = preg_replace('#</head>#i', $head . '</head>', $html, 1);
    if ($foot) $html = preg_replace('#</body>#i', $foot . '</body>', $html, 1);
    status_header(200);
    global $wp_query; if ($wp_query) $wp_query->is_404 = false;
    header('Content-Type: text/html; charset=UTF-8');
    header('X-Alkemija-Home: 2026-' . $map[$path]);
    echo $html;
    exit;
}, 1);
