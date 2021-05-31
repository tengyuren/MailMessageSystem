from flask import Flask,request,Response,render_template
from flask_mail import Mail, Message
import json
import time
import requests

app=Flask(__name__)
app.secret_key="ren"

# 配置信息
app.config['MAIL_SERVER'] = 'smtp.163.com'
app.config['MAIL_PORT'] = 25
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'melon_garden@163.com'   #官方账号
app.config['MAIL_PASSWORD'] = 'ONJDDBYVQQWOPCPC'   # ujeustlpkjtobfia  onyruclmralnbbgb ，密钥  UFQNCRHIOBGLZVNH ONJDDBYVQQWOPCPC mg123465
# app.config['FLASKY_MAIL_SUBJECT_PREFIX'] = '163.com'
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
    msg = Message('MelonGarden Official', sender='melon_garden@163.com', recipients=[to_user,'melon_garden@163.com'])
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
                                <h1 class="logo" title="Mail From MelonGarden">
                                    <img class="im" src="https://6370-cpcloud-4goick7vdf024294-1305462307.tcb.qcloud.la/logo.png?sign=275b2da1dbb167e7652d5b9ff63a38ed&t=1622203471">
                                    Mail From MelonGarden
                                </h1>
                            </div>
                            <!-- 开始 -->
                            <div class="nav-wrapper">
                                <!-- 固定 -->
                                <div class="clearfix">
                                    <div class="all-goods-wrapper">
                                        <div class="all-goods" >Dear %s ：</div>
                                        <div class="left-menu">
                                            %s users found interesting posts on the MelonGarden blog and @you, you can check it at your convenience.  
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
                                <a href="http://github.raiix.com/melongarden/" class="a_to">Go to view</a>
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