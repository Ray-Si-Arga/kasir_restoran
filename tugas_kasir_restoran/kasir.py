import json
import os

# membuat variabel persiapan untuk menjadikannya global variabel
nama_pembeli = None
pilihan_no = None
nama_menu = None
harga_makanan = 0
porsi_dibeli = 0
total_beli = 0
total_harga = 0
diskon = 0
total_bayar = 0
uang_tunai = 0
kembalian = 0

program_berjalan = False
FILE_NAME = "data_menu_makanan.json"

while True:
    print("\n ===== SISTEM KASIR RESTORAN =====")
    print("1. Input Nama Pembeli & Pesanan")
    print("2. Input Makanan & Harga")
    print("3. Keluar Dari Sistem")

    pilihan = input("\n Silahkan Pilih Nomor Berapa : ")

    if pilihan == "1":
        program_berjalan = True

        nama_pembeli = input("Nama Pembeli : ")

        # Program baca file JSON
        if os.path.exists(FILE_NAME):
            with open(FILE_NAME, "r") as file:
                try:
                    data_list = json.load(file)
                except json.JSONDecodeError:
                    data_list = []
        else:
            data_list = []

        print("\n=== DAFTAR MENU SAAT INI ===")
        if not data_list:
            print("Belum ada menu yang ditambahkan.\n")
        else:
            
            # membuat tampilan pada menu
            print(f"{'No':<4} {'Menu':<15} {'Harga':<10} {'Stok/Porsi Tersedia':<10}")
            print("-" * 50)
            for i, item in enumerate(data_list, start=1):
                stok = item.get("jumlah", 0)
                print(f"{i:<4} {item['nama']:<15} {item['harga']:<10} {stok:<10}")
            print()

            pilihan_no = input("Pilih Nomor Menu (misal: 1) : ")

            # memilih menu berdasarkan digit
            if pilihan_no.isdigit():
                idx = int(pilihan_no) - 1

                if 0 <= idx < len(data_list):
                    menu_terpilih = data_list[idx]
                    stok_sekarang = int(menu_terpilih.get("jumlah", 0))

                    if stok_sekarang <= 0:
                        print(f"\n Maaf, stok menu '{menu_terpilih['nama']}' sedang KOSONG!")
                    else:
                        input_porsi = input(f"Porsi yang dibeli (Tersedia {stok_sekarang}) : ")

                        if input_porsi.isdigit():
                            porsi_dibeli = int(input_porsi)

                            if porsi_dibeli <= 0:
                                print("Jumlah porsi harus lebih dari 0!")
                            elif porsi_dibeli > stok_sekarang:
                                print(f"Stok tidak cukup! Hanya tersedia {stok_sekarang} porsi.")
                            else:
                                nama_menu = menu_terpilih['nama']
                                harga_makanan = int(menu_terpilih['harga'])
                                total_harga = harga_makanan * porsi_dibeli
                                total_beli = total_harga

                                # 1. Hitung Diskon
                                if total_harga >= 150000:
                                    diskon = (30 / 100) * total_harga
                                elif total_harga >= 100000:
                                    diskon = (20 / 100) * total_harga
                                elif total_harga >= 50000:
                                    diskon = (10 / 100) * total_harga
                                else:
                                    diskon = 0

                                # 2. Hitung Total Bayar yang harus dibayar
                                total_bayar = total_harga - diskon

                                print(f"\nSubtotal Total Belanja  : Rp.{total_harga}")
                                print(f"Diskon Dipakai            : Rp.{int(diskon)}")
                                print(f"Total Yang Harus Dibayar  : Rp.{int(total_bayar)}")

                                # 3. Input Uang Tunai & Loop jika uang kurang
                                while True:
                                    input_uang = input("Uang Sebesar : Rp.")
                                    if input_uang.isdigit():
                                        uang_tunai = int(input_uang)
                                        if uang_tunai < total_bayar:
                                            print(f"Uang kurang! Minimal pembayaran adalah Rp.{int(total_bayar)}")
                                        else:
                                            break
                                    else:
                                        print("Uang harus berupa angka!")

                                # 4. Hitung Kembalian berdasarkan total_bayar
                                kembalian = uang_tunai - total_bayar
                                print(f"Kembalian: Rp.{int(kembalian)}")
                                print(f"Sisa stok '{nama_menu}': {data_list[idx]['jumlah']}") 
                                
                                print("\n========================================")
                                print("            NOTA PEMBAYARAN            ")
                                print("========================================")
                                print(f"Nama Pembeli : {nama_pembeli}")
                                print(f"Makanan      : {nama_menu}")
                                print(f"Harga Satuan : Rp.{harga_makanan}")
                                print(f"Jumlah Porsi : {porsi_dibeli}")
                                print(f"Subtotal     : Rp.{total_harga}")
                                print(f"Diskon       : Rp.{int(diskon)}")
                                print("----------------------------------------")
                                print(f"Total Bayar  : Rp.{int(total_bayar)}")
                                print("----------------------------------------")
                                print(f"Uang Tunai   : Rp.{int(uang_tunai)}")
                                print(f"Kembalian    : Rp.{int(kembalian)}")
                                print("========================================")         

                                # Kurangi stok & simpan ke file JSON
                                data_list[idx]["jumlah"] = stok_sekarang - porsi_dibeli
                                with open(FILE_NAME, "w") as file:
                                    json.dump(data_list, file, indent=4)
                        else:
                            print("Porsi harus berupa angka!")
                else:
                    print("Nomor menu tidak ada di daftar!")
            else:
                print("Input harus berupa angka nomor menu!")

    elif pilihan == "2":
        program_berjalan = True

        # memanggil file json untuk diambil datanya
        if os.path.exists(FILE_NAME):
            with open(FILE_NAME, "r") as file:
                try:
                    data_list = json.load(file)
                except json.JSONDecodeError:
                    data_list = []
        else:
            data_list = []

        print("\n=== DAFTAR MENU SAAT INI ===")
        
        # Jika data tidak ada menampilkan menu tidakk ada
        if not data_list:
            print("Belum ada menu yang ditambahkan.\n")
        else:
            # membuat judul dan memberikan masing masing judul padding atau spasi
            print(f"{'No':<4} {'Menu':<15} {'Harga':<10} {'Jumlah':<10}")
            # print - sebanyak 38
            print("-" * 38)
            
            # melakukan perulangan dan menghasilkan tampilan seperti list harga
            for i, item in enumerate(data_list, start=1):
                print(f"{i:<4} {item['nama']:<15} {item['harga']:<10} {item['jumlah']:<15}")
            print()

        while True:
            # membuat pembuatan id otomatis
            id_menu = len(data_list) + 1

            nama = input("Masukkan Nama Menu Baru (atau ketik '3' untuk berhenti & simpan): ")
            if nama == "3":
                break

            harga = int(input(f"Masukkan Harga Untuk {nama}: "))
            jumlah = int(input(f"Masukkan Jumlah {nama}: "))

            # memasukkan data ke dalam judul yang ada / variabel yang sudah disiapkan
            data_list.append({"id": id_menu, "nama": nama, "harga": harga, "jumlah": jumlah})

        # memanggil file json dan menyimpannya
        with open(FILE_NAME, "w") as file:
            json.dump(data_list, file, indent=4)

        print(f"\n Data menu berhasil diperbarui dan tersimpan!")

        # jika tidak ada nama pembeli atau menu yang dipesan, print dari not akan muncul
        # if not nama_pembeli or not nama_menu:
        #     print("\n Belum ada transaksi! Silakan pilih menu 1 terlebih dahulu.")
        # else:
            

    elif pilihan == "3":
        print("Program Dihentikan (Terima Kasih)...")
        break

    else:
        print("Nomor tidak dikenali, silakan pilih menu 1-3.")