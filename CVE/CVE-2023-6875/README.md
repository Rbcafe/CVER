## What the exploit does
- Places a token that allows you to view mail.
- Finds the admin's username; if it can't find it, then sets "admin" as the default.
- It requests a link to reset the admin's password, which is emailed to the admin.
- Uses the token placed in the first step and examines the mail logs.
- Selects the most recent log, which contains a link to reset the password.
- Resets the password using the link received in the previous step.
- Logs in as the admin.
- Uploads the shell (a file named shell.zip, which contains a shell).

![exploit demo](https://i.imgur.com/RwCinvZ.gif)

## Usage
1. **Clone:** Clone this repository.
2. **Install Golang:** Install the latest Golang from https://go.dev/dl/. For example:
    ```
    wget https://go.dev/dl/go1.21.6.linux-amd64.tar.gz
    tar -C /usr/local -xzf go1.21.6.linux-amd64.tar.gz
    export PATH=$PATH:/usr/local/go/bin
    go version
    ```
2. **Run the exploit:**
   ```
   go run exploit.go https://example.com
   ```

## Author
Exploit is developed by az_AZ
