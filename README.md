# medical-care-app-repo

## Instructions 
1. install **python** from [here](https://www.python.org/downloads/)
2. open terminal/cmd and navigate to directory.
3. clone this repo
4. then navigate to the cloned directory using 
    ```
    cd medical-care-app-repo
    ```

5. if using **mac os** or **linux** then copy the following code and past it in terminal
    ```
    python3 -m venv venv
    source venv/bin/activate
    ```
6. if using **windows** then copy the following code and past it in cmd
    ```
    python -m venv venv

    venv/Scripts/activate.bat
    ```
    
7. for **installing dependencies** hen copy the following code
    ```
    pip3 -r requirements.txt
    ```

8. goto [Google Firebase](https://firebase.google.com/) and create a project.
9. goto **project setteng**, in prject setting goto **service account** scroll click on **generate new private key**.
10. open downloaded file, copy contents and past it into **serviceAccount.json** file.
11. open .env file.
    a. goto firebase project goto **project setting** copy **web api key** and past it infront of **FIREBASE_WEB_API_KEY** in place of *.
    b. Enter your email infront of **GMAIL** inplace of *.
    c. enter your emal infront of **PASSWORD** in place of *.
 
12. finally write to run web app write in terminal/cmd:
    ```
    flask run --host 0.0.0.0
    ```

13. firt link will is used to access web app in local machine
14. the second link is used to access web in local network
15. if you want to access this app globally for short time then install **ngrok** and copy the following command in past it terminal or cmd:
    ```
      ngrok http 5000
    ```
16. copy the link and share it.
17. smile 🙂.
