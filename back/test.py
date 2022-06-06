from web3 import Web3,HTTPProvider

#https://eagle4.fu.is.saga-u.ac.jp/geth-docker/
w3 = Web3.HTTPProvider('http://127.0.0.1:8545')

print('接続確認',w3.isConnected())