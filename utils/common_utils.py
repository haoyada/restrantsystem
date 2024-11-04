''' Common utilities files for the entire project '''
import time, os, random, io
from PIL import Image, ImageDraw, ImageFont
from django.http import HttpResponse


''' upload pics 
example:
    cover_pic = uploadPicFile(request, "cover_pic", "没有店铺封面上传文件信息")
    ...
    if cover_pic != "NO_PIC_UPLOADED":
        ob.cover_pic = cover_pic
    ...
    ob.save() 
'''
def uploadPicFile(req, filename, target, failMessage, oldPicFile=None, defaultPicName=None):
        myfile = req.FILES.get(filename,None)
        if not myfile:
            # return HttpResponse(failMessage)
            return "NO_PIC_UPLOADED"
        
        if oldPicFile != "NO_PIC_UPLOADED":
            try:
                if defaultPicName != oldPicFile:
                    old_file_path = f"./static/uploads/{target}/{oldPicFile}"
                    os.remove(old_file_path)
            except FileNotFoundError:
                # Handle the case where the file does not exist
                print(f"The file {old_file_path} does not exist.")
                pass
            except Exception as e:
                # Handle other possible exceptions
                print(f"An error occurred: {e}") 

        cover_pic = str(time.time()).replace(".","_") +"."+myfile.name.split('.').pop()
        destination = open("./static/uploads/" + str(target) + "/" +cover_pic,"wb+")
        for chunk in myfile.chunks():      # 分块写入文件  
            destination.write(chunk)  
        destination.close()

        return cover_pic


# 输出验证码
def verifies(request):
    #引入随机函数模块
    # import random
    # from PIL import Image, ImageDraw, ImageFont
    #定义变量，用于画面的背景色、宽、高
    #bgcolor = (random.randrange(20, 100), random.randrange(
    #    20, 100),100)
    bgcolor = (242,164,247)
    width = 100
    height = 25
    #创建画面对象
    im = Image.new('RGB', (width, height), bgcolor)
    #创建画笔对象
    draw = ImageDraw.Draw(im)
    #调用画笔的point()函数绘制噪点
    for i in range(0, 100):
        xy = (random.randrange(0, width), random.randrange(0, height))
        fill = (random.randrange(0, 255), 255, random.randrange(0, 255))
        draw.point(xy, fill=fill)
    #定义验证码的备选值
    #str1 = 'ABCD123EFGHIJK456LMNOPQRS789TUVWXYZ0'
    str1 = '0123456789'
    #随机选取4个值作为验证码
    rand_str = ''
    for i in range(0, 4):
        rand_str += str1[random.randrange(0, len(str1))]
    #构造字体对象，ubuntu的字体路径为“/usr/share/fonts/truetype/freefont”
    font = ImageFont.truetype('static/arial.ttf', 21)
    #font = ImageFont.load_default().font
    #构造字体颜色
    fontcolor = (255, random.randrange(0, 255), random.randrange(0, 255))
    #绘制4个字
    draw.text((5, -3), rand_str[0], font=font, fill=fontcolor)
    draw.text((25, -3), rand_str[1], font=font, fill=fontcolor)
    draw.text((50, -3), rand_str[2], font=font, fill=fontcolor)
    draw.text((75, -3), rand_str[3], font=font, fill=fontcolor)
    #释放画笔
    del draw
    #存入session，用于做进一步验证
    request.session['verifycode'] = rand_str
    """
    python2的为
    # 内存文件操作
    import cStringIO
    buf = cStringIO.StringIO()
    """
    # 内存文件操作-->此方法为python3的
    # import io
    buf = io.BytesIO()
    #将图片保存在内存中，文件类型为png
    im.save(buf, 'png')
    #将内存中的图片数据返回给客户端，MIME类型为图片png
    return HttpResponse(buf.getvalue(), 'image/png')