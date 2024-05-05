# Backend Test Opground - David López Saludes
### DISCLAIMER ###
This code runs with RapidAPI service and it is limited to 50 requests per month. It should be enough to test as in the moment of testing the limitation should have been re-setted to 0. But be weary of the number of requests performed.

Also, in the endpoints `/register` and `detect_job_change` there a variable calledl `job_num`. I created it as to check the previous job of any user in the platform (`job_num: 1`) and then check the current job (`job_num: 0`) so I can test the system to see if the user has changed job. If this is going to be put into production this would be changed in the code itself.  

### How to run the application ###
If it is the first time running the application run the command `make first`, then in order to use the application you can always run (also in the terminal) `make start`. Docker should be open while doing this.

### How to test ###
In order to test the application Postman should be used. The colleciton for running postman can be found in the folder `postman_collection`, this JSON should be imported into Postman in order to run the endpoints.
