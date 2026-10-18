import QtQuick 2.12
import Qt.labs.folderlistmodel 2.15
import "components"

FocusScope {
    id: root
    readonly property string refreshMemoryKey: "zaman.libraryRefreshToken"
    property bool refreshInitialized: false
    property string lastRefreshToken: ""
    readonly property string steamRefreshMemoryKey: "zaman.steamLibraryRefreshToken"
    property bool steamRefreshInitialized: false
    property string lastSteamRefreshToken: ""

    function inspectRefreshSignal() {
        // The sync helper briefly publishes two names while replacing a
        // signal. Wait for the single, stable entry before requesting a scan.
        if (refreshSignals.status !== FolderListModel.Ready || refreshSignals.count !== 1)
            return;

        var token = refreshSignals.get(0, "fileName");
        if (!refreshInitialized) {
            lastRefreshToken = api.memory.has(refreshMemoryKey)
                ? String(api.memory.get(refreshMemoryKey)) : "";
            refreshInitialized = true;
        }
        if (token === lastRefreshToken)
            return;

        lastRefreshToken = token;
        api.memory.set(refreshMemoryKey, token);
        refreshDebounce.restart();
    }

    function inspectSteamRefreshSignal() {
        // The sync helper briefly publishes two names while replacing a
        // signal. Wait for the single, stable entry before requesting a scan.
        if (steamRefreshSignals.status !== FolderListModel.Ready || steamRefreshSignals.count !== 1)
            return;

        var token = steamRefreshSignals.get(0, "fileName");
        if (!steamRefreshInitialized) {
            lastSteamRefreshToken = api.memory.has(steamRefreshMemoryKey)
                ? String(api.memory.get(steamRefreshMemoryKey)) : "";
            steamRefreshInitialized = true;
        }
        if (token === lastSteamRefreshToken)
            return;

        lastSteamRefreshToken = token;
        api.memory.set(steamRefreshMemoryKey, token);
        refreshDebounce.restart();
    }

    FolderListModel {
        id: refreshSignals
        folder: Qt.resolvedUrl("library-refresh")
        nameFilters: ["*.signal"]
        showDirs: false
        showDotAndDotDot: false
        onStatusChanged: root.inspectRefreshSignal()
        onCountChanged: root.inspectRefreshSignal()
    }

    FolderListModel {
        id: steamRefreshSignals
        folder: Qt.resolvedUrl("steam-library-refresh")
        nameFilters: ["*.signal"]
        showDirs: false
        showDotAndDotDot: false
        onStatusChanged: root.inspectSteamRefreshSignal()
        onCountChanged: root.inspectSteamRefreshSignal()
    }

    Timer {
        id: refreshPoll
        interval: 500
        repeat: true
        running: true
        onTriggered: { root.inspectRefreshSignal(); root.inspectSteamRefreshSignal(); }
    }

    Timer {
        id: refreshDebounce
        interval: 350
        repeat: false
        onTriggered: Internal.settings.reloadProviders()
    }

    Shell { anchors.fill: parent; backend: api; focus: true }
}
