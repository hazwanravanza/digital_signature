# Tanda Tangan Digital

Aplikasi ini berbasis web dengan menggunakan web server nginx, sehingga sebelum menjalankan layanan ini maka harus install nginx

Cara install nginx
  1. Download di URL ini :
     https://nginx.org/en/download.html
  2. Extract file download ke folder ->  C:\nginx
  3. Rubah Config file : C:\nginx\conf\nginx.conf
     
      Tambahkan dibawah location /:
     
         proxy_pass http://127.0.0.1:80;
     
         proxy_set_header Host $host;
     
         proxy_set_header X-Real-IP $remote_addr;
     
         proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
     
         proxy_set_header X-Forwarded-Proto $scheme;
     

Run Nginx
  C:\nginx\nginx.exe
 

# Kemudian aplikasi web ini menggunakan framework flask dan waitress
1. install flask di cmd dengan perintah:

        pip install flask
  
        pip install flask-restful


2. install waitress dengan perintah:

        pip install waitress


# Jalankan aplikasi web 
untuk menjalankan aplikasi web ini, masuk ke folder aplikasi yang terdapat file appkripto.py
kemudian jalankan perintah:

       waitress-serve --listen=127.0.0.1:80 app:app

