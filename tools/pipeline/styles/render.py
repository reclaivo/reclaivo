import asyncio,sys,os
from playwright.async_api import async_playwright
url,out,total=sys.argv[1],sys.argv[2],float(sys.argv[3]);times=[float(x) for x in sys.argv[4:]]
FPS=30;os.makedirs(out,exist_ok=True)
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(args=['--use-angle=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist','--use-gl=angle'])
        pg=await b.new_page(viewport={'width':1080,'height':1920})
        pg.on('pageerror',lambda e:print('err',str(e)[:300]));pg.on('console',lambda m:print('c',m.text[:200]) if m.type=='error' else None)
        await pg.goto(url);await pg.wait_for_function('window.ready===true',timeout=120000)
        if times:
            for t in times:
                await pg.evaluate(f'setT({t})');await pg.screenshot(path=f'{out}/t_{t:05.2f}.png')
        else:
            N=int(total*FPS)
            for i in range(N):
                await pg.evaluate(f'setT({i/FPS})');await pg.screenshot(path=f'{out}/{i:04d}.jpg',type='jpeg',quality=95)
        await b.close()
asyncio.run(main())
