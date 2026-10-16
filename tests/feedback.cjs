const fs = require('fs'), vm = require('vm'), assert = require('assert'), path = require('path');
function moduleAt(name) {
  const ctx = {};
  vm.createContext(ctx);
  vm.runInContext(fs.readFileSync(path.join(__dirname, '../lib', name), 'utf8').replace(/^\.pragma library\s*/, ''), ctx);
  return ctx;
}
const art = moduleAt('Library.js'), hints = moduleAt('Hints.js');
const key = (code, label) => ({key:code, modifiers:0, name:()=>label});
const keys = {
  accept:[key(0x100000),key(0x1000004,'Enter')], cancel:[key(0x100001),key(0x1000000,'Esc')],
  details:[key(0x100002)], filters:[key(0x100003)], prevPage:[key(0x100004)], nextPage:[key(0x100007)]
};
assert.equal(hints.binding(keys,'details',true).face,'west');
keys.details = [key(0x100003)]; keys.filters = [key(0x100002)];
assert.equal(hints.binding(keys,'details',true).face,'north');
assert.equal(hints.binding(keys,'filters',true).face,'west');
assert.equal(hints.binding(keys,'prevPage',true).side,'left');
assert.equal(hints.binding(keys,'nextPage',true).side,'right');
assert.equal(hints.binding(keys,'accept',false).text,'Enter');
assert.equal(hints.binding({},'accept',true),null);
const state = {backend:{keys},controllerHints:true,zone:'shelf',page:0,currentGame:{},detailAction:0,keyboard:['A','DONE'],keyboardIndex:0};
let row = hints.forState(state,'');
assert(row.some(x=>x.label==='Details' && x.face==='north'));
assert(!row.filter(x=>x.kind==='arrows').some(x=>x.face));
assert(!row.some(x=>['ACCEPT','DETAILS','FILTERS','D-PAD'].includes(x.text)));
state.zone='hero';state.heroAction=1;
assert(hints.forState(state,'').some(x=>x.label==='Details' && x.face==='south'));
state.controllerHints=false;
assert(hints.forState(state,'').some(x=>x.text==='Esc' && x.label==='System menu'));
assert(hints.forState(state,'details').some(x=>x.text==='Esc' && x.label==='Back'));
state.controllerHints=true;state.keyboardIndex=1;
assert(hints.forState(state,'search').some(x=>x.label==='Search'));
assert(!hints.forState(state,'search').some(x=>x.kind==='shoulder'));
const game={assets:{screenshot:'https://dl.flathub.org/shot.png', logo:'logo.png', boxFront:'logo.png'}};
let candidates=art.artwork(game,['background','screenshot','logo','boxFront']);
assert.equal(candidates.length,2);
assert.equal(candidates[0].fit,false);assert.equal(candidates[1].fit,true);
assert.equal(art.artwork({assets:{logo:'transparent.png'}},['logo'])[0].fit,true);
assert.equal(art.artwork({assets:{}},['logo']).length,0);
console.log('PASS: real artwork and legend JavaScript, remapped bindings, keyboard/modal hints, role fit and URL deduplication');
