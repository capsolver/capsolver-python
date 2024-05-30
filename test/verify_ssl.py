import capsolver

print("api host",capsolver.api_base)
print("api key",capsolver.api_key)

capsolver.verify_ssl = False

solution = capsolver.solve({
    "type":             "ReCaptchaV2TaskProxyLess",
    "websiteKey":       "6Le-wvkSAAAAAPBMRTvw0Q4Muexq9bi0DJwx_mJ-",
    "websiteURL":       "https://www.google.com/recaptcha/api2/demo",
})

print(solution)