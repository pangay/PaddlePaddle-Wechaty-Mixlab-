pip install --upgrade pip
pip install wechaty
pip install ppgan
# 下载模型
hub install animegan_v2_shinkai_33
hub install animegan_v1_hayao_60
hub install animegan_v2_paprika_74
hub install stylepro_artistic

# 设置环境变量
export WECHATY_PUPPET=wechaty-puppet-service
export WECHATY_PUPPET_SERVICE_TOKEN=puppet_padlocal_1320c819baf548c4a20f394443422b70

# 设置使用GPU进行模型预测
export CUDA_VISIBLE_DEVICES=0

# 创建两个保存图片的文件夹
mkdir -p image
mkdir -p image-new

# 运行python文件
python bot_test.py