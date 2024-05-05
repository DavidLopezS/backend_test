# Backend Test Opground - David López Saludes

### Challenges, decisions and compromises ###
- Deciding to use RapidAPI was a big decision, as LinkedIn's API posed some problems, due to having to create a LinkedIn page in order to obtain the API Token.
- Decided to test the service by harcoding from Request the job that will be fetching. Be it, when you register your current job will be saved into the db, thus I decided to harcode that when you register the previous job is saved and then check if it is the same regarding the current one. That was made in order to check the correct functionality of the app.
- Fetching the job when registering, thus it is already saved in the db and there is no need to fetch it afterwards.
- Using Makefile in order to improve the execution, also helps with Docker use.
- Deciding to divide the code in different scripts, thus keeping it more clean, understandable and robust.
- try/except system use, thus catching errors much faster.

### Improvements ###
- The code is far from being over, though it might pose a correct solution for a ticket with all the structure already built. 
- The most important improvement would be to host the data base in a cloud service so it would be properly saved and stored. Also, it would be appropiate to make the `detect_job_changes` a method that is called temporarily by a cronjob, thus checing for job changes every X time.
- It would also be a hughe leap forward to use the proper LinkedIn API instead of RapidAPI (or pay the proper subscription for infinite requests).
- Code-wise I'd merge the `UserProfile` and `EmailBody`classes, but due to lack of time I left them as is, but as they share almost the same fields (except one) it would make sense to just use one instead of two.
- Encrypting the API TOKEN would also be a must, maybe using 3rd party services like One Password to store them. 
- Would also improve the validators to be more discriminatory against possible fake URLs and Emails.

### For production ###
By all means, this application is not ready to be used for production. It would need to have a proper db, better error handling and all the improvements mentioned previously.
But if only the code should be uploaded to production, the main thing to be taken into account is the `job_num` variable in the request, which should be removed.
Besides this, maybe some improvements in the error handling.
