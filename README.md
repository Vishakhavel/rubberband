# "Storage - An ocean of bits & bytes"
<p align = "center">
 <img src="https://user-images.githubusercontent.com/54572908/151648343-68e9057e-44ee-4003-b829-8aec95707005.png"/>

This codebase is my submission for the hackathon conducted by *Cloudwiry*, titled '**Storage - An ocean of bits & bytes**'.

[![FastAPI](https://img.shields.io/badge/Framework-FastAPI-brightgreen)](https://fastapi.tiangolo.com/)
[![AWS](https://img.shields.io/badge/CSP-AWS-brightgreen)](https://aws.amazon.com/)

## Video Link:
 [Click here](https://youtu.be/txjaamv01zQ) for the video demo, and explanation.
## Architecture:
 <p align = "center">
 <img src ="https://user-images.githubusercontent.com/54572908/151702378-e11a4a12-239e-492d-87df-5075be2e946f.png"/>
 </p>
 
 <p>
 Stack: 
 <ol>
 <li> AWS EFS - Distributed storage disk <//li>
 <li> AWS RDS (postgres) - User data storage </li>
 <li> AWS Elastic Beanstalk - Managed servers, Application Load Balancing </li>
 <li> AWS Route53 - DNS, Routing </li>
 <li> AWS Codepipeline, Cloudwatch - CICD </li>
 <li> FastAPI - Web framework </li>
 </ol>
 </p>

## Description:
In this solution, users can interact with a FastAPI application, which acts as a blob storage system. The core logic of my solution is that an AWS EFS volume, which is automatically mounted to EC2 instances as a part of AWS Elastic Beanstalk environment, will serve as a distributed storage disk. The Beanstalk environment also has an Application Load Balancer. Users from multiple availbility zones can access the same storage system (The EFS volume), even if they are routed to different servers(EC2 Instances) by the Application Load Balancer. An AWS RDS postgres instance stores the usernames, encrypted passwords, names and IDs of the users. 


## Key Features:

- [x] User Account creation/deletion
- [x] User Authentication, Password Encryption and API Protection
- [x] Upload, Rename, Share, Download, Delete file functionalities

## Bonus features:
- [x] Trash, which stores deleted files until emptied, for every user
- [x] Autoscaling, Load Balancing and Distributed file storage
- [x] CICD for faster bug fixes and quicker releases
- [x] File compression


## Installation

This application has been deployed to AWS Beanstalk.


## Instructions:

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
Download this [Postman collection](https://drive.google.com/file/d/1ngA5W9vZWvkGp0QMgqNKU6DrZfguDFzV/view?usp=sharing) file, open it in postman and use it to test the application, after creating the environment and the environment variables as explained in the video. 

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.
Please make sure to update tests as appropriate.
