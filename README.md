# 介绍 (Introduction)
一键 下载 中国 古典文学 转为 kindle mobi 文件

如果想放上 封面图片，请把图片放在 template/cover.jpg， 并且 uncomment 
#self.save_cover()

## 安装 calibre (install ebook-convert) 
https://calibre-ebook.com/download_linux

## 安装 python 环境 (python environment setup)
python -m venv venv

source venv/bin/activate

pip install requirements.txt

## 运行 下载程序 (Commands to download)
python download_shiji.py  # 史记
python download_friti.py  # 丰乳肥臀
python download_jpm.py    # 金瓶梅
python download_xyj.py    # 西游记
python download_zztj.py   # 资治通鉴
python download_zzyz.py   # 庄子译注


