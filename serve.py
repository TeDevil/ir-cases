# -*- coding: utf-8 -*-
"""
在局域网里把这个 app 跑起来，方便先在电脑/手机上试手感。

用法（在本文件所在目录打开 PowerShell）：
    ..\\.venv\\Scripts\\python.exe serve.py
    ..\\.venv\\Scripts\\python.exe serve.py 8080     # 换端口

然后把打印出来的 http://192.168.x.x:8000/index.html 在手机浏览器里打开。

⚠ 重要区别：这是 **http** 局域网地址，iOS/Android 都不允许在非 https 下
   注册 Service Worker，所以「断网也能打开」在这里不会生效
   （但功能完全正常，只要手机和电脑在同一个 WiFi）。
   要真的离线可用，请按《部署到GitHub Pages.md》放到 https 静态托管上。

   这一点正是我们选择 GitHub Pages 的原因 —— 它天然是 https。
"""

import http.server
import mimetypes
import os
import socket
import socketserver
import sys

mimetypes.add_type("application/manifest+json", ".webmanifest")
mimetypes.add_type("text/javascript", ".js")
mimetypes.add_type("image/png", ".png")


def lan_ips():
    """本机的内网 IPv4 地址（多网卡机器上尽量只给能用的那个）"""
    ips = []
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(0.5)
        s.connect(("10.255.255.255", 1))
        first = s.getsockname()[0]
        if first and not first.startswith("127."):
            ips.append(first)
        s.close()
    except OSError:
        pass
    try:
        for info in socket.getaddrinfo(socket.gethostname(), None,
                                       socket.AF_INET):
            ip = info[4][0]
            if ip.startswith("127.") or ip.startswith("169.254."):
                continue
            if ip not in ips:
                ips.append(ip)
    except OSError:
        pass
    return ips


class Handler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # 开发时别让缓存捣乱：Service Worker 本来也不该缓存 index
        self.send_header("Cache-Control", "no-store")
        super().end_headers()

    def log_message(self, fmt, *args):
        sys.stdout.write("  %s\n" % (fmt % args))


def main():
    for s in (sys.stdout, sys.stderr):
        try:
            s.reconfigure(encoding="utf-8", errors="replace")
        except Exception:                                    # noqa: BLE001
            pass

    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8000
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    socketserver.TCPServer.allow_reuse_address = True
    try:
        httpd = socketserver.ThreadingTCPServer(("0.0.0.0", port), Handler)
    except OSError as exc:
        print(f"  端口 {port} 起不来：{exc}")
        print(f"  换个端口试试：python serve.py {port + 1}")
        return 1

    ips = lan_ips()
    print("=" * 58)
    print("  介入病例库 · 手机离线建档 —— 本地预览")
    print("=" * 58)
    print(f"  目录：{os.getcwd()}")
    print()
    print("  手机浏览器打开下面任一地址：")
    for ip in ips:
        print(f"     http://{ip}:{port}/index.html")
    print(f"     http://127.0.0.1:{port}/index.html    （本机测试）")
    print()
    if not ips:
        print("  ⚠ 没检测到内网 IP —— 手机可能连不上，检查网络")
    print("  手机和这台电脑必须在同一个 WiFi / 局域网。")
    print()
    print("  提示：http 地址下离线缓存不生效（需要 https）。")
    print("       要真正断网可用，请部署到 GitHub Pages。")
    print()
    print("  按 Ctrl+C 停止。")
    print("=" * 58)

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n  已停止。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
