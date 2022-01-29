# Distributed File Storage system.

![☁️_A_Storage_Solution_☁️](https://user-images.githubusercontent.com/54572908/151648343-68e9057e-44ee-4003-b829-8aec95707005.png)

This codebase is my submission for the hackathon conducted by *Cloudwiry*, titled '**Storage - An ocean of bits & bytes**'

This application has been deployed to **AWS**.

## Architecture
<img width="863" alt="Screen Shot 2022-01-29 at 11 39 53 AM" src="https://user-images.githubusercontent.com/54572908/151649919-c3a200a8-11dd-4b49-b12d-e484da734572.png">


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

4. Create a virtual environment
```bash
python3 -m venv <your-venv-name>
```

5. Activate the virtual environment
```bash
source <your-venv-name>/bin/activate
```
6. Install dependencies
```bash
pip3 install -r requirements.txt
```
7. Start the server
```bash
uvicorn application:app --reload
```
Your terminal should now look like this:

[![asciicast](https://asciinema.org/a/X1MtHZ2kOawAJF6mICk3Nv1iJ.svg)](https://asciinema.org/a/X1MtHZ2kOawAJF6mICk3Nv1iJ)

## Usage
Create a new Postman environment and create these variables.
Open the Postman collection file "collection_cloudwiry" and use it to test the environment.

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.
