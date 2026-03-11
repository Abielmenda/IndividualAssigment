## Installation

Open a terminal and clone the repository:

git clone https://github.com/Abielmenda/IndividualAssigment.git

Create the compatible environment:

python -m venv venv
source venv/bin/activate

Install all dependencies needed:

pip install -r requirements.txt


## Running with Docker (alternative)
start a terminal and a docker CLI or docker Dektop, check docker

docker --version

Build the Docker image (Warning: if you have bad internet conexion you may run the next comand more than one time if you get a runtime error):

docker build -t paperAnalysis .

Run the experiment:

docker run --rm paperAnalysis          