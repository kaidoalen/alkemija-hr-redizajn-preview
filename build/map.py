# Builds a dot-matrix SVG of Europe from Natural Earth 110m (public domain)
import json,math
g=json.load(open('/tmp/ne.geojson'))
polys=[]
for f in g['features']:
    geo=f['geometry'];cs=geo['coordinates']
    if geo['type']=='Polygon': cs=[cs]
    for p in cs: polys.append(p[0])
def inside(x,y,ring):
    c=False;n=len(ring);j=n-1
    for i in range(n):
        xi,yi=ring[i];xj,yj=ring[j]
        if (yi>y)!=(yj>y) and x<(xj-xi)*(y-yi)/(yj-yi)+xi: c=not c
        j=i
    return c
W0,W1,N0,N1=-11,34,31.2,62  # lon/lat bbox
def proj(lon,lat):
    x=(lon-W0)*math.cos(math.radians(48))*10
    y=(N1-lat)*10
    return x,y
bb=[(min(p[0] for p in r),max(p[0] for p in r),min(p[1] for p in r),max(p[1] for p in r)) for r in polys]
dots=[]
step=0.62
lat=N1
while lat>N0:
    lon=W0
    while lon<W1:
        for r,b in zip(polys,bb):
            if b[0]<=lon<=b[1] and b[2]<=lat<=b[3] and inside(lon,lat,r):
                dots.append(proj(lon,lat));break
        lon+=step/math.cos(math.radians(lat))*0.75
    lat-=step*0.75
VW,VH=proj(W1,N0)
cities={'Zagreb':(15.98,45.81),'Milano':(9.19,45.46),'Wien':(16.37,48.21),'München':(11.58,48.14),'Paris':(2.35,48.86),'Amsterdam':(4.9,52.37),'Madrid':(-3.7,40.42),'Warszawa':(21.01,52.23),'Budapest':(19.04,47.5),'Beograd':(20.46,44.79),'Ljubljana':(14.5,46.05),'Sarajevo':(18.41,43.86),'Bruxelles':(4.35,50.85),'Roma':(12.5,41.9),'Athina':(23.73,37.98),'Rabat':(-6.84,34.02),'Podgorica':(19.26,42.44),'Pristina':(21.17,42.66),'Skopje':(21.43,42.0),'Tunis':(10.18,36.8)}
json.dump({'w':VW,'h':VH,'dots':[(round(x,1),round(y,1)) for x,y in dots],'cities':{k:tuple(round(v,1) for v in proj(*c)) for k,c in cities.items()}},open('/workspace/alkemija-hr-redizajn-20261111/build/map.json','w'))
print(len(dots),VW,VH)
