# bootcamp-1-milestone-0

This project is based on [Devops "Charmander-to-Charmeleon" bootcamp](https://devopzilla.notion.site/DevOps-Charmander-to-Charmeleon-boot-camp-2021-c4a3db54884044f1baee4fa586cdcce8)

Stage 0.1 - Build a simple RESTful CRUD API for a merchant application to manage 2 resources; items and orders.

### Getting Started

  1. [Python](https://www.python.org/downloads/) Version: 3.9+
  2. Clone this repo: 
  ```
  git clone https://github.com/Nood-cs/bootcamp-1-milestone-0.git
  
  cd bootcamp-1-milestone-0
  ```
  3. Create virtualenv and activate it: 
  ``` 
  python -m venv venv
  ```
  Activate on Windows
  ```
  venv\Scripts\activate
  ```
  Activate on macOS/Linux
  ```
  source venv/bin/activate
  ```
   *In case you are using VSCode, you might need to change the ExecutionPolicy to Unrestricted, so that you can run the script Activate.ps1*
  ```
  Set-ExecutionPolicy Unrestricted -scope Process
  ```
   *Then try to activate the venv one more time* 
  
  4. Install dependencies with pip: 
  ```
  pip install -r requirements.txt
  ```
  5. Run the app: 
  ```
  python app.py
  ```
  6. Run tests: 
  ```
  pytest -v
  ```
