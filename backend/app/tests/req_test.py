# -*- coding:utf-8 -*-
import requests
import json


def test_request() -> None:
    test_data = {
        "abstract": "铁路应急测绘保障工作贯穿铁路突发事件的预防、应对、处置和恢复的全过程，是铁路应急保障体系的重要内容和基础性工作。铁路系统目前还没有建立铁路应急测绘保障体系，没有形成成熟可行的保障机制，存在着应急测绘预案不完善、地理信息资源储备不足、专业应急测绘保障队伍不健全、突发事件现场资料获取传输及处理不及时等问题。根据铁路应急测绘保障工作的特点，基于近年来相关应急测绘项目应用成果，分析了铁路应急测绘保障的现状和必要性，提出了铁路应急测绘保障体系建设的总体思路，包括铁路应急测绘装备及队伍建设、铁路应急测绘保障预案及工作机制建设、铁路应急测绘保障中心建设和铁路应急测绘保障技术体系建设等内容；并梳理了构建先进的现代铁路工程应急测绘保障技术体系需重点研究的关键性技术。通过建立健全铁路应急测绘保障体系，全面提升铁路行业的应急测绘保障服务能力。"
    }
    data = json.dumps(test_data)
    resp = requests.post("http://127.0.0.1:8080/predict", data=data.encode("utf-8"))
    print(resp.status_code)


if __name__ == "__main__":
    test_request()
