from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.views.generic import ListView, DetailView
from django.views.generic.dates import ArchiveIndexView, TodayArchiveView
from django.contrib.auth.models import User
from django.contrib import auth, messages
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from cryptography.fernet import Fernet
import time
from .models import Post, Comment
import cx_Oracle
import smtplib
from email.message import EmailMessage

def index(request):
    boars = Post.objects.order_by('-id')
    posts = Post.objects
    post_list = Post.objects.all().order_by('-id')
    paginator = Paginator(post_list, 9)
    page = request.GET.get('page')
    postL = paginator.get_page(page)
    return render(request, 'main/index.html', {'boars': boars,'posts':posts,'postL': postL})

def main(request):
    return redirect('/')

def test(request):
    comment = Comment.objects.order_by('-id')
    posts = Post.objects
    post_list = Post.objects.all().order_by('-id')
    paginator = Paginator(post_list,5)
    page = request.GET.get('page')
    postL = paginator.get_page(page)

    return render(request, 'main/test.html', {'posts':posts,'postL': postL,'comment':comment})


def login(request):
    return render(request,'main/login.html')

def loginRes(request):
    id = request.POST.get('id')
    pw = request.POST.get('pw')
    user = auth.authenticate(request, username=id, password=pw)

    if user is not None:
        connection = cx_Oracle.connect('spuser', 'spuser', '210.216.37.5/SPRING')
        cursor = connection.cursor()
        sql = "SELECT * FROM AUTH_USER WHERE USERNAME= '%s' " % id
        cursor.execute(sql)
        rows = cursor.fetchall()
        login = []
        for row in rows:
            dic = {'id': row[0], 'password': row[1], 'is_superuser': row[3], 'username': row[4], 'is_staff': row[8],
                   'is_active': row[9]}
            login.append(dic)
        print(login[0].get('id'))
        connection.close()
        if login[0].get('is_superuser') == 1 and login[0].get('is_staff') == 1 and login[0].get('is_active') == 1:
            auth.login(request, user)
            boars = Post.objects.order_by('-id')
            return redirect('main')
        else:
            messages.info(request, '관리자 권한이 없습니다.')
            return render(request, 'main/login.html')
    else:
        messages.info(request, 'id, pw를 확인해주세요.')
        return render(request, 'main/login.html')

def signup(request):
    return render(request,'main/signup.html')

def signupRes(request):
    if request.method == 'POST':
        if request.POST['pw1'] == request.POST['pw2']:
            user = User.objects.create_user(
                request.POST['id'], password=request.POST['pw1'])
            auth.login(request, user)
            return redirect('/')
        return render(request, 'main/signup.html')
    return render(request, 'signup.html')


def boar(request):
    boars = Post.objects.order_by('-id')
    return render(request, 'main/board.html', {'boars':boars})

def pwConfirm(request, board_id):
    board_detail = get_object_or_404(Post, pk=board_id)
    return render(request, 'main/pwConfirm.html', {'board': board_detail})

def pwConfirmRes(request, board_id):
    pw1 = request.POST.get('pw1')
    pw2 = request.POST.get('pw2')
    board_detail = get_object_or_404(Post, pk=board_id)
    print(board_detail.content)

    key=(board_detail.key).encode('utf-8')
    print('확인 key:'+board_detail.key)
    print(key)
    print('확인 비번:'+pw1)
    print('확인 비번2:'+pw2)
    simpleEnDecrypt = SimpleEnDecrypt(key)
    decrypt_pw1 = simpleEnDecrypt.decrypt(pw1)
    print(decrypt_pw1)
    decrypt_content = simpleEnDecrypt.decrypt(board_detail.content)
    board_detail.content = decrypt_content
    if request.method == 'POST':
        if decrypt_pw1 == request.POST.get('pw2'):
            print(request.POST.get('pw1'))
            print(request.POST.get('pw2'))
            return render(request, 'main/board_detail.html', {'board': board_detail})
        messages.info(request,'비밀번호가 일치하지 않습니다.')
        return redirect('main')
    return redirect('pwConfirm')



def board_detail(request,board_id):
    board_detail = get_object_or_404(Post, pk=board_id)
    key = (board_detail.key).encode('utf-8')
    simpleEnDecrypt = SimpleEnDecrypt(key)
    print(key)
    print(board_detail.content)
    decrypt_content = simpleEnDecrypt.decrypt(board_detail.content)
    board_detail.content = decrypt_content
    return render(request, 'main/board_detail.html', {'board': board_detail})

def create(request):
    return render(request, 'main/create.html')

def createRes(request):
    simpleEnDecrypt = SimpleEnDecrypt()
    now = time.localtime()
    year = str(now.tm_year)
    month = str(now.tm_mon)
    day = str(now.tm_mday)
    hour = str(now.tm_hour)
    min = str(now.tm_min)
    sec = str(now.tm_sec)
    homepage = 'http://bluebird.spsemi.co.kr/'
    if len(hour) == 1:
        hour = '0' + hour
    elif len(min) == 1:
        min = '0' + min

    date = '(' + year + month + day + hour + min + sec + ')'
    mail_date = year+'년 '+month+'월 '+day+'일 '+ hour+":" + min
    if request.method == 'POST':
        if 'file' in request.FILES:
            file = request.FILES['file']
            filename = file._name
            fp = open('%s/%s' % ('C:\\apps\\bluebird\\board\\static\\file', date + filename), 'wb')
            for chunk in file.chunks():
                fp.write(chunk)
            fp.close()
            fileRes = date + filename
            post = Post()
            post.title = request.POST['title']
            post.content = simpleEnDecrypt.encrypt(request.POST['content'])
            post.key = (simpleEnDecrypt.key).decode('utf-8')
            print(post.content)
            print(simpleEnDecrypt.decrypt(post.content))
            post.writer = request.POST['writer']
            post.tent = simpleEnDecrypt.encrypt(request.POST['pw'])
            print('생성 비번:' + post.tent)

            post.pub_date = timezone.datetime.now()
            post.filename = fileRes
            post.save()

            id = str(post.__getattribute__('id'))
            print(post.__getattribute__('id'))
            smtp = smtplib.SMTP('118.128.208.148', 25)
            smtp.ehlo()
            smtp.esmtp_features["smtputf8"] = ""
            smtp.login('master@spsemi.co.kr', 'spadmin1!')  # 로그인
            msg = EmailMessage()
            strres = 'http://210.216.37.23:9001/AdmincreateRes/board_detail/' + '%s' % id
            title = "파랑새 게시판에 새로운 글 [%s 번]이 등록되었습니다." % id
            print(title)
            content = "글 번호: %s<br>" % id + '\n' + "작성자: %s<br>" % post.writer + '\n' + "작성일: %s<br>" % (mail_date)  + '\n' + "홈페이지: %s" % (homepage) + '\n' + "<br><a href=%s>바로가기</a>" % (homepage)
            print(content)
            # 제목 입력
            msg['Subject'] = title
            # 내용 입력
            msg.set_content(content)
            # 보내는 사람
            msg['From'] = 'master@spsemi.co.kr'
            # 받는 사람
            msg['To'] = 'syyoon@spsemi.co.kr'
            smtp.send_message(msg)
            smtp.quit()
        else:
            post = Post()
            post.title = request.POST['title']
            post.content = simpleEnDecrypt.encrypt(request.POST['content'])
            post.key = (simpleEnDecrypt.key).decode('utf-8')
            print(post.content)
            print(simpleEnDecrypt.decrypt(post.content))
            post.writer = request.POST['writer']
            post.tent = simpleEnDecrypt.encrypt(request.POST['pw'])
            print('생성 비번:'+post.tent)

            post.pub_date = timezone.datetime.now()
            post.save()

            id = str(post.__getattribute__('id'))
            print(post.__getattribute__('id'))
            smtp = smtplib.SMTP('118.128.208.148', 25)
            smtp.ehlo()
            smtp.esmtp_features["smtputf8"] = ""
            smtp.login('master@spsemi.co.kr', 'spadmin1!')  # 로그인
            msg = EmailMessage()
            strres = 'http://210.216.37.23:9001/AdmincreateRes/board_detail/'+'%s' % id
            title = "파랑새 게시판에 새로운 글 [%s 번]이 등록되었습니다." % id
            print(title)
            content = "글 번호: %s<br>" % id + '\n' + "작성자: %s<br>" % post.writer + '\n' + "작성일: %s<br>" % (mail_date)  + '\n' + "홈페이지: %s" % (homepage) + '\n' + "<br><a href=%s>바로가기</a>" % (homepage)
            print(content)
                        # 제목 입력
            msg['Subject'] = title
            # 내용 입력
            msg.set_content(content)
            # 보내는 사람
            msg['From'] = 'master@spsemi.co.kr'
            # 받는 사람
            msg['To']= 'syyoon@spsemi.co.kr'
            smtp.send_message(msg)
            smtp.quit()

    return redirect('main')

def AdmincreateRes(request):
    simpleEnDecrypt = SimpleEnDecrypt()
    now = time.localtime()
    year = str(now.tm_year)
    month = str(now.tm_mon)
    day = str(now.tm_mday)
    hour = str(now.tm_hour)
    min = str(now.tm_min)
    sec = str(now.tm_sec)
    if len(hour) == 1:
        hour = '0' + hour
    elif len(min) == 1:
        min = '0' + min

    date = '(' + year + month + day + hour + min + sec + ')'
    if request.method == 'POST':
        if 'file' in request.FILES:
            file = request.FILES['file']
            filename = file._name
            fp = open('%s/%s' % (
            'C:\\apps\\bluebird\\board\\static\\file', date + filename), 'wb')
            for chunk in file.chunks():
                fp.write(chunk)
            fp.close()
            fileRes = date + filename
            post = Post()
            post.title = request.POST['title']
            post.content = simpleEnDecrypt.encrypt(request.POST['content'])
            post.key = (simpleEnDecrypt.key).decode('utf-8')
            print(post.key)
            print(type(post.key))
            print(post.content)
            print(simpleEnDecrypt.decrypt(post.content))
            post.writer = request.POST['writer']
            post.tent = simpleEnDecrypt.encrypt(request.POST['pw'])
            print('생성 비번:' + post.tent)
            post.pub_date = timezone.datetime.now()
            post.filename = fileRes
            post.save()
        else:
            post = Post()
            post.title = request.POST['title']
            post.content = simpleEnDecrypt.encrypt(request.POST['content'])
            post.key = (simpleEnDecrypt.key).decode('utf-8')
            print(post.key)
            print(type(post.key))
            print(post.content)
            print(simpleEnDecrypt.decrypt(post.content))
            post.writer = request.POST['writer']
            post.tent = simpleEnDecrypt.encrypt(request.POST['pw'])
            print('생성 비번:' + post.tent)
            post.pub_date = timezone.datetime.now()
            post.save()
    return redirect('main')

def update(request, board_id):
    board = Post.objects.get(id=board_id)
    key = (board.key).encode('utf-8')
    simpleEnDecrypt = SimpleEnDecrypt(key)
    decrypt_content = simpleEnDecrypt.decrypt(board.content)
    board.content = decrypt_content
    if request.method == "POST":
        board = Post.objects.get(id=board_id)
        key = (board.key).encode('utf-8')
        simpleEnDecrypt = SimpleEnDecrypt(key)
        board.title = request.POST['title']
        board.content = simpleEnDecrypt.encrypt(request.POST['content'])
        board.writer = request.POST['writer']
        board.tent = simpleEnDecrypt.encrypt(request.POST['pw'])
        board.pub_date = timezone.datetime.now()
        board.save()
        return redirect('/')
    else:
        return render(request, 'main/update.html',{'board' : board})


def delete(request, board_id):
    board = Post.objects.get(id = board_id)
    board.delete()
    return redirect('main')

def adminDelete(request, board_id):
    board = Post.objects.get(id=board_id)
    board.delete()
    return redirect('main')

def logout(request):
    auth.logout(request)
    return redirect('/')

def adminBoard(request):
    boars = Post.objects.order_by('-id')
    posts = Post.objects
    post_list = Post.objects.all().order_by('-id')
    paginator = Paginator(post_list, 9)
    page = request.GET.get('page')
    postL = paginator.get_page(page)

    return render(request, 'main/adminBoard.html', {'boars': boars, 'posts': posts, 'postL': postL})

def adminBoardBack(request):
    return redirect('adminBoard')


def commentWrite(request, boar_pk):
    if request.method == 'POST':
        post = get_object_or_404(Post, pk=boar_pk)
        key = (post.key).encode('utf-8')
        simpleEnDecrypt = SimpleEnDecrypt(key)
        decrypt_content = simpleEnDecrypt.decrypt(post.content)
        post.content = decrypt_content
        comment = Comment()
        comment.post=post
        comment.comment_contents=request.POST.get('comment')
        comment.comment_writer='파랑새'
        comment.comment_date=timezone.datetime.now()
        comment.save()
        return render(request, 'main/board_detail.html', {'board': post})

def commentDelete(request, board_id,comment_id):
    comment = Comment.objects.get(id=comment_id)
    comment.delete()
    board_detail = get_object_or_404(Post, pk=board_id)
    key = (board_detail.key).encode('utf-8')
    simpleEnDecrypt = SimpleEnDecrypt(key)
    decrypt_content = simpleEnDecrypt.decrypt(board_detail.content)
    board_detail.content = decrypt_content
    return render(request, 'main/board_detail.html', {'board': board_detail})


class SimpleEnDecrypt:
    def __init__(self, key=None):
        if key is None:  # 키가 없다면
            key = Fernet.generate_key()  # 키를 생성한다
        self.key = key
        self.f = Fernet(self.key)

    def encrypt(self, data, is_out_string=True):
        if isinstance(data, bytes):
            ou = self.f.encrypt(data)  # 바이트형태이면 바로 암호화
        else:
            ou = self.f.encrypt(data.encode('utf-8'))  # 인코딩 후 암호화
        if is_out_string is True:
            return ou.decode('utf-8')  # 출력이 문자열이면 디코딩 후 반환
        else:
            return ou

    def decrypt(self, data, is_out_string=True):
        if isinstance(data, bytes):
            ou = self.f.decrypt(data)  # 바이트형태이면 바로 복호화
        else:
            ou = self.f.decrypt(data.encode('utf-8'))  # 인코딩 후 복호화
        if is_out_string is True:
            return ou.decode('utf-8')  # 출력이 문자열이면 디코딩 후 반환
        else:
            return ou



