# coding:utf-8



from PIL import Image
import time

def pinjie(a, b):
    a = a.replace("C:\\Users\Administrator\Downloads", '')
    b = b.replace("C:\\Users\Administrator\Downloads", '')
    for pic_name in [a, b]:
        if "1" not in pic_name:
            #加载底图
            base_img = Image.open('images/di.png')
            # 可以查看图片的size和mode，常见mode有RGB和RGBA，RGBA比RGB多了Alpha透明度
            box = (0,0, 321,30)  # 底图上需要P掉的区域
            #加载需要P上去的图片
            path = "C:\\Users\Administrator\Downloads\\"
            tmp_img = Image.open(path+pic_name)
            #这里可以选择一块区域或者整张图片
            #region = tmp_img.crop((0,0,304,546)) #选择一块区域
            #或者使用整张图片
            region = tmp_img
            #使用 paste(region, box) 方法将图片粘贴到另一种图片上去.
            # 注意，region的大小必须和box的大小完全匹配。但是两张图片的mode可以不同，合并的时候回自动转化。如果需要保留透明度，则使用RGMA mode
            #提前将图片进行缩放，以适应box区域大小
            region = region.resize((box[2] - box[0], box[3] - box[1]))
            base_img.paste(region, box)
            base_img.save('images/di_pic.png') #保存图片
        else:
                # time.sleep(5)
                base_img = Image.open('images/di_pic.png')
                box = (0,39, 321,139)  # 底图上需要P掉的区域
                path = "C:\\Users\Administrator\Downloads\\"
                tmp_img = Image.open(path+pic_name)
                region = tmp_img
                region = region.resize((box[2] - box[0], box[3] - box[1]))
                base_img.paste(region, box)
                base_img.save('images/out.png') #保存图片
pinjie("下载.png", "下载 (1).png")