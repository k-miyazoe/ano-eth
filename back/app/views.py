from rest_framework import generics, permissions
from .models import User,Ether,Question,Answer
from .serializers import UserSerializer
from web3 import Web3
import environ,json
from django.http import JsonResponse, HttpResponseServerError


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

#イーサリアムアカウント作成処理
#passwordをフロントから受け取る
#アドレスをEtherモデルに保存する etherを作るときに必要
def createEtherAddress(password):
    eth_password = json.loads(password)
    eth_address = w3.geth.personal.new_account(eth_password)
    return JsonResponse(eth_address)

#Etherモデル作成
#csrfが必要
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
