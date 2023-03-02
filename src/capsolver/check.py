
from capsolver.error import CapsolverError


SUPPORT_TASK_TYPE = [
    "HCaptchaTask",
    "HCaptchaTaskProxyLess",
    "HCaptchaEnterpriseTask",
    "HCaptchaEnterpriseTaskProxyLess",

    "FunCaptchaTask",
    "FunCaptchaTaskProxyLess",

    "GeeTestTask",
    "GeeTestTaskProxyLess",

    "ReCaptchaV2Task",
    "ReCaptchaV2TaskProxyLess",

    "ReCaptchaV2EnterpriseTaskProxyLess",
    "ReCaptchaV2EnterpriseTask",

    "ReCaptchaV3Task",
    "ReCaptchaV3TaskProxyLess",

    "MtCaptchaTask",
    "MtCaptchaTaskProxyLess",

    "DataDomeSliderTask",

    "AntiCloudflareTask",

    "AntiKasadaTask",

    "AntiAkamaiBMPTask",

    "ImageToTextTask",

    "HCaptchaClassification",

    "FunCaptchaClassification",

    "AwsWafClassification",

]


def captcha_basic_check(params:dict):
    params_keys = params.keys()
    if "websiteURL" not in params_keys:
        return CapsolverError("need websiteURL param")
    if "websiteKey" not in params_keys:
        return CapsolverError("need websiteKey param")
    return None

def check_recaptcha(params:dict):

    return captcha_basic_check(params)


def check_hcaptcha(params):
    r = captcha_basic_check(params)
    if not r:
        return r
    return None

def check_funcaptcha(params:dict):
    params_keys = params.keys()
    if "websiteURL" not in params_keys:
        return CapsolverError("need websiteURL param")
    if "websitePublicKey" not in params_keys:
        return CapsolverError("need websitePublicKey param")
    return None

def check_mtcaptcha(params:dict):
    r = captcha_basic_check(params)
    if not r:
        return r
    return None


def _format_all_task_type():
    list_types = []
    for i in range(len(SUPPORT_TASK_TYPE)):
        list_types.append(f"{i}. {SUPPORT_TASK_TYPE[i]}")
    return "\n".join(list_types)


def _check_params(params:dict):
    captcha_type:str = params["type"]
    if params["type"] not in SUPPORT_TASK_TYPE:
        return CapsolverError("unsupport TaskType" +captcha_type+"\n support types as follow \n"+_format_all_task_type()) 
    captcha_type = captcha_type.lower()
    if "recaptcha" in captcha_type:
        return check_recaptcha(params)
    if "hcaptcha" in captcha_type:
        return check_hcaptcha(params)
    if "funcaptcha" in captcha_type:
        return check_funcaptcha(params)
    if "mtcaptcha" in captcha_type:
        return captcha_basic_check()

    if "geetesttask" in captcha_type:
        if "gt" not in params.keys():
            return CapsolverError(captcha_type+" need gt param")
        if "challenge" not in params.keys():
            return CapsolverError(captcha_type+" need challenge param")

    if "datadom" in captcha_type:
        if "proxy" not in params.keys():
            return CapsolverError(captcha_type+" need proxy param")
        if "userAgent" not in params.keys():
            return CapsolverError(captcha_type+" need userAgent")

    if "anticloudflare" in captcha_type:
        if "metadata" not in params.keys():
            return CapsolverError(captcha_type+" need metadata param")

    if "antikasada" in captcha_type:
        if "pageURL" not in params.keys():
            return CapsolverError(captcha_type+" need pageURL param")
        if "proxy"  not in params.keys():
            return CapsolverError(captcha_type+" need proxy param")

    if "antiakamaibmp" in captcha_type:
        if "packageName" not in params.keys():
            return CapsolverError(captcha_type+" need packageName param")

    
