import QtQuick 2.12
import "../components"

Item {
    id: preview
    width: 1920; height: 1080
    property string mode: "normal"
    property alias shell: shell
    property alias mock: mock
    property int escapedToHost: 0
    Keys.onPressed: function(event) {
        if (event.key === Qt.Key_Escape) {
            escapedToHost += 1;
            event.accepted = true;
        }
    }
    MockApi { id: mock }
    Component.onCompleted: { mock.populate(mode); shell.rebuild(); shell.forceActiveFocus(); }
    Shell { id: shell; anchors.fill: parent; backend: mock; focus: true }
}
