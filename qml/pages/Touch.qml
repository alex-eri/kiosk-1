import QtQuick 2.10
import QtQuick.Controls 2.12
import QtQuick.Controls.Material 2.12
import QtQuick.Layouts 1.3


Rectangle {
    visible: timeout > 0
    anchors.fill: parent

    property int timeout: 0
    property int tolerance: 20


    Image {
        source: (KioskSettings.n === 0)? '/img/pointA.svg':'/img/point.svg'
        sourceSize: Qt.size(calibrator.tolerance * 4,calibrator.tolerance * 4)
        x: parent.width/8 -  calibrator.tolerance * 2
        y: parent.height/8 -  calibrator.tolerance * 2
    }
    Image {
        source: (KioskSettings.n === 1) ? '/img/pointA.svg':'/img/point.svg'
        antialiasing: true
        sourceSize: Qt.size(calibrator.tolerance * 4,calibrator.tolerance * 4)
        x: parent.width - parent.width/8 -  calibrator.tolerance * 2
        y: parent.height/8 -  calibrator.tolerance * 2
    }
    Image {
        source: (KioskSettings.n === 2)? '/img/pointA.svg':'/img/point.svg'
        sourceSize: Qt.size(calibrator.tolerance * 4,calibrator.tolerance * 4)
        x: parent.width/8 -  calibrator.tolerance * 2
        y: parent.height -  parent.height/8 -  calibrator.tolerance * 2
    }
    Image {
        source: (KioskSettings.n === 3)? '/img/pointA.svg':'/img/point.svg'
        sourceSize: Qt.size(calibrator.tolerance * 4,calibrator.tolerance * 4)
        x: parent.width - parent.width/8 -  calibrator.tolerance * 2
        y: parent.height -  parent.height/8 -  calibrator.tolerance * 2
    }



    Timer {
        running: calibrator.timeout > 0
        interval: 500
        repeat: true
        onTriggered: {
            calibrator.timeout--
            if (calibrator.timeout == 0) KioskSettings.calibrateresetsaved()
        }
    }

    Rectangle {
        id: calCursor
        border.color: Material.color(Material.Blue)
        border.width: 1
        color: 'transparent'
        width: calibrator.tolerance * 2
        height: calibrator.tolerance * 2
        anchors.margins: - calibrator.tolerance
        radius: width/2
        x: mouseArea.mouseX - calibrator.tolerance
        y: mouseArea.mouseY - calibrator.tolerance
    }

    Column {
        x: 10
        y: 10
        Text {
            color: "gray"
            text: "
    1,2,3,4 - нажать и держать по углам
    5 - нажать и держать в любом месте, чтоб применить настройку
    6 - проверьте и нажмите сохранить"
        }

    }


    MouseArea {
        id: mouseArea
        anchors.fill: parent
        acceptedButtons: Qt.LeftButton
        cursorShape: Qt.CrossCursor
        pressAndHoldInterval: 500
        onPressAndHold: {
            KioskSettings.touch()
        }
    }

    Column {
        anchors.centerIn: parent
        width: 200

        Label {
            Layout.fillWidth: true
            text: KioskSettings.n+1
        }
        ProgressBar {
            value: calibrator.timeout
            to: 100
        }
        Button {
            width: 200
            highlighted: true
            text: qsTr("Сброс в железо")
            Material.accent: Material.Red
            font.pixelSize: Qt.application.font.pixelSize
            onClicked: {
                    KioskSettings.calibrateresetdefault()
                    calibrator.timeout = 100
            }
        }
        Button {
            width: 200
            highlighted: true
            text: qsTr("Сброс в сохранение")
            Material.accent: Material.Red
            font.pixelSize: Qt.application.font.pixelSize
            onClicked: {
                    KioskSettings.calibrateresetsaved()
                    calibrator.timeout = 100
            }
        }
        Button {
            width: 200
            highlighted: true
            enabled: KioskSettings.n > 4
            text: qsTr("Сохранить")
            font.pixelSize: Qt.application.font.pixelSize * 2
            onClicked: {
                    KioskSettings.calibratesave()
                    calibrator.timeout = 0
            }
        }

    }

}
