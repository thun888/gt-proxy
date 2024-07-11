import ipaddress
import ipdb
db = ipdb.City(".\ipdb.ipdb")

def anonymize_ip(ip):
    """
    这个函数接收一个IP地址作为输入，返回一个匿名化的IP地址。对于IPv4地址，它将第二和第三个字段替换为"*"；对于IPv6地址，它将第二到倒数第二个字段替换为"*"。

    参数:
    ip (str): 输入的IP地址。

    返回:
    str: 匿名化的IP地址。如果输入的IP地址无效，将返回"无效的IP地址"。

    示例:
    >>> anonymize_ip('192.168.1.1')
    '192.*.*.1'

    >>> anonymize_ip('2001:0db8:85a3:0000:0000:8a2e:0370:7334')
    '2001:*:*:*:*:*:*:7334'
    """
    try:
        # 将输入转换为IP地址对象
        ip_obj = ipaddress.ip_address(ip)

        # 对IPv4和IPv6进行不同的处理
        if ip_obj.version == 4:
            # 将第二和第三个字段替换为"*"
            anonymized_ip = ".".join([ip.split(".")[0], "*", "*", ip.split(".")[3]])
        else:
            # 将第二到倒数第二个字段替换为"*"
            fields = ip.split(":")
            anonymized_ip = ":".join([fields[0]] + ["*"] * (len(fields) - 2) + [fields[-1]])

        return anonymized_ip
    except ValueError:
        return "无效的IP地址"
    
def get_ip_region(ip):
    """
    根据给定的IP地址，获取其所在的国家和城市信息。

    参数:
    ip (str): 需要查询的IP地址。

    返回:
    str: 返回一个字符串，包含IP地址所在的国家和城市信息。如果IP地址是IPv6或者无法找到对应的地理位置，将返回'未知'。

    示例:
    >>> get_ip_region('123.45.67.89')
    '中国，上海市'
    """
    ip_obj = ipaddress.ip_address(ip)
    if ip_obj.version == 4:
        ipinfo=db.find_map(ip, "CN")
        country=ipinfo["country_name"]
        city= ipinfo["region_name"]+"，"+ipinfo["city_name"]
    else:
        country=""
        city="未知"
    return country+city