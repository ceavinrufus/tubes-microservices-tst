# Movie Recommendation Microservice

Made by Ceavin Rufus

## Program Description

_Microservice_ ini berguna untuk memberikan rekomendasi film kepada pengguna berdasarkan sebuah film acuan. _Microservice_ ini menggunakan _machine learning_ untuk menghasilkan daftar film yang sesuai dengan judul film. Selain itu, _microservice_ ini juga berguna untuk memberikan rekomendasi film berdasarkan _mood_ pengguna.

Batasan utama _microservice_ ini adalah hanya memberikan rekomendasi film dari data yang ada dalam sistem, seperti metadata film, tanpa mengintegrasikan data dari sumber eksternal. Selain itu, _mood_ pengguna yang dapat di-_detect_ oleh _microservice_ ini juga masih terbatas.

_Microservice_ ini juga menyediakan fitur mencari film berdasarkan input judul (_search engine_) untuk membantu pengguna mengetahui ID dari film yang akan digunakan menjadi input dari fitur rekomendasi film.

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

### Movies

| Endpoint                 | Method | Summary               | Parameters                                                 | Request Body             | Responses                                                                                    | Security  |
| ------------------------ | ------ | --------------------- | ---------------------------------------------------------- | ------------------------ | -------------------------------------------------------------------------------------------- | --------- |
| /movies/recommendations/ | POST   | Movie Recommendations | mood (query, string) <br> max_amount (query, integer)      |                          | 200: Successful Response (application/json) <br> 422: Validation Error (HTTPValidationError) | JWTBearer |
| /movies/similar/         | GET    | Similar Movies        | movie_id (query, integer) <br> max_amount (query, integer) |                          | 200: Successful Response (application/json) <br> 422: Validation Error (HTTPValidationError) | JWTBearer |
| /movies                  | GET    | Get All Movies        |                                                            |                          | 200: Successful Response (application/json)                                                  |           |
| /movies                  | POST   | Create Movie          |                                                            | Movie (application/json) | 200: Successful Response (application/json) <br> 422: Validation Error (HTTPValidationError) | JWTBearer |
| /movies/{movie_id}       | GET    | Get Movie By Id       | movie_id (path, integer)                                   |                          | 200: Successful Response (application/json) <br> 422: Validation Error (HTTPValidationError) |           |
| /movies/{id}             | PUT    | Update Movie          | id (path, integer)                                         | Movie (application/json) | 200: Successful Response (application/json) <br> 422: Validation Error (HTTPValidationError) | JWTBearer |
| /movies/{id}             | DELETE | Delete Movie          | id (path, integer)                                         |                          | 200: Successful Response (application/json) <br> 422: Validation Error (HTTPValidationError) | JWTBearer |
| /movies/search/          | GET    | Search Movie          | title (query, string)                                      |                          | 200: Successful Response (application/json) <br> 422: Validation Error (HTTPValidationError) |           |

## Schemas

### Genre

| Property | Type    | Description |
| -------- | ------- | ----------- |
| id       | integer | Id          |
| name     | string  | Name        |

### HTTPValidationError

| Property | Type                     | Description |
| -------- | ------------------------ | ----------- |
| detail   | array of ValidationError |             |

### Language

| Property  | Type   | Description |
| --------- | ------ | ----------- |
| iso_639_1 | string | Iso 639 1   |
| name      | string | Name        |

### Movie

| Property          | Type              | Description       |
| ----------------- | ----------------- | ----------------- |
| id                | integer           | Id                |
| title             | string            | Title             |
| genres            | array of Genre    | Genres            |
| original_language | string            | Original Language |
| overview          | string            | Overview          |
| release_date      | date              | Release Date      |
| popularity        | number            | Popularity        |
| runtime           | integer           | Runtime           |
| spoken_languages  | array of Language | Spoken Languages  |
| vote_average      | number            | Vote Average      |

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
| birthdate | date                            | Birthdate   |

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
| birthdate | date                            | Birthdate   |
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
