import zipfile
import os
import shutil
import typing
import json

startguns:typing.Literal[False,True]=True
gunsrools:int=1
startammo:typing.Literal[False,True]=False
ammorools:int=300
startattachments:typing.Literal[False,True]=True
attachmentsrools:int=30



zipfiledir:str=input("输入目标目录:")
if os.path.exists("randomdatapack"):
    print("当前目录有生成的结果?删了它")
    shutil.rmtree("randomdatapack")
gunids:list[str]=list()
ammoids:list[str]=list()
attachmentsids:list[str]=list()
for item in os.listdir(zipfiledir):
    #每个包
    if not item.endswith('.zip')and not os.path.isdir(item):
        #如果结尾不是.zip就放弃这个(并且不是文件夹类型的)
        continue
    if not os.path.isdir(item):
        print(f"发现文件:{item}")
        path:str=os.path.join(zipfiledir,item)
        #具体的文件的路径
        os.system("md \""+str(os.path.join(os.path.join(zipfiledir,"temp"),item))+"\"")
        epath:str=os.path.join(os.path.join(zipfiledir,"temp"),item)
        print(f"缓存目录准备，目录是:{epath}\n开始解压")
        #缓存的位置
        with zipfile.ZipFile(path, 'r') as zip_ref:
            zip_ref.extractall(epath)
        print("解压完成")
        #解压到缓存目录
    else:
        print(f"居然直接是文件夹?!我直接把缓存目录设置到这个文件夹\n发现文件夹形式的包{item}")
        #直接重定向到目标文件夹
        epath=item
    epath=os.path.join(epath,"data")
    #包里的data
    for allnames in os.listdir(epath):
        print(f"找到命名空间{allnames}")
        absallnames=os.path.join(epath,allnames)
        #里面的每个命名空间
        if os.path.exists(os.path.join(absallnames,"index","guns")):
            print("找到目标gun文件夹")
            #如果没有写gun的内容就跳过
            for file in os.listdir(os.path.join(absallnames,"index","guns")):
                print(f"找到文件{file}\n加入gun列表")
                #每个文件
                gunids.append(allnames+":"+os.path.splitext(file)[0])
                #获取它的名字(就是gunid)存入gunid表
        if os.path.exists(os.path.join(absallnames,"index","ammo")):
            print("找到目标ammo文件夹")
            #如果没有写ammo的内容就跳过
            for file in os.listdir(os.path.join(absallnames,"index","ammo")):
                print(f"找到文件{file}\n加入ammo列表")
                #每个文件
                ammoids.append(allnames+":"+os.path.splitext(file)[0])
                #获取它的名字(就是ammoid)存入ammoid表
        if os.path.exists(os.path.join(absallnames,"index","attachments")):
            print("找到目标attachments文件夹")
            #如果没有写attachments的内容就跳过
            for file in os.listdir(os.path.join(absallnames,"index","attachments")):
                print(f"找到文件{file}\n加入attachments列表")
                #每个文件
                attachmentsids.append(allnames+":"+os.path.splitext(file)[0])
                #获取它的名字(就是attachmentsid)存入attachmentsid表

print("炸了临时目录")
shutil.rmtree(os.path.join(zipfiledir,"temp"))
#炸了临时目录
pools:list=list()
print(f"准备添加gun池,随机{gunsrools}次")
if startguns is True:
    gunitems=list()
    for agun in gunids:
        print(f"添加{agun}到gun池内")
        gunitems.append({"type":"item","name":"tacz:modern_kinetic_gun","functions":[{"function":"set_nbt","tag":"{"+f"\"GunId\":\"{agun}\""+"}"}]})
    pools.append({"rolls":gunsrools,"entries":gunitems})
print(f"准备添加ammo池,随机{ammorools}次")
if startammo is True:
    ammoitems=list()
    for aammo in ammoids:
        print(f"添加{aammo}到ammo池内")
        ammoitems.append({"type":"item","name":"tacz:ammo","functions":[{"function":"set_nbt","tag":"{"+f"\"AmmoId\":\"{aammo}\""+"}"}]})
    pools.append({"rolls":ammorools,"entries":ammoitems})
print(f"准备添加attachments池,随机{attachmentsrools}次")
if startattachments is True:
    attachmentsitems=list()
    for aattachments in attachmentsids:
        print(f"添加{aattachments}到attachments池内")
        attachmentsitems.append({"type":"item","name":"tacz:attachment","functions":[{"function":"set_nbt","tag":"{"+f"\"AttachmentId\":\"{aattachments}\""+"}"}]})
    pools.append({"rolls":attachmentsrools,"entries":attachmentsitems})
o={"pools":pools}
print(f"完成，目前内容:{o}\n准备保存为数据包\n创建文件夹")
os.makedirs(os.path.join("randomdatapack","data","randatapck","loot_tables"))
os.makedirs(os.path.join("randomdatapack","data","randatapck","functions"))
print("写入pack.mcmeta")
with open(os.path.join("randomdatapack","pack.mcmeta"),'w',encoding="utf-8")as f:
    f.write("{\"pack\":{\"pack_format\":15,\"description\":\"a randompack\"}}")
print("写入func")
with open(os.path.join("randomdatapack","data","randatapck","functions","gamestart.mcfunction"),'w',encoding="utf-8")as f:
    f.write("loot give @a loot randatapck:pools")
print("序列化并保存为战利品表json文件")
with open(os.path.join("randomdatapack","data","randatapck","loot_tables","pools.json"), 'w', encoding='utf-8') as f:
    json.dump(o, f, ensure_ascii=False, indent=4)
print("json文件保存完成")
