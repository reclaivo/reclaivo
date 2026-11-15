import asyncio,os,shutil,sys,json
from playwright.async_api import async_playwright
from PIL import Image
R=sys.argv[1];only=sys.argv[2:]
cf=json.load(open(f'/tmp/vid5/{R}/cuts.json'));shutil.copy(f'/tmp/vid5/{R}/cuts.json',f'/tmp/t3d/cut_{R}.json')
FPS=cf['fps'];N=int(cf['total']*FPS);D=f'/tmp/vid5/{R}/ins';os.makedirs(D,exist_ok=True)
blank=f'{D}/blank.png';Image.new('RGBA',(1080,1920),(0,0,0,0)).save(blank)
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(args=['--use-angle=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist','--use-gl=angle'])
        pg=await b.new_page(viewport={'width':1080,'height':1920})
        pg.on('pageerror',lambda e:print('err',str(e)[:300]))
        await pg.goto(f'http://localhost:8123/insert.html?r={R}');await pg.wait_for_function('window.ready===true',timeout=120000)
        for i in range(N):
            t=i/FPS;f=f'{D}/{i:04d}.png'
            inw=(cf['c3'][0]<=t<cf['c3'][1]) or (cf['c6'][0]<=t<cf['c6'][1])
            if only and str(i) not in only: continue
            if inw:
                await pg.evaluate(f'setT({t})');await pg.screenshot(path=f,omit_background=True)
            else:
                shutil.copy(blank,f)
        await b.close()
asyncio.run(main());print('ins done',R)
