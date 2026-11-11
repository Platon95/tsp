import sys
t=open('src/template.html').read(); f=open('src/fonts.css').read(); d=open('src/data.json').read().replace('</','<\\/')
b=t.replace('__FONTS__',f).replace('__DATA__',d)
head='<!doctype html>\n<html lang="ru">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">\n<meta name="theme-color" content="#FFFFFF">\n<meta name="description" content="ТСП: кормовые добавки, ветеринарные препараты, аминокислоты, продукция Дзержинского агрокомбината и переработка непищевого сырья. Оставьте номер, и мы перезвоним.">\n'
i=b.index('</style>')+len('</style>')
pre=b[:i].replace('<meta name="claude:viewport-fit-sides" content="cover">\n','')
open(sys.argv[1],'w').write(head+pre+'\n<style>img{max-width:100%}[hidden]{display:none!important}body{margin:0}</style>\n</head>\n<body>\n'+b[i:]+'\n</body>\n</html>\n')
