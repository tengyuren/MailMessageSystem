from flask import Flask,request,Response,render_template
from flask_mail import Mail, Message
import json
import time
import requests

app=Flask(__name__)
app.secret_key="ren"

# 配置信息
app.config['MAIL_SERVER'] = 'smtp.qq.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = '877494093@qq.com'   #官方账号
app.config['MAIL_PASSWORD'] = 'onyruclmralnbbgb'   # ujeustlpkjtobfia ，密钥
mail = Mail(app)

TEMPLATES_AUTO_RELOAD = True
SEND_FILE_MAX_AGE_DEFAULT = 0

@app.route("/",methods=["GET","POST"])
def root():
    return "hello , this is index page"

# 获得评论
def get_comment(post_id,id):
    print(post_id,id)
    url = 'http://81.68.104.78:8082/api/v1/comments/%s/%s'%(post_id,id)
    return requests.get(url).json()['content']

# 参数：from(当前评论人的邮箱),to（需要发送的人的邮箱）,content（评论的内容）
@app.route("/api/postmail/<from_user>/<to_user>/<post_id>/<id>",methods=["GET","POST"])
def post_mail(from_user,to_user,post_id,id):
    print(from_user,to_user,post_id,id)
    if(not to_user):
        return "must contain a deceiver"
    if(not post_id or not id):
        return "error , please take post_id and id"
    
    # 获取当前时间
    time_std=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    
    # 请求post_id、id给内容赋值
    try:
        content=get_comment(post_id,id)
    except:
        content='<h3>快来查看评论吧</h3>'
    
    # 返回值
    msg = Message('MelonGarden官方提醒邮件', sender='877494093@qq.com', recipients=['877494093@qq.com'])
    msg.html= '''<!DOCTYPE html>
                    <html lang="en">
                    <head>
                    </head>
                    <body>
                        <style>
                        a{
                            text-decoration: none;
                        }
                        .a_to{
                            color: rgb(167, 215, 172);
                            font-weight: 600;
                            box-shadow:1px 1px 6px white ;
                        }
                        .header .nav-wrapper{
                            float: left;
                            margin-left: 7px;
                        }

                        .nav .show-goods:hover ~ .good-info,
                        .good-info:hover{
                            height: 228px;
                            border-top: 1px solid rgb(224,224,224);
                            box-shadow: 0 5px 3px rgba(0, 0, 0, 0.2);
                        }
                        .header-wrapper{
                            width: 650px;
                            height: 700px;
                            background-color: rgb(167, 215, 172);
                            margin: 0 auto;
                            padding: 10px;
                            border-radius: 20px;
                            box-shadow:-5px -5px 10px rgb(206, 204, 204) ;
                        }
                        .logo{
                            font-size: 40px;
                            line-height: 40px;
                        }
                        .clearfix{
                            margin-top: 60px;
                            line-height: 50px;
                            font-size: 18px;
                            background-color: rgb(167, 215, 172);
                        }
                        .im{
                            width: 60px;
                            padding-top: 12px;
                            padding-right: 20px;
                        }
                        .all-goods{
                            font-weight: 700;
                        }
                        .left-menu{
                            padding-left: 30px;
                        }
                        .content_wrapper{
                            background-color: white;
                            margin-top: 30px;
                            padding: 20px;
                            margin-left: 20px;
                            margin-right: 20px;
                            border-radius: 20px;
                            box-shadow:1px 1px 6px rgb(250, 249, 249) ; 
                        }
                        .shuming{
                            font-size: smaller; 
                            color: rgb(204, 204, 199);
                            
                        }
                        .btn_wrapper{
                            width: 100px;
                            height: 50px;
                            background-color: white;
                            text-align: center;
                            line-height: 50px;
                            border-radius: 10px;
                            margin: 0 auto;
                            margin-top: 60px;
                        }
                        </style>
                        <div class="header-wrapper">
                            <div class="headerclearfix">
                                <!-- 创建logo -->
                                <h1 class="logo" title="来自MelonGarden的邮件">
                                    <img class="im" src="https://6370-cpcloud-4goick7vdf024294-1305462307.tcb.qcloud.la/logo.png?sign=275b2da1dbb167e7652d5b9ff63a38ed&t=1622203471">
                                    来自MelonGarden的邮件
                                </h1>
                            </div>
                            <!-- 开始 -->
                            <div class="nav-wrapper">
                                <!-- 固定 -->
                                <div class="clearfix">
                                    <div class="all-goods-wrapper">
                                        <div class="all-goods" >亲爱的%s，您好：</div>
                                        <div class="left-menu">
                                            %s用户在MelonGarden博客中找到了有趣的帖子并且@了您，希望您及时查看。  
                                        </div>
                                    </div> 
                                </div>
                                <!-- 嵌入的内容 -->
                                <div class="content_wrapper">
                                    %s
                                    <p class="shuming">MelonGarden %s</p>
                                </div>
                            </div>
                            <div class="btn_wrapper">
                                <a href="http://github.raiix.com/melongarden/" class="a_to">前往查看</a>
                            </div>
                        </div>
                    </body>
                    </html>
    '''%(from_user,to_user,content,time_std)
    with app.app_context():
        mail.send(msg)
    return "send mail ok"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port='5001')