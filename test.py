from Tools import identdict

s="{data: '75bad476e35b8827e55e1fedf1bd4589',time: '1653809731312',enc: '4589C22A239522A298A61C0D41D87F82',displayName:'周良宇',userRole:'3',group1:'',mobilePhone:''}"
d = eval(s, identdict())
print(d)