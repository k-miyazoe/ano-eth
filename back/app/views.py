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
    permission_classes = (permissions.IsAdminUser,)

class UserCreate(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
class UserRetrieveUpdate(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated, )

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
class EtherList(generics.ListAPIView):
    queryset = Ether.objects.all().order_by('id')
    serializer_class = EtherSerializer
    # #管理者のみユーザーリスト確認可能
    # permission_classes = (permissions.IsAdminUser,)

#Etherモデル生成
class EtherCreate(generics.CreateAPIView):
    queryset = Ether.objects.all()
    serializer_class = EtherSerializer
    

#Question
class QuestionList(generics.ListAPIView):
    #投稿時間が新しい順に変更したい
    queryset = Question.objects.all().order_by('id')
    serializer_class = QuestionSerializer

class QuestionCreate(generics.CreateAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

#updateを使ってみた
class QuestionUpdate(generics.UpdateAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    
#Answer
#一つの質問に対する複数の回答を取得するクラスを作成する
#投稿時間が新しい順に変更したい
#特定の回答を取得する
#lookup_field no
#ListAPIView -> RetrieveAPIView 1つしか返せない
#MultipleFieldLookupMixin
#引数をもらって，実行する(シリアライザーを使用しない)
class AnswerGet(generics.ListAPIView):
    #queryset = Answer.objects.all()
    queryset = Answer.objects.filter(question_id=0)
    serializer_class = AnswerSerializer
    lookup_field = 'question_id'   
    
class AnswerCreate(generics.CreateAPIView):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer

#updateを使ってみた
class AnswerUpdate(generics.UpdateAPIView):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializer