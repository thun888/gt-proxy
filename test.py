import re


def processcookies(cookies):
    result_list = []

    for name, value in cookies.items():
        s = name + '=' + value + ';'
        result_list.append(s)

    result = ''.join(result_list)
    cookies_dict = {cook.split('=')[0]:cook.split('=')[1] for cook in result.split('; ')}
    return cookies_dict

def loadcookies():
    # 打开cookies.json
    s = open('cookies.json', 'r', encoding='utf-8').read()
    pat = re.compile(r'(true,)|(false,)|(null,)|(null)')
    r = pat.sub('"a",', s)
    # 将剪切板内容作为字典输入
    cookie_list = eval(r)

    result_list = []

    for dic in cookie_list:
        s = dic.get('name') + '=' + dic.get('value') + ';'
        print(s)
        result_list.append(s)

    result = ''.join(result_list)
    cookies_dict = {cook.split('=')[0]:cook.split('=')[1] for cook in result.split('; ')}
    return cookies_dict

if __name__ == '__main__':
    # 脱敏
    # cookies = {}
    # print(processcookies(cookies))
    print(loadcookies())