# Distributed File Storage system.

![☁️_A_Storage_Solution_☁️](https://user-images.githubusercontent.com/54572908/151648343-68e9057e-44ee-4003-b829-8aec95707005.png)

This codebase is my submission for the hackathon conducted by *Cloudwiry*, titled '**Storage - An ocean of bits & bytes**'

[![FastAPI](https://img.shields.io/badge/Framework-FastAPI-brightgreen)](https://fastapi.tiangolo.com/)
[![AWS](https://img.shields.io/badge/CSP-AWS-brightgreen)](https://aws.amazon.com/)


## Architecture
<!-- <img width="863" alt="System Architecture" src="https://user-images.githubusercontent.com/54572908/151702378-e11a4a12-239e-492d-87df-5075be2e946f.png">
 -->
![image](https://user-images.githubusercontent.com/54572908/151702378-e11a4a12-239e-492d-87df-5075be2e946f.png)

## Installation

This application has been deployed to AWS Beanstalk. Here is the deployed URL:
[Cloudwiry Application](http://cloudwiry-backend-fastapi.ap-south-1.elasticbeanstalk.com/docs) 



All you need to do is download the postman collection file and start testing out the APIs. However, if you feel the need to run the server locally:
1. Clone this repository
```bash
git clone https://github.com/Vishakhavel/file-management-system.git
```
2. Move into the project directory 
```bash
cd file-management-system
```
3. Create a virtual environment
```bash
python3 -m venv <your-venv-name>
```
4. Activate the virtual environment
```bash
source <your-venv-name>/bin/activate
```
5. Install dependencies
```bash
pip3 install -r requirements.txt
```
6. Start the server
```bash
uvicorn application:app --reload
```

## Usage
Create a new Postman environment and create these variables.
Download this [Postman collection](https://drive.google.com/file/d/1ngA5W9vZWvkGp0QMgqNKU6DrZfguDFzV/view?usp=sharing) file "collection_cloudwiry" and use it to test the environment.

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.
