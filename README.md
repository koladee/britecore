# BRITECORE ASSESSMENT
# Feature Request Web App

With this web app users can create feature requests and view the exiting ones as well.

A "feature request" is a request for a new feature sent by a user and it will be added to the software. 


## Approach to Problem Statement
When a new feature request is submitted by a particular client, based on the problem statement that "all the priorities of all other feature requests for that same client should be reordered", the priorities are reorderd by adding 1 to heighest value of priority to replace that of the existing priority that is equal to the newly submitted priority.
Then for the priority of the new request takes its original value.
With this, no priority is repeated.


## How to get Started

The instructions bellow will get this project up and running on a Linux Server 

### Requirements

What things you need to install the software and how to install them

```
Server Side Scripting: Python 3.6+
Server Framework: Flask (Python web framework)
ORM: Sql-Alchemy
```

`Set Up a Virtual Environment`


`pip install requirement.txt`

`from the root directory from the project run the following command`

`python britecore`

`britecore in this regards is the package name for the web app`

```
You can now start submitting request from the UI by opening the below URL on a browser
```

`URL: ` <http://localhost:5000> 

```
You are good to go
```


## Live Version

`To setup on a live server follow this link:`
* [SEVER SETUP](https://www.datasciencebytes.com/bytes/2015/02/24/running-a-flask-app-on-aws-ec2/) - deployment with apache
* Then setup HTTP(S) load balancing to serve over port 443

`For live testing, visit`
<https://spibes.com/>

## Built With

* [Flask](http://flask.pocoo.org/) - Python web framework used
* [GCP (Compute Engine)](https://console.cloud.google.com/) - Hosting Platform
* [Jquery](https://jquery.com/) - Javascript framework

