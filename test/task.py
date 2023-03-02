#pip install --upgrade capsolver
import capsolver
#capsolver.api_key = ""
print("api host",capsolver.api_base)
print("api key",capsolver.api_key)

solution = capsolver.solve({
    "type":             "FunCaptchaTask",
	"websiteURL":       "https://setup.live.com/register",
	"websitePublicKey": "B7D8911C-5CC8-A9A3-35B0-554ACEE604DA",
	"proxy":            "private.residential.proxyrack.net:10004",
})
print(solution)

# solution = capsolver.solve({
#         "type":"ReCaptchaV2TaskProxyLess",
#         "websiteKey":"6Le-wvkSAAAAAPBMRTvw0Q4Muexq9bi0DJwx_mJ-",
#         "websiteURL":"https://www.google.com/recaptcha/api2/demo",
#     })
# print(solution)