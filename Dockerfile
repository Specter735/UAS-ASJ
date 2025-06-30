# memeulai image dengan versi python ini
FROM python:3.11-slim-buster
# /app menjadi direktori didalam kontainer
WORKDIR /app
# salin dari host ke direktori /app
COPY requirements.txt .
# perintah pip install yang menginstal semua dpendensi python di dalam requirement. mengurangi ukuran image
RUN pip install --no-cache-dir -r requirements.txt
# salin semua direktori proyek ke /app di container. 
COPY . .
# kontainer akan mendengarkan di port 5000 saat runtime dan memberi tau dockert
EXPOSE 5000
# perintah default yang akan dijalankan saat kontainer dimulai
# menjalankan app.py menggunakan interpreter python, untuk menjalankan aplikasi flask ini
CMD ["python", "app.py"]