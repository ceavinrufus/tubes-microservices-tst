# Tugas Besar TST: Movie Recommendation Microservice Deployment

Made by Ceavin Rufus

## Program Description

Program ini merupakan sebuah microservice yang bertujuan untuk memberikan rekomendasi film kepada pengguna berdasarkan masukan film. Microservice ini akan menerima permintaan dari pengguna dan menggunakan machine learning untuk menghasilkan daftar film yang sesuai. Batasan utama microservice ini adalah hanya memberikan rekomendasi film dari data yang ada dalam sistem, seperti metadata film, tanpa mengintegrasikan data dari sumber eksternal.

Microservice ini juga menyediakan fitur mencari film berdasarkan input judul (search engine) untuk membantu pengguna mengetahui ID dari film yang akan digunakan menjadi input dari fitur rekomendasi film.

## Requirements

1. Docker
2. Python
3. MongoDB

## How to run locally via virtual environment

1. _Rename_ `.env.example` menjadi `.env`
2. Buat _virtual environment_ dengan menggunakan _command_
   ```
   python -m venv venv
   ```
3. Aktivasi _virtual environment_ dengan menggunakan _command_
   - Windows
     ```
     source venv/Scripts/activate
     ```
   - Mac & Linux
     ```
     source venv/bin/activate
     ```
4. _Install library_ yang diperlukan dengan menggunakan _command_
   ```
   pip install -r requirements.txt
   ```
5. Gunakan _command_ di bawah untuk menjalankan app
   ```
   uvicorn app.main:app --host 0.0.0.0 --port 80 --reload
   ```

## How to run locally using Docker

1. _Rename_ `.env.example` menjadi `.env`
2. Pastikan Docker daemon sudah _running_
3. Gunakan _command_ di bawah untuk menjalankan app
   ```
   docker build -t tubes-tst .
   docker run -d --name tubes-tst-container -p 80:80 tubes-tst
   ```

## Notes

- Jika tidak bisa menggunakan `python` pada command line, coba menggunakan `python3`, begitupun juga jika tidak bisa menggunakan `pip`, gunakan `pip3`
