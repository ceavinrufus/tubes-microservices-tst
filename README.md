# II3160 Integrated System Technology - Final Project

<p style="font-size: 20px;">Made by Ceavin Rufus De Prayer Purba - 18221162</p>

Example of frontend app that use this API:</br>
https://moodtertainment.netlify.app/

Made using Azure API Management, you can access the service through the following endpoint:</br>
https://tubes-tst-18221162.azure-api.net

- If you want to use **Mood Based Recommendation** microservice
  - Access the service via https://tubes-tst-18221162.azure-api.net/mood-based-recommendation
  - Which is equivalent to accessing it through https://mood-rec-18221162.azurewebsites.net
- If you want to use **Movie Recommendation** microservice
  - Access the service via https://tubes-tst-18221162.azure-api.net/movie-recommendation
  - Which is equivalent to accessing it through https://movie-rec-18221162.azurewebsites.net
- If you want to use **Beverage Recommendation** microservice
  - Access the service via https://tubes-tst-18221162.azure-api.net/beverage-recommendation
  - Which is equivalent to accessing it through https://bevbuddy--c3oinea.thankfulbush-47818fd3.southeastasia.azurecontainerapps.io/

## Requirements

1. Docker
2. Python
3. MongoDB

## How to run locally (using Docker Compose)

1. Rename `.env.example` to `.env`
2. Make sure that Docker daemon already running
3. Make a _virtual environment_ with this command
   ```
   python -m venv venv
   ```
4. Activate virtual environment with this command
   - Windows
     ```
     source venv/Scripts/activate
     ```
   - Mac & Linux
     ```
     source venv/bin/activate
     ```
5. Install required library with this command
   ```
   pip install -r requirements.txt
   ```
6. Use this command below to run the app

   - If using bash terminal, you can just type

     ```
     #!/bin/sh
     ./up.sh
     ```

   - If not, use this command
     ```
     docker-compose up --build --remove-orphans -d
     ```

## API documentation

### Mood Based Recommendation

- Swagger: https://mood-rec-18221162.azurewebsites.net/docs
- Redoc: https://mood-rec-18221162.azurewebsites.net/redoc
- API Contract: https://github.com/ceavinrufus/tubes-microservices-tst/blob/master/mood_based_recommendation/README.md

### Movie Recommendation

- Swagger: https://movie-rec-18221162.azurewebsites.net/docs
- Redoc: https://movie-rec-18221162.azurewebsites.net/redoc
- API Contract: https://github.com/ceavinrufus/tubes-microservices-tst/blob/master/movie_recommendation/README.md

### Beverage Recommendation (External Service)

- Swagger: https://bevbuddy--c3oinea.thankfulbush-47818fd3.southeastasia.azurecontainerapps.io/docs
- Redoc: https://bevbuddy--c3oinea.thankfulbush-47818fd3.southeastasia.azurecontainerapps.io/redoc
- Detail information about this service is available in my friend [@fiknaufalh](https://github.com/fiknaufalh/) repository (https://github.com/fiknaufalh/bevbuddy/)
