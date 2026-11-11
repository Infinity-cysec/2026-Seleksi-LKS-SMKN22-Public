#!/usr/bin/env python3
import socket
import threading

HOST = "0.0.0.0"
PORT = 1337

FLAG = "SMKN22{Analytic_Ins1d3n_rEs90n_GGWP}"

QUESTIONS = [
    (
        "1. Victim Identification\n"
        "Identifikasi alamat IP komputer korban yang mengirimkan "
        "HTTP POST mencurigakan ke server eksternal.\n"
        "Masukkan IP korban:",
        ["10.10.20.15"]
    ),
    (
        "2. C2 Server Identification\n"
        "Tentukan alamat IP server Command and Control (C2) "
        "yang menerima komunikasi mencurigakan serta port yang digunakan.\n"
        "Format: IP:PORT",
        ["198.51.100.66:80"]
    ),
    (
        "3. FTP Credentials\n"
        "Temukan username dan password yang digunakan korban "
        "untuk melakukan autentikasi ke server FTP.\n"
        "Format: username:password",
        ["finance01:finac$@!!2027"]
    ),
    (
        "4. Code Secret\n"
        "Temukan fragmen kode secret yang dikirimkan, "
        "gabungkan dan lakukan decoding.\n"
        "Masukkan teks asli hasil decoding:",
        ["secretmalware008"]
    ),
    (
        "5. Suspicious Domain\n"
        "Identifikasi domain yang digunakan dalam komunikasi "
        "Masukkan domain mencurigakan:",
        ["update-security.ichik1wir.com"]
    ),
    (
        "6. Path Identification\n"
        "Identifikasi path atau endpoint yang digunakan "
        "untuk mengirim fragmen Code Secret ke server C2.\n"
        "Format: /path",
        ["/upload"]
    ),
]


def send_line(conn, message):
    conn.sendall((message + "\r\n").encode())


def send_prompt(conn, message):
    conn.sendall(message.encode())


def receive_line(conn):
    data = bytearray()

    while True:
        char = conn.recv(1)

        if not char:
            return None

        if char == b"\n":
            return data.decode("utf-8").strip()

        if char != b"\r":
            data.extend(char)

        if len(data) > 1024:
            return data.decode("utf-8").strip()


def handle_client(conn, address):
    print(f"[+] Peserta terhubung: {address}")

    try:
        conn.settimeout(300)

        send_line(conn, "")
        send_line(conn, "======================================")
        send_line(conn, " OPERATION SILENT INFECTION")
        send_line(conn, "======================================")
        send_line(conn, "Jawab semua pertanyaan dengan benar.")
        send_line(conn, "")

        for nomor, (prompt, accepted) in enumerate(QUESTIONS, 1):

            send_line(conn, prompt)
            send_prompt(conn, "> ")

            answer = receive_line(conn)

            if answer is None:
                return

            answer = answer.strip().lower()

            accepted = [
                item.lower() for item in accepted
            ]

            if answer in accepted:
                send_line(conn, "[+] BENAR")
                send_line(conn, "")

                print(
                    f"[+] {address} menjawab soal {nomor} dengan benar"
                )

            else:
                send_line(conn, "[-] SALAH NIH KURANG TELITI!")

                print(
                    f"[-] {address} gagal di soal {nomor}"
                )

                return

        send_line(conn, "======================================")
        send_line(conn, "SEMUA JAWABAN BENAR!")
        send_line(conn, "SELAMAT, MENJADI SEPUHNYA PARAH SEPUH!")
        send_line(conn, "")
        send_line(conn, f"FLAG: {FLAG}")
        send_line(conn, "======================================")

        print(f"[+] {address} berhasil mendapatkan flag!")

    except (socket.timeout, ConnectionError, OSError) as error:
        print(f"[!] Koneksi bermasalah: {error}")

    finally:
        conn.close()


def main():

    print("======================================")
    print(" OPERATION SILENT INFECTION")
    print(" NC SUBMISSION SERVER")
    print("======================================")
    print(f"Listening: {HOST}:{PORT}")

    server = socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM
    )

    server.setsockopt(
        socket.SOL_SOCKET,
        socket.SO_REUSEADDR,
        1
    )

    server.bind((HOST, PORT))
    server.listen(20)

    print("[+] Server siap menerima peserta!")

    try:
        while True:

            conn, address = server.accept()

            thread = threading.Thread(
                target=handle_client,
                args=(conn, address),
                daemon=True
            )

            thread.start()

    except KeyboardInterrupt:
        print("\n[!] Server dihentikan.")

    finally:
        server.close()


if __name__ == "__main__":
    main()
