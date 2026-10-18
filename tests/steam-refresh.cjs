const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');
const source = fs.readFileSync(path.join(__dirname, '../theme.qml'), 'utf8');
const functions = source.match(/^    function inspect\w+Signal\(\) \{[\s\S]*?^    \}/gm).join('\n');
const memory = new Map();
let reloads = 0;
const context = {FolderListModel: {Ready: 1},
  api: {memory: {has: key => memory.has(key), get: key => memory.get(key), set: (key, value) => memory.set(key, value)}},
  refreshSignals: {status: 1, count: 1, get: () => 'native-one.signal'},
  steamRefreshSignals: {status: 1, count: 1, get: () => 'steam-one.signal'},
  refreshInitialized: false, steamRefreshInitialized: false,
  lastRefreshToken: '', lastSteamRefreshToken: '',
  refreshMemoryKey: 'native', steamRefreshMemoryKey: 'steam',
  refreshDebounce: {restart: () => reloads++}};
vm.createContext(context); vm.runInContext(functions, context);
context.inspectRefreshSignal(); context.inspectSteamRefreshSignal();
assert.equal(reloads, 2);
assert.equal(memory.get('native'), 'native-one.signal');
assert.equal(memory.get('steam'), 'steam-one.signal');
context.inspectRefreshSignal(); context.inspectSteamRefreshSignal(); assert.equal(reloads, 2);
context.steamRefreshSignals.get = () => 'steam-two.signal'; context.inspectSteamRefreshSignal();
assert.equal(reloads, 3); assert.equal(memory.get('native'), 'native-one.signal');
context.steamRefreshSignals.count = 2; context.inspectSteamRefreshSignal(); assert.equal(reloads, 3);
assert.match(source, /folder: Qt.resolvedUrl\("steam-library-refresh"\)/);
console.log('PASS: Steam and Native Games refresh independently without touching each other\'s tokens');
