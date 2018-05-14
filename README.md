# 中国行政区划数据

## 区划代码
具体区划代码建议从[http://www.mca.gov.cn/](http://www.mca.gov.cn/)网站下载，在页面中搜索“全国行政区划代码”。

## 矢量地图
地图仅详细至区县级，供网站展示使用。

 - geojson版本路径：`geojson/geojson/*.json`
 - svg版本路径：`svg/svg/*.svg`

## 代码运行
Python版本请确保在3.0以上。

下载依赖库：
```sh
pip install -r requirements.txt
```

更新geojson文件：
```sh
python src/geojson.py
```

更新svg文件：
```sh
python src/svg.py
```