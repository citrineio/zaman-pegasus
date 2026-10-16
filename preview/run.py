#!/usr/bin/env python3
"""Render and exercise the real theme against a small Pegasus API mock.

pip install PyQt5  # Qt 5, closest to the target Pegasus runtime
python3 preview/run.py --test --output preview/home.png
python3 preview/run.py --qt6 --test --output preview/home-qt6.png
python3 preview/run.py --interactive
"""
import argparse
import json
import os
import sys
from pathlib import Path

p = argparse.ArgumentParser()
p.add_argument('--qt6', action='store_true')
p.add_argument('--test', action='store_true')
p.add_argument('--interactive', action='store_true')
p.add_argument('--output')
p.add_argument('--page', default='home', choices=['home','library','favorites','preferences','details','search','collections'])
p.add_argument('--mode', default='normal')
p.add_argument('--hero-action', choices=['play','details'])
p.add_argument('--width', type=int, default=1920)
p.add_argument('--height', type=int, default=1080)
a = p.parse_args()
if not a.interactive:
    os.environ.setdefault('QT_QPA_PLATFORM', 'offscreen')
    os.environ.setdefault('QT_QUICK_BACKEND', 'software')
    os.environ.setdefault('QSG_RENDER_LOOP', 'basic')
if a.qt6:
    from PySide6.QtCore import Qt, QUrl, QObject, QPointF, qInstallMessageHandler, qVersion
    from PySide6.QtGui import QGuiApplication
    from PySide6.QtQuick import QQuickView
    from PySide6.QtQml import QQmlExpression, QQmlEngine
    from PySide6.QtTest import QTest
else:
    from PyQt5.QtCore import Qt, QUrl, QObject, QPointF, qInstallMessageHandler, qVersion
    from PyQt5.QtGui import QGuiApplication
    from PyQt5.QtQuick import QQuickView
    from PyQt5.QtQml import QQmlExpression, QQmlEngine
    from PyQt5.QtTest import QTest

messages = []
def log(kind, context, message):
    if 'XDG_RUNTIME_DIR' not in message:
        messages.append(message)
        print(message, file=sys.stderr)
qInstallMessageHandler(log)
app = QGuiApplication(sys.argv)
view = QQuickView()
view.setResizeMode(QQuickView.SizeRootObjectToView)
view.resize(a.width, a.height)
view.setSource(QUrl.fromLocalFile(str(Path(__file__).with_name('Preview.qml').resolve())))
if view.status() == QQuickView.Error:
    raise SystemExit(1)
view.show()
view.requestActivate()
QTest.qWait(500)
root = view.rootObject()
shell = root.findChild(QObject, 'zamanShell')
assert shell is not None
def js(code):
    expression = QQmlExpression(QQmlEngine.contextForObject(root), root, code)
    result = expression.evaluate()
    if expression.hasError():
        raise RuntimeError(expression.error().toString())
    if isinstance(result, tuple):
        result = result[0]
    if hasattr(result, 'toVariant'):
        result = result.toVariant()
    return result
def key(name, repeat=1):
    for _ in range(repeat):
        QTest.keyClick(view, getattr(Qt, 'Key_'+name))
        QTest.qWait(10)
def check(code, message):
    assert js(code), message
def item_center(name, x=0.5, y=0.5):
    item = root.findChild(QObject, name)
    assert item is not None, name
    return item.mapToScene(QPointF(item.width() * x, item.height() * y)).toPoint()
def click_item(name, x=0.5, y=0.5):
    center = item_center(name, x, y)
    QTest.mouseClick(view, Qt.LeftButton, pos=center)
    QTest.qWait(50)
def reset(mode='normal'):
    js('mock.populate('+json.dumps(mode)+'); shell.modal=""; shell.notice=""; shell.page=0; shell.query=""; shell.collectionName=""; shell.sortMode=0; shell.homeIndex=0; shell.heroAction=0; shell.gameIndex=0; shell.zone="shelf"; shell.launching=false; shell.rebuild(); shell.forceActiveFocus()')
    QTest.qWait(80)

reset(a.mode)
if a.test:
    reset()
    js('preview.escapedToHost=0')
    key('Escape'); check('preview.escapedToHost===1 && shell.zone==="shelf"', 'Escape reaches Pegasus from Home')
    js('shell.switchPage(1); shell.zone="grid"')
    key('Escape'); check('preview.escapedToHost===2 && shell.page===1 && shell.zone==="grid"', 'Escape reaches Pegasus from Library')
    js('shell.showDetails(shell.currentGame)')
    key('Escape'); check('shell.modal==="" && preview.escapedToHost===2', 'Escape closes theme dialog first')
    reset()
    check('shell.homeGames.length === 18 && shell.currentGame.title === "Dune Runner"', 'recent games')
    key('Right'); check('shell.currentGame.title === "Orbital"', 'D-pad selection')
    key('I'); check('shell.modal === "details"', 'details action')
    key('Right'); key('Return'); check('shell.detailGame.favorite === true', 'favorite toggle')
    key('Escape'); check('shell.modal === "" && shell.homeIndex === 1', 'details back restores selection')
    key('Return'); check('mock.launchCount === 1 && mock.lastLaunched === "Orbital"', 'launch exact selected game')
    key('Return'); check('mock.launchCount === 1', 'duplicate launch guard')
    check('mock.launchMemory["zaman.v1"].identity === "/preview/1.rom"', 'persist stable launch identity')
    js('shell.homeIndex=0; shell.restore()'); check('shell.homeIndex===1', 'restore selection')
    key('Up',2); key('Right'); check('shell.page===1 && shell.zone==="nav"', 'tab navigation')
    key('Down'); key('Return'); check('shell.modal==="collections"', 'collection picker')
    key('Down'); key('Return'); check('shell.filteredGames.length===6 && shell.collectionName==="16-bit collection"', 'collection membership filter')
    key('F'); check('shell.modal==="search"', 'controller search')
    # Type D using the on-screen keyboard, then navigate to DONE.
    key('Right',3); key('Return'); check('shell.draftQuery==="D"', 'on-screen keyboard input')
    key('Down',3); key('Right',6); key('Return')
    check('shell.modal==="" && shell.query==="D" && shell.filteredGames.length===3', 'apply controller search')
    key('F'); key('Backspace'); key('Z'); key('Down',3); key('Right',9); key('Return')
    check('shell.filteredGames.length===0', 'empty search result')
    key('Up'); check('shell.zone==="filters"', 'empty result escape path')
    reset('empty'); key('Return'); key('I'); key('Right'); check('shell.currentGame===null && shell.modal===""', 'empty library input safe')
    reset('single'); key('Right',3); check('shell.homeIndex===0', 'single game clamps navigation')
    reset('unplayed'); check('!shell.hasRecent && shell.homeGames.length===18', 'new library fallback')
    reset('noart'); key('I'); check('shell.detailGame.assets.banner===undefined', 'missing artwork fallback')
    reset('missing'); key('Return'); check('shell.notice!==""', 'missing ROM blocked')
    reset('long'); key('I'); key('Down',3); check('shell.modal==="details"', 'long description navigable')
    reset(); js('shell.switchPage(2); shell.zone="grid"'); check('shell.filteredGames.length===5', 'favorites page')
    # Remove every favorite through the detail UI, including the final item.
    for _ in range(5):
        key('I'); key('Right'); key('Return'); key('Escape')
    check('shell.filteredGames.length===0 && shell.currentGame===null', 'last favorite removal')
    js('shell.switchPage(3); shell.enterContent()'); key('Return'); check('shell.reducedMotion===false', 'preferences persist')
    key('Down'); key('Return'); check('shell.columns===5', 'density preference')
    reset('large'); js('shell.switchPage(1); shell.enterContent(); shell.move(0,1)'); check('shell.filteredGames.length===10000', 'large library model')
    key('PageDown'); check('shell.gameIndex===10', 'page navigation')
    # Change model while running, then allow the model notifications to rebuild.
    js('mock.populate("single")'); QTest.qWait(150); check('shell.games.length===1 && shell.gameIndex===0', 'model change reclamps selection')
    reset()
    key('Right'); key('Up')
    check('shell.zone==="hero" && shell.heroAction===0 && shell.currentGame.title==="Orbital"', 'controller reaches hero actions')
    key('Right'); key('Return')
    check('shell.modal==="details" && shell.detailGame.title==="Orbital"', 'controller hero details')
    key('Escape'); key('Down')
    check('shell.zone==="shelf" && shell.homeIndex===1', 'hero returns to selected recent game')
    key('Up'); key('Left')
    before = js('mock.launchCount')
    key('Return')
    check('mock.launchCount===' + str(before+1) + ' && mock.lastLaunched==="Orbital"', 'controller hero play')

    for size in [(1920,1080),(1280,720),(1280,800)]:
        view.resize(*size); QTest.qWait(100); reset()
        click_item('heroDetails')
        check('shell.modal==="details" && shell.detailGame.title==="Dune Runner"', 'hero details mouse click '+str(size))
        key('Escape')
        before = js('mock.launchCount')
        click_item('heroPlay')
        check('mock.launchCount===' + str(before+1) + ' && mock.lastLaunched==="Dune Runner" && shell.modal===""', 'hero play mouse click '+str(size))
        click_item('heroPlay')
        check('mock.launchCount===' + str(before+1), 'hero pointer duplicate launch blocked')
        reset(); click_item('heroArtworkInput',0.85,0.5)
        check('shell.modal==="details"', 'hero artwork opens details')
        reset()
        before = js('mock.launchCount')
        start = item_center('heroPlay',0.25,0.5)
        end = item_center('heroPlay',0.75,0.5)
        QTest.mousePress(view, Qt.LeftButton, pos=start); QTest.qWait(20)
        QTest.mouseMove(view, end); QTest.mouseRelease(view, Qt.LeftButton, pos=end); QTest.qWait(50)
        check('mock.launchCount===' + str(before+1) + ' && shell.modal===""', 'button release within bounds')
        if a.qt6:
            touch_device = QTest.createTouchDevice()
            reset()
            center = item_center('heroDetails')
            sequence = QTest.touchEvent(view, touch_device)
            sequence.press(0, center, view).commit(); QTest.qWait(20)
            sequence.release(0, center, view).commit(); QTest.qWait(50)
            check('shell.modal==="details"', 'hero details touchscreen tap '+str(size))
            key('Escape')
            before = js('mock.launchCount')
            center = item_center('heroPlay')
            sequence.press(0, center, view).commit(); QTest.qWait(20)
            sequence.release(0, center, view).commit(); QTest.qWait(50)
            check('mock.launchCount===' + str(before+1) + ' && shell.modal===""', 'hero play touchscreen tap '+str(size))
    view.resize(a.width,a.height); QTest.qWait(100)
    print('PASS: navigation, Escape propagation, hero controller/mouse/artwork actions, scaled hit areas, duplicate guard, search, filters, favorites, restoration, data edge cases, preferences, 10,000 games, model refresh')
    reset(a.mode)
    js('shell.reducedMotion=true; shell.compact=false')

if a.page in ['library','favorites','preferences']:
    js('shell.switchPage('+str(['home','library','favorites','preferences'].index(a.page))+'); shell.enterContent();')
    if a.page != 'preferences': js('shell.zone="grid"')
elif a.page == 'details': js('shell.showDetails(shell.currentGame)')
elif a.page == 'search': js('shell.openSearch()')
elif a.page == 'collections': js('shell.openPicker()')
if a.hero_action and a.page == 'home':
    js('shell.zone="hero"; shell.heroAction='+str(0 if a.hero_action == 'play' else 1))
    QTest.mouseMove(view, item_center('heroPanel',0.99,0.99))
QTest.qWait(700)
if a.output:
    dest = Path(a.output).resolve(); dest.parent.mkdir(parents=True, exist_ok=True)
    shot = view.grabWindow()
    if shot.isNull():
        result = root.grabToImage()
        for _ in range(50):
            QTest.qWait(50)
            shot = result.image()
            if not shot.isNull(): break
    if not shot.save(str(dest)):
        raise RuntimeError('Screenshot failed')
    print('Saved', dest)
print('Qt', qVersion())
errors = [m for m in messages if any(x in m for x in ['Error:', 'is not a type', 'Binding loop', 'Unable to assign', 'Cannot assign', 'Cannot read', 'Cannot call', 'QML Image:'])]
if errors:
    raise SystemExit('QML errors: '+ '\n'.join(errors))
if a.interactive:
    raise SystemExit(app.exec() if a.qt6 else app.exec_())
