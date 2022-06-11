function changeTimestamp(object) {
    for (let item in object) {
        let date = item.question_post_time
        let year_str = date.getFullYear();
        //月だけ+1すること
        let month_str = 1 + date.getMonth();
        let day_str = date.getDate();
        let hour_str = date.getHours();
        let minute_str = date.getMinutes();
        let second_str = date.getSeconds();

        format_str = 'YYYY-MM-DD hh:mm:ss';
        format_str = format_str.replace(/YYYY/g, year_str);
        format_str = format_str.replace(/MM/g, month_str);
        format_str = format_str.replace(/DD/g, day_str);
        format_str = format_str.replace(/hh/g, hour_str);
        format_str = format_str.replace(/mm/g, minute_str);
        format_str = format_str.replace(/ss/g, second_str);
        item = format_str
    }
    //return new object
    console.log(object)
    return object
}

//関数をexport
export default {
    changeTimestamp,
};