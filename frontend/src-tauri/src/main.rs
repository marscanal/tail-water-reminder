#![cfg_attr(
    all(not(debug_assertions), target_os = "windows"),
    windows_subsystem = "windows"
)]

use tauri_plugin_shell::ShellExt;

fn main() {
    tauri::Builder::default()
        .plugin(tauri_plugin_shell::init())
        .plugin(tauri_plugin_notification::init())
        .setup(|app| {
            let handle = app.handle().clone();

            tauri::async_runtime::spawn(async move {
                let (_rx, _child) = handle.shell()
                    .command("node")
                    .args(&["../backend/index.js"])
                    .spawn()
                    .expect("Failed to spawn backend");
                // 这里 _rx 是用来监听子进程的输出的，如果想拿到日志，可以用它
            });

            Ok(())
        })
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
