var crypto = require('./cryptojs/cryptojs.js').Crypto

const json2form = json => {
  var str = [];
  for (var p in json) {
    str.push(encodeURIComponent(p) + "=" + encodeURIComponent(json[p]));
  }
  return str.join("&");
}

const encodeUTF8 = text => {
  const code = encodeURIComponent(text);
  const bytes = [];
  for (var i = 0; i < code.length; i++) {
    const c = code.charAt(i);
    if (c === '%') {
      const hex = code.charAt(i + 1) + code.charAt(i + 2);
      const hexVal = parseInt(hex, 16);
      bytes.push(hexVal);
      i += 2;
    } else bytes.push(c.charCodeAt(0));
  }
  return bytes;
}

const decodeUTF8 = bytes => {
  var encoded = "";
  for (var i = 0; i < bytes.length; i++) {
    encoded += '%' + bytes[i].toString(16);
  }
  return decodeURIComponent(encoded);
}

function base64_encode(str) { // 编码，配合encodeURIComponent使用
  var c1, c2, c3;
  var base64EncodeChars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=";
  var i = 0, len = str.length, strin = '';
  while (i < len) {
    c1 = str.charCodeAt(i++) & 0xff;
    if (i == len) {
      strin += base64EncodeChars.charAt(c1 >> 2);
      strin += base64EncodeChars.charAt((c1 & 0x3) << 4);
      strin += "==";
      break;
    }
    c2 = str.charCodeAt(i++);
    if (i == len) {
      strin += base64EncodeChars.charAt(c1 >> 2);
      strin += base64EncodeChars.charAt(((c1 & 0x3) << 4) | ((c2 & 0xF0) >> 4));
      strin += base64EncodeChars.charAt((c2 & 0xF) << 2);
      strin += "=";
      break;
    }
    c3 = str.charCodeAt(i++);
    strin += base64EncodeChars.charAt(c1 >> 2);
    strin += base64EncodeChars.charAt(((c1 & 0x3) << 4) | ((c2 & 0xF0) >> 4));
    strin += base64EncodeChars.charAt(((c2 & 0xF) << 2) | ((c3 & 0xC0) >> 6));
    strin += base64EncodeChars.charAt(c3 & 0x3F)
  }
  return strin
}

const encryptPasswd = pwd => {
  let bytes = crypto.SHA1(pwd, {asBytes:true})
  let str = crypto.SHA1(pwd, { asString: true })
  console.log("SHA1:" + str)
  console.log("SHA1:" + crypto.SHA1(pwd))
  let encrypted = crypto.util.bytesToBase64(bytes)
  console.log('base64:' + encrypted)
  console.log('new base64:' + base64_encode(str))
  return encrypted
}

const bytes2Str = bytes => {
  for (var str = [], i = 0; i < bytes.length; i++)
    str.push(String.fromCharCode(bytes[i]));
  return str.join("");
}

const getcurDateFormatString = date => {
  let datestr = date.toLocaleDateString()
  let dateArr = datestr.split('/')
  for (let i = 1; i <= 2; i++) {
    if (dateArr[i].length < 2) {
      dateArr[i] = "0" + dateArr[1]
    }
  }
  return dateArr.join('-')
}


module.exports = {
  json2form: json2form,
  encodeUTF8: encodeUTF8,
  decodeUTF8: decodeUTF8,
  encryptPasswd: encryptPasswd,
  bytes2Str: bytes2Str,
  getcurDateFormatString: getcurDateFormatString
}