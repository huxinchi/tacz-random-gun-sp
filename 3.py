#发gun的数量
gunsrools:int=1
#每个gun几发弹药
ammorools:int=300
#每把枪发几个配件
attachmentsrools:int=10
#玩家的名字的列表
pls:list=list()
#是否生成为数据包,不生成数据包的结果文件保存在当前目录
spdatapack=True
#(只在生成数据包时启用)数据包生成的位置
sppath=""
#(只在生成数据包时启用)mc的版本(x.x.x如1.20.1)
mcver=""
#额外执行的命令(当前目录下的addcommands.mcfunction,在发放后执行)
addconnamds=False
#重要配置，tacz文件的位置，用来读取枪包
zipfiledir:str=""
#快速配置，只需要输入你版本的具体存档文件夹的位置就可以快速配置除addconnamds,pls,attachmentsrools,ammorools,gunsrools的内容
qsms=False
qsmspath=""

'''
说明:
默认会把当前目录下的save.json作为缓存文件，不存在会重新扫描枪包数据并且缓存进这个文件夹,如果你更新了枪包数据请删除这个文件(可以使用sha-256检测文件变化后自动删除文件)
默认所有在枪包目录下的.zip后缀的文件和文件夹作为枪包
如果程序非正常退出可能无法删除枪包文件夹下的temp文件夹，考虑手动删除，程序启动时自动删除
'''





































import zipfile
import os
import json
breakpoint()
if qsms is True:
    print("快速配置开始，将覆盖一些配置\n配置枪包文件夹")
    zipfiledir=os.path.join(qsmspath,"..","..","tacz")
    #获取上一层下的tacz文件夹
    zipfiledir=os.path.normpath(zipfiledir)
    #防止有..的路径不兼容，直接标准化一下
    print("配置数据包生成")
    addconnamds=False
    spdatapack=True
    sppath=os.join(qsmspath,"datapacks")
    print("获取mc版本")#读json,我不确定能不能行
    for i in os.listdir(os.path.join(qsmspath,"..","..")):
        if i.endswith(".json"):
            with open(os.path.join(qsmspath,"..","..",i))as f:
                try:
                    vsdatajson=json.load(f)
                    mcver=vsdatajson["patches"][0]["version"]
                    #尝试读取这个文件的["patches"][0]["version"]
                    break
                except:
                    pass

try:
    #因为tacz的json文件有注释，只能使用不标准的json模块
    import json5
except ModuleNotFoundError:
    os.system("pip install json5")
#goto的准备,把标签映射到行号
labellist={}
with open(os.path.abspath(__file__),"r",encoding="utf-8") as f:
    #打开本文件
    for linenum,line in enumerate(f,1):
        #获取当前行号和行的内容
        dqline=line.strip()
        if dqline.startswith("#label "):
            #如果当前行是标签
            labellist[line[7:len(line)-1]]=linenum
            #就把当前行的行号存到当前行描述的标签内容
del dqline
del linenum
del line
#释放
def gotostr(label:str)->list:
    return ["n",f"j {labellist[label]}","c"]

nogoto:int=0
try:
    breakpoint(commands=gotostr("gototest"))
    nogoto:int=1
except TypeError:
    nogoto:int=1
#label gototest
if nogoto == 1:
    print("你无法使用goto,可能是因为你python版本低于3.14,无法缓存结果")
else:
    print("goto测试完成,你支持goto")
nosave:int=0

import shutil

def mover(src:str, dst:str)->str:
    """
    移动文件或目录到目标位置，支持目标目录存在时的内容合并

    参数:
        src (str): 源文件/目录路径
        dst (str): 目标路径

    返回:
        bool: 操作是否成功
    """
    try:
        # 检查源路径是否存在
        if not os.path.exists(src):
            raise FileNotFoundError(f"源路径不存在: {src}")

        # 如果目标是已存在的目录
        if os.path.isdir(dst):
            dst_path = os.path.join(dst, os.path.basename(src))

            # 如果是文件且目标文件已存在
            if os.path.isfile(src) and os.path.exists(dst_path):
                # 这里选择覆盖，可根据需求修改为跳过或重命名
                os.remove(dst_path)
                shutil.move(src, dst)

            # 如果是目录且目标目录已存在
            elif os.path.isdir(src) and os.path.exists(dst_path):
                # 递归合并目录内容
                for item in os.listdir(src):
                    src_item = os.path.join(src, item)
                    mover(src_item, dst_path)
                # 删除空源目录
                os.rmdir(src)

            else:
                shutil.move(src, dst)

        # 目标不存在或不是目录
        else:
            # 确保目标父目录存在
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            shutil.move(src, dst)

        return True

    except Exception as e:
        print(f"移动失败: {e}")
        return False











import random

random.seed()
class gun():
    #gunid就是gunid,ammo指可使用的弹药，fire_mode指开火模式,allow_attachments是一个list,装着所有可以使用的配件
    def __init__(self,gunid:str=None,ammo:str=None,fire_mode:str=None,allow_attachmentsid:list[str]=list())->None:
        self.gunid:str=gunid
        self.ammo:str=ammo
        self.fire_mode:str=fire_mode
        self.allow_attachmentsid:list[str]=allow_attachmentsid
    def to_dict(self) -> dict:
        """将对象转换为字典"""
        return {
            'gunid': self.gunid,
            'ammo': self.ammo,
            'fire_mode': self.fire_mode,
            'allow_attachmentsid': self.allow_attachmentsid
        }
    @classmethod
    def from_dict(cls, data: dict):
        """从字典创建对象"""
        return cls(
            gunid=data.get('gunid'),
            ammo=data.get('ammo'),
            fire_mode=data.get('fire_mode'),
            allow_attachmentsid=data.get('allow_attachmentsid', [])
        )
def serialize_gun_list(guns: list[gun]) -> str:
    """序列化Gun对象列表为JSON字符串"""
    return json.dumps([gun.to_dict() for gun in guns],indent=4,ensure_ascii=False)

def deserialize_gun_list(json_str: str) -> list[gun]:
    """从JSON字符串反序列化为Gun对象列表"""
    return [gun.from_dict(gun_dict) for gun_dict in json.loads(json_str)]

if nogoto == 0 and os.path.exists("save.json"):
    print("检测到缓存文件,正在使用goto加载")
    breakpoint(commands=gotostr("save"))


if os.path.exists(os.path.join(zipfiledir,"temp")):
    print("检测到存在临时目录，可能是上次运行时程序没有正常退出\n删除临时目录")
    shutil.rmtree(os.path.join(zipfiledir,"temp"))
os.makedirs(os.path.join(zipfiledir,"temp","endpack"))
epath=os.path.join(zipfiledir,"temp","endpack")
print("合包")

#准备合并包
for item in os.listdir(zipfiledir):
    #每个包
    if (not item.endswith('.zip')and not os.path.isdir(os.path.join(zipfiledir,item)))or item=="temp":
        #如果结尾不是.zip就放弃这个(并且不是文件夹类型的)或者是名称是"temp"的包
        continue
    if not os.path.isdir(os.path.join(zipfiledir,item)):
        print(f"发现文件:{item}")
        path:str=os.path.join(zipfiledir,item)
        #具体的文件的路径
        os.makedirs(os.path.join(zipfiledir,"temp",item))
        thispath:str=os.path.join(os.path.join(zipfiledir,"temp"),item)
        print(f"缓存目录准备，目录是:{thispath}\n开始解压")
        #缓存的位置
        with zipfile.ZipFile(path, 'r') as zip_ref:
            zip_ref.extractall(thispath)
        print("解压完成")
        #解压到缓存目录
    else:
        print(f"居然直接是文件夹?!我直接cv\n发现文件夹形式的包{item}")
        #直接重定向到目标文件夹
        breakpoint()
        os.makedirs(os.path.join(zipfiledir,"temp",item))
        thispath:str=os.path.join(os.path.join(zipfiledir,"temp"),item)
        shutil.copy2(os.path.join(zipfiledir,item),os.path.join(zipfiledir,"temp"))
    #thispath是当前包的data文件夹
    thispath=os.path.join(thispath,"data")
    for namespace in os.listdir(thispath):
        #提取出当前命名空间
        print(f"准备合并{item}的{namespace}命名空间")
        dqns=os.path.join(thispath,namespace)
        #需要的文件夹(但是还有tacz_tags\attachments重复时需要特殊处理,这几个都是不能重复的,重复了tacz也会报错)
        if os.path.exists(os.path.join(dqns,"index","guns")):
            print("合并枪械索引文件")
            try:
                os.makedirs(os.path.join(epath,namespace,"index"))
            except FileExistsError:
                pass
            mover(os.path.join(dqns,"index","guns"),os.path.join(epath,namespace,"index",))
        else:
            print(f"没有写枪械索引文件,正常的配置路径是{os.path.join(dqns,"index","guns")}")
        if os.path.exists(os.path.join(dqns,"data","guns")):
            print("合并枪械数据文件")
            try:
                os.makedirs(os.path.join(epath,namespace,"data"))
            except FileExistsError:
                pass
            mover(os.path.join(dqns,"data","guns"),os.path.join(epath,namespace,"data"))
        else:
            print(f"没有写枪械数据文件,正常的配置路径是{os.path.join(dqns,"data","guns")}")
        if os.path.exists(os.path.join(dqns,"tacz_tags","attachments","allow_attachments")):
            print("合并允许的配件")
            try:
                os.makedirs(os.path.join(epath,namespace,"tacz_tags","attachments"))
            except FileExistsError:
                pass
            mover(os.path.join(dqns,"tacz_tags","attachments","allow_attachments"),os.path.join(epath,namespace,"tacz_tags","attachments"))
        else:
            print(f"没有允许的配件文件,正常的路径是{os.path.join(dqns,"tacz_tags","attachments","allow_attachments")}")
        if os.path.exists(os.path.join(dqns,"tacz_tags","attachments")):
            print("合并配件声明")
            try:
                os.makedirs(os.path.join(epath,namespace,"tacz_tags","attachments"))
            except FileExistsError:
                pass
            for afile in os.listdir(os.path.join(dqns,"tacz_tags","attachments")):
                print(f"合并{afile}")
                if not afile.endswith(".json"):
                    print("这个文件不是声明文件")
                    #如果不是json文件，就直接跳过这个
                    continue
                if not os.path.exists(os.path.join(epath,namespace,"tacz_tags","attachments",afile)):
                    print("直接合并")
                    #如果目标文件夹不存在这个就直接移动
                    mover(os.path.join(dqns,"tacz_tags","attachments",afile),os.path.join(epath,namespace,"tacz_tags","attachments",afile))
                else:
                    print("目标文件已存在，列表进行合并")
                    with open(os.path.join(dqns,"tacz_tags","attachments",afile),"r",encoding="utf-8")as f1:
                        with open(os.path.join(epath,namespace,"tacz_tags","attachments",afile),"r+",encoding="utf-8")as f2:
                            #合并2个文件去重后写入文件
                            json.dump(list(set(json.load(f1)+json.load(f2))),f2)
print("合包完成，准备生成枪械列表")
gunids:list[gun]=list()
#包里的data
for allnames in os.listdir(epath):
    print(f"找到命名空间{allnames}")
    absallnames=os.path.join(epath,allnames)
    #里面的每个命名空间
    if os.path.exists(os.path.join(absallnames,"index","guns")):
        print("找到目标gun文件夹")
        #如果没有写gun的内容就跳过
        for file in os.listdir(os.path.join(absallnames,"index","guns")):
            print(f"找到文件{file}")
            allow_attachmentsid=list()
            #每个文件
            with open(os.path.join(absallnames,"index","guns",file),"r",encoding="utf-8")as f:
                #读取索引文件保存为datafile
                data = json5.load(f)
                datafile=data["data"].split(':',1)
            with open(os.path.join(epath,datafile[0],"data","guns",datafile[1]+".json"),"r",encoding="utf-8") as f:
                print(f"找到数据文件:{os.path.join(epath,datafile[0],"data","guns",datafile[1]+".json")}")
                #读取数据文件的ammo和fire_mode字段(使用的弹药和开火模式)
                data = json5.load(f)
                ammo=data["ammo"]
                fire_mode=data["fire_mode"].copy()[0]
            if not os.path.exists(os.path.join(absallnames,"tacz_tags","attachments","allow_attachments",file)):
                print(f"没有配件可用或者没有写枪?,正常的配置位置:{os.path.join(absallnames,"tacz_tags","attachments","allow_attachments",file)}")
                gunids.append(gun(allnames+":"+os.path.splitext(file)[0],ammo,fire_mode,list()))
                continue
            with open(os.path.join(absallnames,"tacz_tags","attachments","allow_attachments",file),"r",encoding="utf-8")as f:
                print(f"读取支持的配件:{os.path.join(absallnames,"tacz_tags","attachments","allow_attachments",file)}")
                #读取允许的配件列表
                data = json5.load(f)
                allow_attachments=data.copy()
            for allowatt in allow_attachments:
                #读取每一个内容
                if not allowatt.startswith("#"):
                    #如果不是标签
                    allow_attachmentsid.append(allowatt)
                    #就直接加入到最终列表
                else:
                    print(f"展开标签{allowatt}")
                if os.path.exists(os.path.join(allnames,allowatt.split(":")[0],"tacz_tags","attachments",allowatt.split(":")[1])):
                #如果存在这个文件
                    with open(os.path.join(epath,allowatt.split(":")[0],"tacz_tags","attachments",allowatt.split(":")[1]),"r",encoding="utf-8")as f:
                        #打开这个包的标签表示的文件
                        for ii in json.load(f):
                            #的所有内容加入列表
                            allow_attachmentsid.append(ii)
            gunids.append(gun(allnames+":"+os.path.splitext(file)[0],ammo,fire_mode,allow_attachmentsid))
            #把gun加入到列表中
    else:
        print("没有写枪？")


print("炸了临时目录")
shutil.rmtree(os.path.join(zipfiledir,"temp"))
with open("save.json","w",encoding="utf-8")as f:
    #序列化列表并存储
    f.write(serialize_gun_list(gunids))
nosave:int=1
#label save
if os.path.exists("save.json")and nosave == 0:
    with open("save.json","r",encoding="utf-8")as f:
        #读取缓存文件
        gunids=deserialize_gun_list(f.read()).copy()




print("生成func文件")
with open("start.mcfunction","w",encoding="utf-8")as f:
    for ii in pls:
        print(f"给玩家{ii}发道具")
        #当前玩家的内容
        okgun:list[gun]=list()
        #重置已发的gun
        if not gunids:
            print("你根本没有枪啊")
            break
        for i in range(1,gunsrools+1):
            dqgun=random.choice(gunids)
            print(f"给{ii}发{dqgun.gunid}")
            okgun.append(dqgun)
            f.write(f"give {ii} tacz:modern_kinetic_gun 1 "+"{"+f"\"GunId\":\"{dqgun.gunid}\",\"GunFireMode\":\"{dqgun.fire_mode}\""+"}\n")
        #发gun
        for iii in okgun:
            print(f"给{ii}的{iii.gunid}发{ammorools}发{iii.ammo}弹药")
            f.write(f"give {ii} tacz:ammo {ammorools} "+"{"+f"\"AmmoId\":\"{iii.ammo}\""+"}\n")
            #发ammo
            if not iii.allow_attachmentsid:
                print("没有配件可发")
                break
            for iiii in range(1,attachmentsrools+1):
                dqattachments=random.choice(iii.allow_attachmentsid)
                print(f"给{ii}的{iii.gunid}发{dqattachments}配件")
                f.write(f"give {ii} tacz:attachment 1 "+"{"+f"\"AttachmentId\":\"{dqattachments}\""+"}\n")
                #发attachment
    if addconnamds is True:
        print("额外命令已开启")
        if os.path.exists("addcommands.mcfunction"):
            with open("addcommands.mcfunction","r",encoding="utf-8")as f1:
                readdata=f1.read()
                print(f"你要执行的命令是{readdata}")
                f.write(readdata)
        else:
            print("额外命令文件不存在")
if spdatapack is True:
    vers=mcver.split(".",2)
    #提取出每一位版本号
    vers=[int(i) for i in vers]
    #转换为int
    if len(vers)==2:
        vers.append(0)
    can_rename_pack_format=False
    if vers[1]>=21:
        funcfilename="function"
    else:
        funcfilename="functions"
    #如果版本大于1.21就把functions改名变成functions(ojang的改名)
    if vers[1]==13 or vers[1]==14:
        #1.13-1.14.4,13and14,4
        pack_format=4
    elif vers[1]==15 or (vers[1]==16 and vers[2]<=1):
        #1.15-1.16.1,15 and 16<=1,5
        pack_format=5
    elif vers[1]==16 and vers[2]>=2:
        #1.16.2-1.16.5,16 and >=2,6
        pack_format=6
    elif vers[1]==17:
        #1.17-1.17.1,17,7
        pack_format=7
    elif vers[1]==18 and vers[2]<=1:
        #1.18-1.18.1,18 and <=1,8
        pack_format=8
    elif vers[1]==18 and vers[2]==2:
        #1.18.2,18 and 2,9
        pack_format=9
    elif vers[1]==19 and vers[2]<=3:
        #1.19-1.19.3,19 and <=3,10
        pack_format=10
    elif vers[1]==19 and vers[2]==4:
        #1.19.4,19 and ==4,12
        pack_format=12
    elif vers[1]==20 and vers[2]<=1:
        #1.20-1.20.1,20 and <=1,15
        pack_format=15
    elif vers[1]==20 and vers[2]==2:
        #1.20.2,20 and 2,18
        pack_format=18
    elif vers[1]==20 and (vers[2]==3 or vers[2]==4):
        #1.20.3-1.20.4,20 and (3 or 4),26
        pack_format=26
    elif vers[1]==20 and vers[2]>=5:
        #1.20.5-1.20.6,20 and >=5,41
        pack_format=41
    elif vers[1]==21 and vers[2]<=1:
        #1.21-1.21.1,21 and <=1,48
        pack_format=48
    elif vers[1]==21 and (vers[2]==2 or vers[2]==3):
        #1.21.2-1.21.3,21 and (2 or 3),57
        pack_format=57
    elif vers[1]==21 and vers[2]==4:
        #1.21.4,21 and 4,61
        pack_format=61
    elif vers[1]==21 and vers[2]==5:
        #1.21.5,21 and 5,71
        pack_format=71
    elif vers[1]==21 and vers[2]==6:
        #1.21.6,21 and 6,80
        pack_format=80
    elif vers[1]==21 and (vers[2]==7 or vers[2]==7):
        #1.21.7-1.21.8,21 and (7 or 8),81
        pack_format=81
    elif vers[1]>=21 and vers[2]>=9:
        #1.21.9+ ojang的改名之min_format,max_format
        can_rename_pack_format=True
    else:
        print("不支持的版本号，这个版本不存在或者是非正常版本(如4.1特殊版本)")
        quit(0)


    if not os.path.exists(os.path.join(sppath,"datapack","data","game",funcfilename)):
        print("检测到你开启了数据包生成模式\n生成数据包\n正在创建数据包文件夹")
        os.makedirs(os.path.join(sppath,"datapack","data","game",funcfilename))
        print("写入包元数据")
        with open(os.path.join(sppath,"datapack","pack.mcmeta"),"w",encoding="utf-8")as f:
            if can_rename_pack_format is True:
                #因为ojang的改名，最低只可以到48(1.21)但pack_format必须在min_format和max_format指定的范围内,但又其实因为低版本必须有pack_format但是这个版本不支持使用pack_format其实是不兼容的(ojng员工小时候升三年级发现自己二年级写的暑假作业broken or incompatible)
                f.write("{\"pack\"}:{\"min_format\":\"[82,0]\",\"max_format\":\"[2147483647,2147483647]\",\"description\":\"a randompack\"}")
            else:
                f.write("{\"pack\":{\"pack_format\":"+f"{pack_format}"+",\"description\":\"a randompack\"}}")
        print("移动作好的函数文件")
        mover("start.mcfunction",os.path.join(sppath,"datapack","data","game",funcfilename))
        print("生成完成")
    else:
        print("检测到你开启了数据包生成模式\n存在数据包,更新数据包的对应文件")
        mover("start.mcfunction",os.path.join(sppath,"datapack","data","game",funcfilename))
        print("更新完成")
