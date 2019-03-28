import QtQuick 2.10
import QtQuick.Controls 2.12
import QtQuick.Controls.Material 2.12

Rectangle {
    property int hiddeninterval: 30
    property int interval: 10

    function restart() {
        console.log('timeout start')
        splashTimer.count=0
        stackTimer.restart()
    }

    function stop() {
        console.log('timeout stop')
        stackTimer.stop()
    }

    Timer {
        id: stackTimer
        interval: parent.hiddeninterval*1000;
        running: false
        onTriggered: {
            console.log('timeout')
            splashTimer.count = parent.interval
        }
    }

    Timer {
        property int count: 0
        id: splashTimer
        interval: 1000;
        repeat: true
        running: count > 0
        onTriggered: {
            count--
            if (count==0) {
                stackView.pop(null)
                numberForm.form_number = ''
                stackTimer.stop()
            }
        }
    }


    anchors.fill:parent
    visible: splashTimer.count > 0
    color: "#80000000"
    Pane {
        width: parent.width/4*3
        height: parent.height/2

        anchors.centerIn: parent
        Material.elevation: 6
        Row {
            anchors.centerIn: parent
            spacing: 30
            Label {
                width: font.pixelSize
                text: splashTimer.count
                horizontalAlignment: Text.AlignRight
                font.pixelSize: Qt.application.font.pixelSize * 8
                anchors.verticalCenter: parent.verticalCenter
            }

            Column{


                Label {
                    text: qsTr("Продолжить?")
                    anchors.horizontalCenter: parent.horizontalCenter
                }
                Label {
                    color: Material.color(Material.BlueGrey)
                    anchors.horizontalCenter: parent.horizontalCenter
                    text: qsTr("Коснитесь экрана")
                    font.pixelSize: Qt.application.font.pixelSize * 3
                }
            }
        }
    }
    MouseArea {
        anchors.fill:parent
        onClicked: {
            parent.restart()
        }
    }

}
