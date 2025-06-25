# versi terbaru python
FROM python:3.11-slim-buster

# Atur direktori kerja di dalam kontainer menjadi /app
# Semua perintah habis ini akan dijalankan dari direktori ini
WORKDIR /app

COPY requirements.txt .

# Instal semua dependensi Python yang tercantum dalam requirements.txt, --no-cache-dir untuk mengurangi ukuran image dan -r requirements.txt untuk menginstal dari file requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Salin semua file lainnya dari direktori proyek app.py dan folder templates ke dalam direktori /app di kontainer
COPY . .

# kontainer akan mendengarkan di port 5000 saat runtime dan memberi tau dockert
EXPOSE 5000

# perintah default yang akan dijalankan saat kontainer dimulai
# menjalankan app.py menggunakan interpreter python
CMD ["python", "app.py"]