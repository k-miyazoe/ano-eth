import Web3 from "web3";

function createEtherUser(password) {
    var web3 = new Web3();
    let eth_id = ""
    let eth_password = password
    let eth_objetct = {}
    //後で環境変数に書き換える
    const host = "https://eagle4.fu.is.saga-u.ac.jp/geth-docker/"
    web3.setProvider(new Web3.providers.HttpProvider(host));
    //acount作成
    web3.eth.personal.newAccount(password).then(
        (data) => {
            ether_id_save = data;
            console.log("etherアカウント作成ok", data);
            //data(etheridとpasswordをobjectで返す)
            //返した後vue側でobjectに要素を追加する必要がある
            return 0;
        },
        (err) => {
            console.log("error", err);
        }
    );
}

//関数をexport
export default {
    createEtherUser,
};