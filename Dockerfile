# 使用轻量级 Python 3.13 基础镜像（slim 版本）
FROM python:3.13-slim

# 设置工作目录
WORKDIR /app

# 复制依赖文件并安装（先安装依赖可利用 Docker 缓存）
COPY requirements.txt .
# 安装依赖时使用国内镜像源（阿里云）
RUN pip install --no-cache-dir -i https://mirrors.aliyun.com/pypi/simple/ -r requirements.txt

# 或者使用清华大学镜像
# RUN pip install --no-cache-dir -i https://pypi.tuna.tsinghua.edu.cn/simple/ -r requirements.txt


# 复制所有应用代码（包括 jina_search_re.py）
COPY . .

# 清理构建时的临时文件（可选但推荐）
RUN apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# 指定监听端口（根据你的脚本实际监听端口修改）
# 例如：如果脚本监听 45678 端口
EXPOSE 45678

# 启动命令：运行 jina_search.py
CMD ["python", "jina_search_re.py"]
