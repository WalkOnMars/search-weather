import urllib.request
import json
import requests


def find_city_code(city):
    """
    城市名返回城市代码
    :param city:城市名
    :return: dict
    """
    citys = {}
    with open("city.json", encoding="utf-8") as file:
        city_json = json.load(file)
        for c in city_json:
            if c["city_code"]:
                citys[f'{c["city_name"]}'] = c["city_code"]
        print(city in citys)
        if city in citys:
            return citys[city]
        else:
            return False


def if_has_net():
    """
    :return: 布尔类型
    """
    choice = True
    try:
        urllib.request.urlopen(url="https://www.baidu.com", timeout=5)
    except Exception as e:
        choice = False
        print(f"网络状态{choice}，{e}")

    finally:
        print(f"网络状态{choice}")
        return choice


def get_city_weather(city):
    """
    :param city: 城市名
    :return: 城市天气信息list
    """
    # 判断输入城市是否在city.json
    city_id = find_city_code(city)
    if city_id:
        url = f"http://t.weather.sojson.com/api/weather/city/{find_city_code(city)}"
        # 判断是否连网
        if if_has_net():
            city_weather = json.loads(requests.get(url).text)  # 以utf-8编码对x.read()进行解码，获得字符串类型对象在转对象
            # 是否成功获取数据
            if city_weather["status"] == 200:

                return_json = {}
                c_info = city_weather["cityInfo"]
                data = city_weather["data"]
                c_ytd = data["yesterday"]
                c_td = data["forecast"][0]
                c_tmr = data["forecast"][1]
                c_ht = data["forecast"][2]
                c_dht = data["forecast"][3]
                c_ddht = data["forecast"][4]
                # 城市ip当做文档id
                cityId = {"city_id": c_info["citykey"]}
                # 获取城市天气时间
                get_info_time = {"get_info_time": city_weather["time"]}
                # 城市信息
                return_json['city_info'] = {"city": c_info["city"], "update_time": c_info["updateTime"]}
                # 昨天
                return_json['yesterday'] = {"month": city_weather["date"][4:6], "day": c_ytd["date"], "week": c_ytd["week"],
                             "type": c_ytd["type"], "fx": c_ytd["fx"], "fl": c_ytd["fl"], "notice": c_ytd["notice"],
                             "high": c_ytd["high"], "low": c_ytd["low"], "aqi": c_ytd["aqi"]}
                # 今天
                return_json['today'] = {
                    "shidu": data["shidu"], "pm25": data["pm25"], "pm10": data["pm10"], "quality": data["quality"],
                    "wendu": data["wendu"], "ganmao": data["ganmao"],
                    "month": city_weather["date"][4:6], "day": c_td["date"], "week": c_td["week"],
                    "type": c_td["type"], "fx": c_td["fx"], "fl": c_td["fl"], "notice": c_td["notice"],
                    "high": c_td["high"], "low": c_td["low"], "aqi": c_td["aqi"]
                }
                # 明天
                return_json['tomorrow'] = {
                    "month": city_weather["date"][4:6], "day": c_tmr["date"], "week": c_tmr["week"], "type": c_tmr["type"],
                    "fx": c_tmr["fx"], "fl": c_tmr["fl"], "notice": c_tmr["notice"], "high": c_tmr["high"], "low": c_tmr["low"],
                    "aqi": c_tmr["aqi"]
                }
                # 后天
                return_json['ht'] = {
                    "month": city_weather["date"][4:6], "day": c_ht["date"], "week": c_ht["week"], "type": c_ht["type"],
                    "fx": c_ht["fx"], "fl": c_ht["fl"], "notice": c_ht["notice"], "high": c_ht["high"], "low": c_ht["low"],
                    "aqi": c_ht["aqi"]
                }
                # 大后天
                return_json['dht'] = {
                    "month": city_weather["date"][4:6], "day": c_dht["date"], "week": c_dht["week"], "type": c_dht["type"],
                    "fx": c_dht["fx"], "fl": c_dht["fl"], "notice": c_dht["notice"], "high": c_dht["high"], "low": c_dht["low"],
                    "aqi": c_dht["aqi"]
                }
                # 大大后天
                return_json['ddht'] = {
                    "month": city_weather["date"][4:6], "day": c_ddht["date"], "week": c_ddht["week"], "type": c_ddht["type"],
                    "fx": c_ddht["fx"], "fl": c_ddht["fl"], "notice": c_ddht["notice"], "high": c_ddht["high"], "low": c_ddht["low"],
                    "aqi": c_ddht["aqi"]
                }
                # 判断数据是否存在数据库? 存在:是否最新？（是:返回,否:更新）,否:添加返回，
                return return_json
            else:
                return "服务器正在维护"
        else:
            print("不存在")
            return "网络已断开"
    else:
        return "你输入的城市有误或不再查询范围"


