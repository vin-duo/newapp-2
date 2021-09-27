import math


class Regressao():
	def __init__(self, valores_alfa=[], valores_resistencia=[],  valores_ac=[], valores_m=[],valores_C=[], arredondamento=3):
		self.alfa=valores_alfa
		self.valores_resistencia_log=tuple(map(lambda var: math.log10(var), valores_resistencia))
		self.valores_ac=valores_ac
		self.valores_m=valores_m
		self.valores_C=valores_C
		self.log_resistencias=[]
		self.arredondamento=arredondamento

	def media(self, x):
		media=sum(x)/len(x)
		return(media)

	def linear(self,x,y):
		media_x = self.media(x)
		media_y = self.media(y)
		sxx = 0
		sxy = 0
		for i in range(len(x)):
			xix = x[i] - media_x
			yiy = y[i] - media_y
			xix2 = xix**2
			xixyiy = xix*yiy
			sxx = sxx + xix2
			sxy = sxy + xixyiy
		b = sxy / sxx
		a = media_y - b * media_x
		return(a,b)

	def k1(self):
		k1 = 10**self.linear(self.valores_ac,self.valores_resistencia_log)[0]
		return round(k1,self.arredondamento)

	def k2(self):
		k2 = 1/(10**self.linear(self.valores_ac,self.valores_resistencia_log)[1])
		return round(k2,self.arredondamento)

	def k3(self):
		k3 = self.linear(self.valores_ac,self.valores_m)[0]
		return round(k3,self.arredondamento)

	def k4(self):
		k4 = self.linear(self.valores_ac,self.valores_m)[1]
		return round(k4,self.arredondamento)

	def k5(self):
		k5 = self.linear(self.valores_m,self.valores_C)[0]
		return round(k5,self.arredondamento)

	def k6(self):
		k6 = self.linear(self.valores_m,self.valores_C)[1]
		return round(k6,self.arredondamento)

'''
va = [1,2,3]
vr = [38,28,20]
vac = [0.41,0.55,0.7]
vm = [4,5,6]
vc = [472,371,309]

r = Regressao(va,vr,vac,vm,vc)

print(r.k1())
print(r.k2())
print(r.k3())
print(r.k4())
print(r.k5())
print(r.k6())

va = [1,2,3]
vr = [57.5,43.7,31.4]
vac = [0.36,0.42,0.49]
vm = [3,4,5]
vc = [479,371,295]
r = Regressao(va,vr,vac,vm,vc)
print('\n')
print(r.k1())
print(r.k2())
print(r.k3())
print(r.k4())
print(r.k5())
print(r.k6())
'''
