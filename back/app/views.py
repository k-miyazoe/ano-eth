from rest_framework import generics, permissions
from .models import User,Ether,Question,Answer
from .serializers import UserSerializer,EtherSerializer,QuestionSerializer,AnswerSerializer
from web3 import Web3
import environ,json
from django.http import JsonResponse, HttpResponseServerError
from django.views.decorators.csrf import csrf_exempt


env = environ.Env()
env.read_env('back.env')

#remote provider sets
w3 = Web3(Web3.HTTPProvider(env('GETH_REMOTE_PROVIDERS')))

class UserList(generics.ListAPIView):
    queryset = User.objects.all().order_by('id')
    serializer_class = UserSerializer
    #管理者のみユーザーリスト確認可能
    #permission_classes = (permissions.IsAdminUser,)

class UserCreate(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
class UserRetrieveUpdate(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    #permission_classes = (permissions.IsAuthenticated, )

#イーサリアムアドレス作成処理[未完成]
############################################################################
@csrf_exempt
def createEtherAddress(request):
    if request.body:
        json_dict = json.loads(request.body)
        eth_password = json_dict['password']
        eth_address = w3.geth.personal.new_account(eth_password)
        return JsonResponse({"ether_address": eth_address})
    else:
        return HttpResponseServerError()
        
#仮想通貨送金処理
#defaultでは300秒間アカウントロックが解除される durationが0なら無期限解除になる
def sendTransaction(to,value,password):
    transaction = {
        'to':to,
        'from': w3.eth.coinbase,
        'value': value
    }
    #送り主はminer
    #w3.geth.personal.unlock_account('0xd3CdA913deB6f67967B99D67aCDFa1712C293601', password)
    #ロック解除時間がもしみじかいならのち増やす
    w3.geth.personal.unlock_account(w3.eth.coinbase, password)
    w3.geth.personal.send_transaction(transaction, password)
    w3.geth.personal.lock_account(w3.eth.coinbase)

#Etherモデル作成 シリアライザーを作成
#user_idが外部キーなのでそこの振る舞い方のちがいが発生するかも
def postCreateEther(request):
    #ユーザーが設定したパスワードとそのパスワードによって作られたアドレス、ユーザー名,正アカウント、アカウント名が必要
    json_dict = json.loads(request)
    #''中身をvue側とそろえる
    user_id = json_dict['user_id'] #引数に依存
    #addressはpasswordを使ってcreatEtherAddress()を使うかも
    ether_address = json_dict['address'] #パスワード,関数に依存
    ether_password = json_dict['password'] #引数に依存
    ether_wallet = 0 #依存なし
    ether_anonymous = json_dict['anonymous'] #現在のetherアカウント所持数に依存
    ether_account_name = json_dict['account_name'] #ぜんざいのehterアカウント所持数に依存
    #Todo.objects.create(task=task, due=due, done=done)
    #すでにアカウントが存在する場合、returnさせる
    Ether.ojbects.create(user_id=user_id,ether_address=ether_address,ether_password=ether_password,ether_wallet=ether_wallet,ether_anonymous=ether_anonymous,ether_account_name=ether_account_name)

##############################################################################

#Etherモデル確認
class EtherGet(generics.ListAPIView):
    serializer_class = EtherSerializer
    
    def get_queryset(self):
        u_id = self.kwargs.get("user_id")
        return Ether.objects.filter(user_id=u_id)

#Etherモデル生成
class EtherCreate(generics.CreateAPIView):
    queryset = Ether.objects.all()
    serializer_class = EtherSerializer
    
class EtherRetrieveUpdate(generics.RetrieveUpdateAPIView):
    queryset = Ether.objects.all()
    serializer_class = EtherSerializer
    #permission_classes = (permissions.IsAuthenticated, )

#Question
class QuestionList(generics.ListAPIView):
    #投稿時間が新しい順に変更したい
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    
    def get_queryset(self):
        flag = self.kwargs.get("flag")
        if flag == "unresolved":
            return Question.objects.filter(question_status=False)
        elif flag == "resolved":
            return Question.objects.filter(question_status=True)
        #未完成
        elif flag == "my-question":
            return Question.objects.filter()
        else:
            return Question.objects.all()

class QuestionCreate(generics.CreateAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

#1つの質問を取得 + 更新
class QuestionGet(generics.RetrieveUpdateAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    
#解決や評価に使用
class QuestionUpdate(generics.UpdateAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

#自身の質問のみ編集可能 使用するか未定
class QuestionUpdateOnlyCreater(generics.UpdateAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

#質問検索機能
class QuestionSearch(generics.ListAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    def get_queryset(self):
        keyword = self.kwargs.get("question_content")
        return Question.objects.filter(question_content__icontains=keyword)
 
#Answer
#特定の質問に対する回答をすべて取得
class AnswerGet(generics.ListAPIView):
    serializer_class = AnswerSerializer
    
    def get_queryset(self):
        q_id = self.kwargs.get("question_id")
        return Answer.objects.filter(question_id=q_id)
    
class AnswerCreate(generics.CreateAPIView):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer

class AnswerUpdate(generics.UpdateAPIView):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer