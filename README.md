# fetch-data-engineer
Assesment for data engineer summer internship 2023


## Run Locally

Clone the project

```bash
  git clone https://github.com/SINDHUSITA/fetch-data-engineer.git
```
Requires python >3.8

Go to the project directory

```bash
  cd fetch-data-engineer
```
If anaconda is present create a virtual environment

```bash
conda create fetch --name python=3.9
conda active fetch
```

Install dependencies

```bash
  pip install -r requirements.txt
```

Start the server

```bash
  pip install awscli-local
  docker compose up
```
To run program

```bash
python program.py
```

## Sample Output
![Output](https://github.com/SINDHUSITA/fetch-data-engineer/blob/main/output.PNG)

 ## Questions
● How would you deploy this application in production?
To deploy this application in production, one needs to follow these general steps:

Prepare the environment: Ensure the necessary infrastructure and dependencies are in place, such as servers, databases, and libraries.

Build and test the application: Compile the application code and run tests to ensure it works as expected.

Package the application: Package the application code and dependencies into a deployable format using Docker container or a virtual machine image.

Deploy the application: This application can be deployed in production as a microservice in a kubernetes cluster 1and start it.

Monitor and manage the application: Monitor the application for any issues and perform regular maintenance, such as applying updates and scaling resources as needed.

Continuously improve: Continuously monitor the performance and stability of the application and make improvements as needed.

● What other components would you want to add to make this production ready?

Answer: To make this application production ready, one can add the following components:

Load balancer: To distribute incoming traffic across multiple instances of the application and ensure high availability.

Monitoring and logging: To monitor the performance and stability of the application and track any issues. This can include tools for monitoring system metrics, such as CPU usage and memory utilization, as well as tools for logging application-level events and errors.

Backup and recovery: To ensure the application can be quickly restored in the event of a disaster, such as a hardware failure or data loss.

Security: To protect the application from potential threats, such as attacks, unauthorized access, and data breaches. This can include firewalls, SSL certificates, and network security policies.

Scalability: To ensure the application can handle increased load as needed, either by adding more resources or by implementing horizontal scaling with multiple instances of the application.

Continuous integration/continuous deployment (CI/CD): To automate the build, test, and deployment processes, ensuring that updates and improvements can be quickly and easily made to the application.

Disaster recovery plan: To ensure that the application can continue to operate in the event of a disaster, such as a data center outage or network failure.

These components can help make an application more resilient, scalable, and secure in a production environment.

● How can this application scale with a growing dataset.

Answer: Scaling a Python application with a growing dataset requires a combination of different strategies, including:

Database optimization: Optimize the database to handle increasing amounts of data, such as adding indexes, partitioning tables, or using a database optimized for large datasets, like Apache Cassandra or Amazon Redshift.

Caching: Implement caching mechanisms to reduce the amount of data that needs to be retrieved from the database, such as using a cache server like Redis or Memcached.

Horizontal scaling: Add more machines to the application to handle the increased load, either by adding more database servers or by adding more application servers.

Load balancing: Distribute incoming traffic across multiple instances of the application to ensure high availability and prevent a single instance from becoming a bottleneck.

Data compression: Compress data to reduce its size, either in the database or during transmission, to reduce the amount of storage and bandwidth required.

Parallel processing: Use parallel processing to speed up processing of large datasets, such as using the Python multiprocessing module or using tools like Apache Spark or Dask.

● How can PII be recovered later on?

Answer: The PII fields in the data are masked using base64 encoding which can be easily recovered using the decrypt function in the program.py file

● What are the assumptions you made?

Answer: Since, the PII is not password strings here, so assuming that encryption/cryptography is not required. So, I used a simple base64 encoding scheme which is helpful in preserving duplicate values as well for data analysis.
