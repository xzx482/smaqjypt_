
import qrcode
import json

es={
"支付宝":"https://qr.alipay.com/fkx16486yjrwnfci0um7o32",
"微信":"wxp://f2f1cQJjDNbMoZc1x1pWGBubsDyZx2Hu-Vdm",
"QQ":"https://i.qianbao.qq.com/wallet/sqrcode.htm?m=tenpay&f=wallet&u=1493440548&a=1&n=xzx&ac=CAEQpLCQyAUYqsX1_AUgZA%3D%3D_xxx_sign",
}

def 生成(数据="hello"):
	qr =qrcode.main.QRCode(error_correction=1)
	qr.add_data(数据)
	qr.make()
	
	modcount = qr.modules_count
	ab=""
	'''
	for r in range(modcount):
		ab+=("  ")
		for c in range(modcount):
			if qr.modules[r][c]:
				ab+=("▇")
			else:
				ab+=("  ")
	print(ab)
	'''
	a=[]
	for r in range(modcount):
		b=""
		for c in range(modcount):
			if qr.modules[r][c]:
				b+="1"
			else:
				b+="0"
		a.append(int(b,2))
	return a

c={}
for i in es:
	c[i]=[es[i],生成(es[i])]
	
print(json.dumps(c,ensure_ascii=False,sort_keys=True,separators=(',',':')))
