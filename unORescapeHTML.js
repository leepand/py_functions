//将服务端字符串中特殊字符互相转化  " ' < > 等
/**
 * @function escapeHTML 转义html脚本 < > & " '
 * @param a  字符串   
 */
 
function escapeHTML(a){
    a = "" + a;
    return a..replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;").replace(/'/g, "&apos;");
}
 
 
 
/**
 * @function unescapeHTML 还原html脚本 < > & " '
 * @param a  字符串
 */
function unescapeHTML(a){
    a = "" + a;
    return a.replace(/&lt;/g, "<").replace(/&gt;/g, ">").replace(/&amp;/g, "&").replace(/&quot;/g, '"').replace(/&apos;/g, "'");
}