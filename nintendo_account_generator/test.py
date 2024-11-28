# pip3 install selenium-wire
import seleniumwire.undetected_chromedriver as uc
from selenium.webdriver.common.by import By

# define your proxy credentials
proxy_username = "<YOUR_USERNAME>"
proxy_password = "<YOUR_PASSWORD>"
proxy_host = "<PROXY_IP_ADDRESS>"
proxy_port = "<PROXY_PORT>"

# form the proxy address
proxy_address = f"http://{proxy_username}:{proxy_password}@{proxy_host}:{proxy_port}"

# add the proxy address to proxy options
proxy_options = {
    "proxy": {
        "http": proxy_address,
        "https": proxy_address,
    }
}

if __name__ == "__main__":
    # set Chrome options
    options = uc.ChromeOptions()

    # run Chrome in headless mode
    options.headless = True

    # create a Chrome instance with the proxy options
    driver = uc.Chrome(
        seleniumwire_options=proxy_options,
        options=options,
    )

    # # visit the test URL to check your proxy IP
    driver.get("https://httpbin.io/ip")

    # select the body tag containing the current IP address
    ip_address = driver.find_element(By.TAG_NAME, "body").text

    # print your current IP
    print(ip_address)
