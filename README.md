
# Pex reversing challenge 
This is my solution for reversing challenge. Firstly, I wanted to do in more robust way with better engineering practises such as separating the code into multiple files, better exception handling, more versatile. However, I decided to keep it simple, short and do it in one python script with minimum requirements possible. I tried to write code self-explanatory and added comments where necessary.
The only needed library is for AES encryption, which is `pyaes`. The exact version is in requirements.txt. You can install it with `pip install -r requirements.txt`. The server port is `8888` and MITM proxy has to be running on `8080`.

If you would like to see more robust version in golang, please let me know and I will prepare it but for the sake of simplicity, I did it in python.

Files: 
- solution.py : The solution for the challenge
- screenshots: The screenshots of MITM proxy and the working solution
- requirements.txt: The requirements file for the solution
- challenge.js : The original challenge file that is hosted
