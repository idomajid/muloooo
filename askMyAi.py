import sys, requests, json, re, threading
from time import sleep

def loading_animation():
    animation = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
    i = 0
    while not stop_loading:
        sys.stdout.write(f"\rLoading {animation[i % len(animation)]}")
        sys.stdout.flush()
        sleep(0.1)
        i += 1
    sys.stdout.write("\r" + " " * 20 + "\r")  # Clear loading text


def main():
    global stop_loading

    if(sys.argv[1] == "-v"):
        print("Version: deepseek-r1:1.5b")
        sys.exit(0)

    if(len(sys.argv) < 2):
        print("Usage: askMyAi <prompt> true/false")
        print("true: apply thinking mode")

        sys.exit(1)
    
    prompt = sys.argv[1]


    url = 'http://localhost:11434/api/generate'
    headers = {'Content-Type': 'application/json'}
    body = {
            "model": "deepseek-r1:1.5b",
            "prompt": prompt,
            "stream": False
            }
    

    # Start loading animation
    stop_loading = False
    loading_thread = threading.Thread(target=loading_animation)
    loading_thread.start()
    
    response = requests.post(url, headers=headers, data=json.dumps(body))

     # Stop loading animation
    stop_loading = True
    loading_thread.join()

    if response.status_code != 200:
        print(f"Error: {response.status_code} - {response.text}")
        sys.exit(1)


    json_response = response.json()
    model_value = json_response.get("response")


    # Remove <think> tags and their content
    thinking_mode = re.sub(r'<think>.*?</think>', '', model_value, flags=re.DOTALL)

    # Determine if cleaning should be applied (default is False)
    apply_cleaning = len(sys.argv) > 2 and sys.argv[2].lower() == "true"
    final_response = thinking_mode if model_value  else  apply_cleaning

    # type out the response
    speedType = 0.03
    for char in final_response:
        sleep(0.03)
        sys.stdout.write(char)
        sys.stdout.flush()

    print()


if __name__ == "__main__":
    main()

   



 
