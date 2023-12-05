# Mood Based Recommendation Microservice

Made by Ceavin Rufus

## Program Description

_Microservice_ ini berguna untuk merekomendasikan berbagai hal sesuai dengan _mood_ pengguna, seperti merekomendasikan film atau minuman yang cocok dengan _mood_. Pengguna dapat memilih dari berbagai kategori _mood_, seperti _happy_, _sad_, _scared_, _neutral_, dan _angry_ untuk merekam perasaan mereka pada waktu tertentu. _Microservice_ akan menyimpan data _mood_ pengguna, dan berdasarkan _mood_ tersebut, dengan menggunakan algoritma khusus, _microservice_ akan merekomendasikan berbagai hal sesuai dengan _mood_ pengguna.

_Microservice_ ini merupakan hasil integrasi dari:

### Movie Recommendation Microservice:

- _Microservice_ ini berguna untuk memberikan rekomendasi film kepada pengguna berdasarkan sebuah film acuan. _Microservice_ ini menggunakan _machine learning_ untuk menghasilkan daftar film yang sesuai dengan judul film. Selain itu, _microservice_ ini juga berguna untuk memberikan rekomendasi film berdasarkan _mood_ pengguna. <a href="https://github.com/ceavinrufus/tubes-microservices-tst/tree/master/movie_recommendation">Lebih lengkap</a>

### Beverage Recommendation Microservice:

- _Microservice_ yang berguna untuk memberikan rekomendasi minuman/beverage dari suatu kafe berdasarkan berat badan, tinggi badan, usia, gender, dan exercise level dari aktivitas mingguan pengguna untuk menentukan minuman dengan kadar nutrisi (kalori, karbohidrat, protein, lemak, kadar gula, kafein) yang sesuai. Selain itu, rekomendasi juga dapat didasarkan pada mood pengguna dan cuaca terkini di lokasi pengguna menggunakan _Microservice_ ini. <a href="https://github.com/fiknaufalh/bevbuddy">Lebih lengkap</a>

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

## API documentation

### Users

| Endpoint        | Method | Summary       | Parameters               | Request Body                 | Responses                                                                         | Security  |
| --------------- | ------ | ------------- | ------------------------ | ---------------------------- | --------------------------------------------------------------------------------- | --------- |
| /users/register | POST   | Register      | key (query, string/null) | UserInDB (application/json)  | 200: Successful Response (Token) <br> 422: Validation Error (HTTPValidationError) |           |
| /users/login    | POST   | Login         |                          | UserLogin (application/json) | 200: Successful Response (Token) <br> 422: Validation Error (HTTPValidationError) |           |
| /users/me       | GET    | Read Users Me |                          |                              | 200: Successful Response (User)                                                   | JWTBearer |

### Moods

| Endpoint                | Method | Summary          | Parameters                                             | Request Body               | Responses                                                                                    | Security  |
| ----------------------- | ------ | ---------------- | ------------------------------------------------------ | -------------------------- | -------------------------------------------------------------------------------------------- | --------- |
| /moods/recommendations/ | POST   | Recommendations  | input (query, string) <br> max_amount (query, integer) |                            | 200: Successful Response (application/json) <br> 422: Validation Error (HTTPValidationError) | JWTBearer |
| /moods                  | GET    | Get All Moods    |                                                        |                            | 200: Successful Response (application/json)                                                  | JWTBearer |
| /moods                  | POST   | Create Mood      |                                                        | MoodReq (application/json) | 200: Successful Response (application/json) <br> 422: Validation Error (HTTPValidationError) | JWTBearer |
| /moods/user/{username}  | GET    | Get User Moods   | username (path, string)                                |                            | 200: Successful Response (application/json) <br> 422: Validation Error (HTTPValidationError) | JWTBearer |
| /moods/{date}           | GET    | Get Mood By Date | date (path, string, date)                              |                            | 200: Successful Response (application/json) <br> 422: Validation Error (HTTPValidationError) | JWTBearer |
| /moods/{datetime}       | PUT    | Update Mood      | datetime (path, string, date-time)                     | MoodReq (application/json) | 200: Successful Response (application/json) <br> 422: Validation Error (HTTPValidationError) | JWTBearer |
|                         | DELETE | Delete Mood      | datetime (path, string, date-time)                     |                            | 200: Successful Response (application/json) <br> 422: Validation Error (HTTPValidationError) | JWTBearer |

## Schemas

### HTTPValidationError

| Property | Type                     | Description |
| -------- | ------------------------ | ----------- |
| detail   | array of ValidationError |             |

### MoodReq

| Property | Type                                                   | Description |
| -------- | ------------------------------------------------------ | ----------- |
| mood     | enum: happy/loved/focus/chill/sad/scared/angry/neutral | Mood        |
| notes    | string                                                 | Notes       |
| datetime | string (format: date-time)                             | Datetime    |

### Token

| Property     | Type   | Description  |
| ------------ | ------ | ------------ |
| access_token | string | Access Token |
| token_type   | string | Token Type   |

### User

| Property  | Type                            | Description |
| --------- | ------------------------------- | ----------- |
| username  | string                          | Username    |
| email     | string                          | Email       |
| full_name | string                          | Full Name   |
| gender    | enum: Male/Female               | Gender      |
| role      | enum: customer/admin/superadmin | Role        |
| weight    | number                          | Weight      |
| height    | number                          | Height      |
| birthdate | string (format: date)           | Birthdate   |

### UserInDB

| Property  | Type                            | Description |
| --------- | ------------------------------- | ----------- |
| username  | string                          | Username    |
| email     | string                          | Email       |
| full_name | string                          | Full Name   |
| gender    | enum: Male/Female               | Gender      |
| role      | enum: customer/admin/superadmin | Role        |
| weight    | number                          | Weight      |
| height    | number                          | Height      |
| birthdate | string (format: date)           | Birthdate   |
| password  | string                          | Password    |

### UserLogin

| Property | Type   | Description |
| -------- | ------ | ----------- |
| username | string | Username    |
| password | string | Password    |

### ValidationError

| Property | Type                         | Description |
| -------- | ---------------------------- | ----------- |
| loc      | array of strings or integers | Location    |
| msg      | string                       | Message     |
| type     | string                       | Error Type  |

## Security

### JWTBearer

- **Type:** HTTP
- **Scheme:** bearer
