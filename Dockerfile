# Gunakan image dasar Python resmi yang ringan (versi 3.9 berdasarkan Debian Buster)
FROM python:3.11-slim-buster

# Atur direktori kerja di dalam kontainer menjadi /app
# Semua perintah setelah ini akan dijalankan dari direktori ini
WORKDIR /app

# Salin file requirements.txt dari komputer Anda ke dalam direktori /app di kontainer
COPY requirements.txt .

# Instal semua dependensi Python yang tercantum dalam requirements.txt
# --no-cache-dir untuk mengurangi ukuran image
# -r requirements.txt untuk menginstal dari file requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Salin semua file lainnya dari direktori proyek di komputer Anda (yaitu app.py dan folder templates)
# ke dalam direktori /app di kontainer
COPY . .

# Beri tahu Docker bahwa kontainer akan mendengarkan di port 5000 saat runtime
EXPOSE 5000

# Perintah default yang akan dijalankan saat kontainer dimulai
# Ini akan menjalankan app.py menggunakan interpreter python
CMD ["python", "app.py"]