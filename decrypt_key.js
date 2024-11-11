
var cjs = require("crypto-js");
function convertArrayToBase64(a) {
    for (var b = "", c = a.byteLength, d = 0; d < c; d++)
        b += String.fromCharCode(a[d]);
    return btoa(b)
}
function convert(a){var b=a.words;a=a.sigBytes;for(var c=new Uint8Array(a),d=0;d<a;d++)c[d]=b[d>>>2]>>>24-d%4*8&255;return c}
n = cjs
a = n.AES.decrypt
o = convertArrayToBase64
u = n.mode.ECB
d = n.enc
h = d.Hex.parse
c = n.pad.NoPadding;
apkId = process.argv[2]
timestampdata = process.argv[3]
timestampurl = process.argv[4]

var f = new Uint8Array(eval(timestampdata))
var pp = timestampurl.split('/timestamp/')[1] ?? '',
        v = f.subarray(8, 24),
        g = f.subarray(32, 48);
    if (pp === 'aav') {
        v = f.subarray(16, 32); 
        g = f.subarray(48, 64);
      } else if (pp === 'scw') {
        v = f.subarray(0, 16); 
        g = f.subarray(48, 64);
      } else if (pp === 'scs') {
        v = f.subarray(8, 24); 
        g = f.subarray(32, 48);
      } else if (pp === 'sdq') {
        g = f.subarray(0, 16); 
        v = f.subarray(48, 64);
      } else if (pp === 'sxc') {
        v = f.subarray(0, 16); 
        g = f.subarray(32, 48);
      } else if (pp === 'q1wq') {
        g = f.subarray(0, 16); 
        v = f.subarray(32, 48);
      } else if (pp === 'w1q') {
        g = f.subarray(16, 32); 
        v = f.subarray(48, 64);
      }

f = a(o(g), h(apkId.substring(16, 48)), {
        mode: u,
        padding: c,
      })

f = convert(a(o(v), f, {
    mode: u,
    padding: c
}))
this.decryptkey = new Uint8Array(f.buffer)
console.log("["+f.toString()+"]")
