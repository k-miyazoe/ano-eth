import Axios from "axios";
import Cookies from "js-cookie";

function setHeader() {
    const csrftoken = Cookies.get("csrftoken");
    let axios = Axios.create({
        baseURL: process.env.VUE_APP_API_URL,
        timeout: 2500,
        headers: {
            "Content-Type": "application/json",
            //Authorization: jwt,
            "X-CSRFToken": csrftoken,
        },
    });
    return axios
}

//関数をexport
export default {
    setHeader,
};