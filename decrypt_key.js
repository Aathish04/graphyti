var cjs = require("crypto-js");

// Add required shims
cjs.enc.u8array = {stringify:function (a){var b=a.words;a=a.sigBytes;for(var c=new Uint8Array(a),d=0;d<a;d++)c[d]=b[d>>>2]>>>24-d%4*8&255;return c}}
global.window = {
    cjs: cjs,
    convertArrayToBase64: function (a) {
        for (var b = "", c = a.byteLength, d = 0; d < c; d++)
            b += String.fromCharCode(a[d]);
        return btoa(b)
    },
    apkId: process.argv[2]
};
global.self = global;


const Hls = require('./hls.min.js');
const hls = new Hls();

r = { // shim of result object
    frag:{
        decryptdata:{}
    }
}
t = { // shim of request/response object after getting the timestamp key data
    url:process.argv[4],
    data: new Uint8Array(eval(process.argv[3]))
}

for (var controller of hls.networkControllers){
    if(controller.hasOwnProperty("decryptkey")){
        controller.loadsuccess(t,1,r)
        console.log("["+r.frag.decryptdata.key.toString()+"]")
    }
}
