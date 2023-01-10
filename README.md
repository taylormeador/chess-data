# chess-data

This is a side project I am undertaking for fun and in order to learn about data engineering tools like Airflow, dbt, Spark, etc.

The diagram below shows the architecture for the project.

![alt-text](https://github.com/taylormeador/chess-data/blob/main/chessdata.drawio.png)

 Although I initially ran Airflow on AWS and used S3 for the data lake, I decided to migrate some things back to a local environment in order to save on costs. A diagram of this setup would simply have a local hard drive as the data lake instead of S3.

The CLI tool can be used by simply building the Docker container and running it. At the time of writing, there is only one real command.
I plan to add more functionality to this so that the project can have some real world use, but I mostly wanted to explore Docker and Airflow, which I used mostly for the ingestion and tranformation of the data into the cloud.