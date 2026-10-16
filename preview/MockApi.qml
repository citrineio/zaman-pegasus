import QtQuick 2.12

QtObject {
    id: mock
    property int launchCount: 0
    property string lastLaunched: ""
    property var launchMemory: ({})
    property QtObject device: QtObject { property real batteryPercent: NaN; property bool batteryCharging: false }
    property QtObject memory: QtObject {
        property var values: ({})
        function get(key) { return values[key]; }
        function has(key) { return values[key] !== undefined; }
        function set(key, value) { values[key] = value; }
        function unset(key) { delete values[key]; }
    }
    property QtObject keys: QtObject {
        property var accept: [{key: 0x100000, modifiers: 0}, {key: Qt.Key_Return, modifiers: 0, label: "Enter"}]
        property var cancel: [{key: 0x100001, modifiers: 0}, {key: Qt.Key_Escape, modifiers: 0, label: "Esc"}]
        property var details: [{key: 0x100002, modifiers: 0}, {key: Qt.Key_I, modifiers: 0, label: "I"}]
        property var filters: [{key: 0x100003, modifiers: 0}, {key: Qt.Key_F, modifiers: 0, label: "F"}]
        property var prevPage: [{key: 0x100004, modifiers: 0}, {key: Qt.Key_Q, modifiers: 0, label: "Q"}]
        property var nextPage: [{key: 0x100007, modifiers: 0}, {key: Qt.Key_E, modifiers: 0, label: "E"}]
        function isAccept(e) { return e.key === Qt.Key_Return || e.key === Qt.Key_Enter; }
        function isCancel(e) { return e.key === Qt.Key_Escape; }
        function isDetails(e) { return e.key === Qt.Key_I; }
        function isFilters(e) { return e.key === Qt.Key_F; }
        function isNextPage(e) { return e.key === Qt.Key_E; }
        function isPrevPage(e) { return e.key === Qt.Key_Q; }
        function isPageUp(e) { return e.key === Qt.Key_PageUp; }
        function isPageDown(e) { return e.key === Qt.Key_PageDown; }
    }
    property Component modelFactory: Component {
        QtObject {
            property var items: []
            readonly property int count: items.length
            function get(i) { return items[i] || null; }
            function toVarArray() { return items.slice(); }
        }
    }
    property Component collectionFactory: Component {
        QtObject {
            property string name
            property string shortName
            property var games
        }
    }
    property Component gameFactory: Component {
        QtObject {
            property string title
            property string sortBy: title
            property string developer: "Zaman preview studio"
            property string genre: "Adventure"
            property string summary: ""
            property string description: summary
            property int releaseYear: 0
            property int players: 1
            property bool favorite: false
            property bool missing: false
            property int playCount: 0
            property int playTime: 0
            property date lastPlayed
            property var assets: ({})
            property var collections
            property var files
            function launch() { mock.launchCount++; mock.lastLaunched = title; mock.launchMemory = JSON.parse(JSON.stringify(mock.memory.values)); }
        }
    }
    property QtObject allGames: modelFactory.createObject(mock)
    property QtObject collections: modelFactory.createObject(mock)
    function populate(mode) {
        var specs = [
            ["Dune Runner", "dune", "Cross the quiet dunes. Follow the last signal home.", "Exploration"],
            ["Orbital", "orbital", "One small ship. A sky full of possibilities.", "Arcade"],
            ["The Last Garden", "garden", "Bring life back to a forgotten world.", "Adventure"],
            ["Neon Circuit", "circuit", "Find your line through the city after dark.", "Racing"],
            ["Deep Current", "current", "There is a whole world beneath the surface.", "Exploration"],
            ["Ember Trail", "ember", "A trail of sparks leads into the unknown.", "Platformer"]
        ];
        var cs = [];
        for (var c = 0; c < 3; ++c) cs.push(collectionFactory.createObject(mock, {name: ["16-bit collection", "Arcade collection", "Handheld collection"][c], shortName: "preview" + c, games: modelFactory.createObject(mock)}));
        var gs = [];
        var total = mode === "empty" ? 0 : mode === "large" ? 10000 : mode === "single" ? 1 : 18;
        for (var i = 0; i < total; ++i) {
            var spec = specs[i % specs.length];
            var game = gameFactory.createObject(mock, {
                title: spec[0] + (i >= 6 ? " " + (Math.floor(i / 6) + 1) : ""),
                summary: spec[2], description: spec[2] + "\n\nThis fictional game is included only as preview data. The installed theme uses your own library, metadata and artwork.",
                genre: spec[3], favorite: i % 4 === 0,
                playCount: mode === "unplayed" ? 0 : 18 - i, playTime: (18 - i) * 270,
                lastPlayed: new Date(2026, 8, 8, 20 - i),
                assets: mode === "noart" ? {} : {banner: Qt.resolvedUrl("assets/" + spec[1] + ".svg"), background: Qt.resolvedUrl("assets/" + spec[1] + ".svg"), boxFront: Qt.resolvedUrl("assets/" + spec[1] + "-poster.svg")},
                collections: modelFactory.createObject(mock, {items: [cs[i % 3]]}),
                files: modelFactory.createObject(mock, {items: [{path: "/preview/" + i + ".rom"}]})
            });
            gs.push(game);
        }
        if (mode === "long" && gs.length) {
            gs[0].title = "A Very Long Game Title: The Definitive Anniversary Collection and the Mystery of the Forgotten Kingdom";
            gs[0].description = Array(24).join("A lengthy description verifies scrolling and readability. ");
        }
        if (mode === "missing" && gs.length) gs[0].missing = true;
        for (var ci = 0; ci < cs.length; ++ci) {
            var group = [];
            for (var j = 0; j < gs.length; ++j) if (j % 3 === ci) group.push(gs[j]);
            cs[ci].games.items = group;
        }
        collections.items = total ? cs : [];
        allGames.items = gs;
    }
}
