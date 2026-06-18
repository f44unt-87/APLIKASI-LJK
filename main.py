# Di dalam fungsi proses_gambar, ganti bagian loop 'for opsi, (x_raw, y_raw) in pilihan.items():'
# dengan kode ini agar lebih stabil:

    for no, pilihan in KOORDINAT.items():
        hasil_jawaban[no] = "-"
        max_density = 0
        
        # Urutan kunci agar A, B, C, D, E terbaca dengan benar
        for opsi in ['A', 'B', 'C', 'D', 'E']:
            if opsi not in pilihan: continue
            
            x_raw, y_raw = pilihan[opsi]
            x = int(x_raw + OFFSET_X)
            y = int(y_raw + OFFSET_Y + (int(no) * 0.1)) 
            
            # Gambar lingkaran merah untuk setiap opsi
            cv2.circle(img_visual, (x, y), 15, (0, 0, 255), 2)
            
            roi = img_warped[y-25:y+25, x-25:x+25]
            if roi.size == 0: continue
            
            gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
            _, thresh = cv2.threshold(gray, 120, 255, cv2.THRESH_BINARY_INV)
            kepadatan = cv2.countNonZero(thresh) / thresh.size
            
            if kepadatan > 0.20 and kepadatan > max_density:
                max_density = kepadatan
                hasil_jawaban[no] = opsi
