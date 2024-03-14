## Project Title
DS Bulksms Simulation

## About the project
This project is a simulation of sending sms in bulk. An example could be sending sms to every student in University of Oulu. Let us imagine a scenario having certain credit with us and on each sms sent, a credit of 0.1 will be deducted.Since sending sms and getting delivery reports can be resource intensive so we decided to seperate out components to microservices.  Thus, we separated services with separate databases and separate webservers, but we kept redis common between them. We aim to demonstrate communication between the services and synchronization between the services. 

## Implementated components:
Here we have 3 nodes, each node has a different api server. All the nodes can co exist independently. Two of the nodes acts as client-server while one acts as a RPC server.

![alt text](image.png)



Node 1: webapi
Webapi has a separate database with table that has credit i.e, workspace

Node 2: Salesapi 
Salesapi has a separate database with table bulksms and bulksms_info.
Node 3: rpc server
This node has an implementation of gRPC and the stubs 


Since, our primary focus is to demonstrate communication between distributed system. We attempted to demonstrate various ways of message exchange between them, we implemented the following:

JobQueue: We implemented background workers as general_worker and sales_worker with job queues to communicate between them.
gRPC: We implemented gRPC with protos and buffs that would fetch the available credit with get_workspace_credit function. This rpc communication can be carried out by both webapi and salesapi nodes.
pub/sub: We implemented a pub/sub architecture using redis for subscribing and publishing. We subscribed into a topic named `workspace_credit` and listening to that topic from websocket we got the credit available.


Since, both the servers webapi and salesapi could accept and transmit messages as long as they had resources on them. However, the read/write operation on the database seemed to be inferior. The sms sending task would be initiated by salesapi via two rest apis `create` and `run`. `create` would create a bulksms campaign ready to run. Whereas `run` would cause the bulksms campaign to run and send sms to the contacts reading from the uploaded csv file. Then salesapi will get response callback to each and every message to the contacts as queued->sent/failed->delivered->undelivered. The main challenge was to update 


## Built with
- **Python**: A high-level programming language used for developing various components of the system due to its simplicity, readability, and extensive library support.

- **Starlette**: A lightweight ASGI framework used for building high-performance asynchronous web applications and APIs. It was used for handling WebSocket connections and routing.

- **asyncio**: A library in Python used for writing asynchronous code. It was used for managing asynchronous tasks such as handling WebSocket connections and sending messages asynchronously.

- **PostgreSQL**: A powerful open-source relational database management system used for storing and managing data. It was used for persisting data related to contacts, SMS campaigns, and other relevant information.

- **Redis**: An in-memory data structure store used as a database, cache, and message broker. It was used for caching data and possibly for queuing tasks asynchronously.

- **Docker**: A platform for developing, shipping, and running applications in containers. It was used for containerizing and deploying the microservices and other components of the system.

- **gRPC**: A high-performance RPC (Remote Procedure Call) framework developed by Google. It was mentioned in the context of communicating between microservices.

- **WebSocket**: A communication protocol that provides full-duplex communication channels over a single TCP connection. It was used for real-time communication between clients and the server.

- **KrispBroadcast**: A custom broadcast mechanism used for handling pub/sub communication. It facilitated the distribution of messages to WebSocket clients subscribed to specific topics.

- **JobQueue**: A mechanism used for queuing and processing background tasks asynchronously. It was used for processing tasks such as sending bulk SMS campaigns in the background.

- **Matplotlib**: A plotting library for Python used for creating static, animated, and interactive visualizations. It was suggested for generating graphical analyses of system stats collected during testing.

## Getting Started
This below is the mechanism for setting up project locally


## Install Python
### Windows:
1. **Download Python:**
    - Visit the official Python website at [﻿python.org](https://www.python.org/) .
    - Navigate to the "Downloads" section.
    - Download the latest version of Python for Windows.
2. **Run the Installer:**
    - Run the downloaded installer.
    - Check the box that says "Add Python to PATH" during installation.
3. **Verify Installation:**
    - Open a command prompt and type: 
```
python3 --version
```
### Linux:
1. **Install Python:**
    - Python is often pre-installed on Linux. To install or update Python, use your package manager:
```
sudo apt update
sudo apt install python3
```
1. **Verify Installation:**
    - Open a terminal and type:
```
python3 --version
```
## Install and Activate Virtual Environment
### Windows:
1. **Open a Command Prompt:**
    - Open a command prompt or PowerShell.
2. **Install **`**virtualenv:**` 
```
pip install virtualenv
```
**Create a Virtual Environment:**

- Navigate to your project directory.
- Create a virtual environment by running:
```
python -m venv venv
```
**Activate the Virtual Environment:**

- Activate the virtual environment:
```
  .\venv\Scripts\activate
```
### Linux:
1. **Open a Terminal:**
    - Open a terminal.
2. **Install **`**virtualenv:**` 
```
sudo apt install python3-venv
```
**Create a Virtual Environment:**

- Navigate to your project directory.
- Create a virtual environment by running:
```
python3 -m venv venv
```
**Activate the Virtual Environment:**

- Activate the virtual environment:
```
source venv/bin/acivate
```
## Deactivate Virtual Environment
To deactivate the virtual environment, simply run:

### Windows and Linux:
```bash
deactivate
```
## Installing requirements
```
pip install -r requirements.txt
```



## Postgres Installation

### Windows

1. Download the PostgreSQL installer from the [official website](https://www.postgresql.org/download/windows/).
2. Run the installer and follow the on-screen instructions.
3. During installation, you'll be prompted to set a password for the default `postgres` user.

### Linux

1. Install PostgreSQL using your distribution's package manager. For example, on Ubuntu, you can run:
```
sudo apt update
sudo apt install postgresql postgresql-contrib
```

### macOS

1. Install PostgreSQL using Homebrew. Run the following command in your terminal:
```
brew install postgresql
```

## Configuring database
1. After installing PostgreSQL, you can access the PostgreSQL command-line interface (CLI) using the following command:
```
psql -U postgres
```

2. Once you are in the PostgreSQL CLI, you can create and setup a  new database using the following SQL command:
```
CREATE DATABASE mydatabase;
CREATE USER myuser WITH PASSWORD 'mypassword';
GRANT ALL PRIVILEGES ON DATABASE mydatabase TO myuser;
```

## Accessing PostgreSQL

### Windows

- You can access PostgreSQL using the pgAdmin tool, which is installed along with PostgreSQL on Windows.

### Linux and macOS

- Access PostgreSQL using the `psql` command-line tool:
```
psql -U myuser -d mydatabase -h localhost -p 5432
```

## Docker orchestration
We can also setup the database and redis using docker 
```
docker-compose -f webapi/docker-compose.yaml up -d
```

## Migrating the database
And then running alembic commands as
```
cd bulksms/
alembic upgrade heads
```
This will create tables bulksms, bulksms_info on database salesdb 


```
cd workspace/
alembic upgrade heads
```
This will create table workspace on database ds


## Running the backend server
**Run the Application:**
### Webapi:

```
python console.py webapi serve
```
- This will serve the webapi on  [﻿http://127.0.0.1:8000/](http://127.0.0.1:8000/) or [﻿http://localhost:8000/](http://localhost:8000/) .
- You should see the webapi application running.
- Webapi uses database ds running on port 5432


### Salesapi:

```
python console.py salesapi serve
```
- This will serve the salesapi on  [﻿http://127.0.0.1:8002/](http://127.0.0.1:8002/) or [﻿http://localhost:8002/](http://localhost:8002/) .
- You should see the salesapi application running.
- Salesapi uses database salesdb running on port 5433.

### RPC server:

```
python console.py rpc serve
```
- This will serve the rpc on  [﻿http://127.0.0.1:8003/](http://127.0.0.1:8003/) or [﻿http://localhost:8003/](http://localhost:8003/) .
- You should see the rpc application running.
- This is an implementation of gRPC


### Queue worker:

```
arq webapi.webapi.worker_swarm.general_worker.WorkerSettings
```
- This will serve the redis Jobqueue for webapi

```
arq salesapi.salesapi.worker_swarm.sales_worker.WorkerSettings
```
- This will serve the redis Jobqueue for salesapi
