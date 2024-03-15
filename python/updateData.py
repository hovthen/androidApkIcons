# python updateData.py --help

import os, argparse, json, locale, sys
version = '1.0.0'
updateDate = '2024-03-15'

locale.setlocale(locale.LC_ALL, 'zh_CN.UTF-8')

class ChineseHelpFormatter(argparse.HelpFormatter):
  def add_usage(self, usage, actions, groups, prefix=None):
    if prefix is None:
      prefix = '使用方式: '
    return super().add_usage(usage, actions, groups, prefix)

  def add_argument(self, action):
    if action.option_strings:
      action.help = action.help.replace('options:', '选项')
      action.help = action.help.replace('show this help message and exit', '显示帮助信息并退出')
      action.help = action.help.replace('optional arguments', '可选参数')
    else:
      action.help = action.help.replace('positional arguments', '位置参数')
    return super().add_argument(action)

parser = argparse.ArgumentParser(formatter_class=ChineseHelpFormatter, description='图标包数据更新工具')
parser.add_argument('-v', '--version', action='store_true', help='查看当前版本号: -v')
parser.add_argument('-add','--add', dest='JsonDataFilePath', help="补全基础数据：-add 'apksDate.json'")
parser.add_argument('-up','--update', dest='IconsPackageName', help="更新图标包数据: -up 'PrefectOne'")
args = parser.parse_args()

def writeFile(file_path, file_content):
  try:
    file_dir = os.path.dirname(file_path)
    if not os.path.exists(file_dir):
      os.makedirs(file_dir)
    with open(file_path, 'w', encoding='utf-8') as file:
      json.dump(file_content, file, indent=4, sort_keys=True, ensure_ascii=False)
      return True
  except Exception as e:
    print(f"写入 {file_path} 时发生错误: {str(e)}")
    return False

def readFile(file_path):
  try:
    file_dir = os.path.dirname(file_path)
    if not os.path.exists(file_dir):
      print(f"读取 {file_path} 时发生错误: 文件不存在")
      return False
    with open(file_path, 'r', encoding='utf-8') as file:
      return json.load(file)
  except Exception as e:
    print(f"读取 {file_path} 时发生错误: {str(e)}")
    return False

Icons = []
apksData = {}
apksDataNew = {}
apksDataAdd = {}
apksDataNone = {}

# --version
if args.version == True:
  print('图标包数据更新工具\n\n当前版本号:', version, '\n更新日期:', updateDate)
  sys.exit()

# --add
if args.JsonDataFilePath is not None:
  apksDataAddRead = readFile(args.JsonDataFilePath)
  if apksDataAddRead != False:
    apksDataAdd = apksDataAddRead
    print('apksDataAdd:', len(apksDataAdd))

# --update
if args.IconsPackageName is not None:
  IconsPackageName = args.IconsPackageName
else:
  IconsPackageName = input("请输入图标包名称：")


if len(apksDataAdd) > 0 or len(IconsPackageName) > 0:
  apksDataRead = readFile('../data/apks.json')
  if apksDataRead != False:
    apksData = apksDataRead
    print('apksData:', len(apksData))
else:
  sys.exit('输入不能为空，已退出 ...')

if len(apksDataAdd) > 0 :
  print('apksDataAdd:', len(apksDataAdd))
  apksDataNew = {**apksData, **apksDataAdd}
  print('apksDataNew:', len(apksDataNew))
  apksDataNewWrite = writeFile('../data/apksNew.json', apksDataNew)
  print("Write apksDataNew +Add:", apksDataNewWrite)
  apksData = apksDataNew

if len(IconsPackageName) > 0:
  for root, dirs, files in os.walk('../IconsPackageName/'+IconsPackageName):
    for file in files:
      keyFile = os.path.splitext(file)[0]
      keyName = apksData.get(keyFile)
      if keyName is not None:
        Icons.append({'name': keyName, 'file': keyFile})
      else:
        Icons.append({'name': keyFile, 'file': keyFile})
        apksDataNone[keyFile] = keyFile
  print('Icons:', len(Icons))
  IconsWrite = writeFile('../dataPack/'+IconsPackageName+'.json', Icons)
  print("Write Icons:", IconsWrite)


if len(apksDataNone) > 0 :
  print('IconsNameNone:', len(apksDataNone))
  # apksDataNoneWrite = writeFile('../data/apksNone.json', apksDataNone)
  # print("Write apksDataNone:", apksDataNoneWrite)

  apksDataNew = {**apksDataNone, **apksData}
  print('apksDataNew:', len(apksDataNew))
  apksDataNewWrite = writeFile('../data/apksNew.json', apksDataNew)
  print("Write apksDataNew:", apksDataNewWrite)

exit('All Done ..')
