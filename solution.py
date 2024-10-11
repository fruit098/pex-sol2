#!/usr/bin/env python3.10

# 1. part http server
def server():
    import socketserver
    import threading
    from http.server import SimpleHTTPRequestHandler

    def start_server():
        with socketserver.TCPServer(("", SERVER_PORT), SimpleHTTPRequestHandler) as httpd:
            print(f"Server running at port {SERVER_PORT}")
            httpd.serve_forever()


    # Running server on separete thread so main thread can continue to do other tasks
    server_thread = threading.Thread(target=start_server)
    server_thread.daemon = True
    server_thread.start()

# 2. part http client
def get_response():
    import http.client

    conn = http.client.HTTPConnection("localhost",MITM_PORT)
    # Setting up host, port for CONNECT tunnel that is needed for proxy 
    conn.set_tunnel("localhost",SERVER_PORT)
    conn.request("GET", "/challenge.js")
    response = conn.getresponse()
    response_body = response.read().decode()
    print(f"Response code: {response.status}")
    conn.close()
    return response_body

# 3. part regex
def extract_function_and_get_key(response):
    import re 
    import subprocess

    # Regex for TargetFunc extraction, the most obvious for me was using comments that are enclosing the function
    # if the comments would not be there I would use some function starting, ending parts of code to catch it
    reg = "\/\* .+? function below \*\/[\S\s]+?\/\* end of function .+? \*\/"
    # Adding evaluation of our specific input
    function = re.search(reg, response)[0] + "\n process.stdout.write(TargetFunc('1WjC5GYPs3t2iTRkvH'))"

    # Chose nodejs runtime to process the functions as its faster/robust than any other package
    result = subprocess.run(["node", "-"], input=function, capture_output=True, text=True).stdout
    print(f"Node.js execution output: {result}")
    return result

# 4. part decrypt the secrets
def decrypt(key):
    import base64
    from pyaes import AESModeOfOperationCBC

    ciphertext = base64.b64decode("pYE2lP4m9pkCSGRfSz6IVAGZt2Q4Hboln3tKcWSWe3mAmtB6lFjPKq5rEyA+QhVoqoiF4qq4RATrRvrm3LWf1BdpYnb5jpDJsXdkC3PyFTg=")
    # Ciphertext needs to be split into blocks of 16 bytes for that library
    blocks_of_cipher_text  = [ciphertext[i:i+16] for i in range(0, len(ciphertext), 16)]
    # Key and IV are the same
    aes = AESModeOfOperationCBC(bytes(key,"ascii"), bytes(key, "ascii"))
    result = b""
    for block in blocks_of_cipher_text:
        result += aes.decrypt(block)
    print(result)



if __name__ == "__main__":
    SERVER_PORT = 8888
    MITM_PORT = 8080

    server()
    response = get_response()
    key = extract_function_and_get_key(response)
    decrypt(key)
