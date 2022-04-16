These are the all the necessary files to create a docker image and a docker container.
The docker image is also available on DockerHub, which you can access with the `docker pull isaacjay/assignment` command.
If the image is being pulled from DockerHub, proceed to create the container from the image.

Open powershell and change the directory to this repository.
Enter `docker-compose up` to build the docker image.
If there is an existing container, open and run it on a browser. The link should look like `http://localhost:5000/`.

If there isn't, create the container from the image using `docker run -it -p 5000 isaacjay/assignment`.
