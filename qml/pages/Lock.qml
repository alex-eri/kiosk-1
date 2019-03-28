import QtQuick 2.10
import QtQuick.Controls 2.12
import QtQuick.Controls.Material 2.12

Rectangle {
    property int hiddeninterval: 30
    property int interval: 10
    anchors.fill:parent
    color: "#80000000"
    Pane {
        width: parent.width/4*3
        height: parent.height/2

        anchors.centerIn: parent
        Material.elevation: 6

        background: Rectangle {
            color: Material.color(Material.Red)
        }

        Label {
            color: "#fff"
            font.pixelSize: Qt.application.font.pixelSize * 5
            text: qsTr("Терминал временно не работает")
            wrapMode: Label.WordWrap
            anchors.verticalCenter: parent.verticalCenter
            width: parent.width
            horizontalAlignment: Text.AlignHCenter
        }

    }
    MouseArea {
        anchors.fill:parent
        pressAndHoldInterval: 30000
        onPressAndHold: {
            parent.visible = false
        }
    }

}
