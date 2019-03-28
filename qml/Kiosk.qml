import QtQuick 2.10
import QtQuick.Controls 2.12
import QtQuick.Controls.Material 2.12
import QtGraphicalEffects 1.12

import 'pages'

ApplicationWindow {
    id: main
    //width: 1024
    //height: 768

    font.pixelSize: Qt.application.font.pixelSize * 4

    //property alias current_number: numberForm.form_number

    title: 'settings.title'

//    background: Image {
//            anchors.fill: parent
//            fillMode: Image.PreserveAspectCrop
//            source: '/img/unsplash.jpg'
//    }

    Component.onCompleted: {
        // VirtualKeyboardSettings.activeLocales = ['en_US','ru_RU']
        main.showFullScreen()
        // main.showNormal()
        title = KioskSettings.title
    }



    MouseArea {
        anchors.fill: parent
        acceptedButtons: Qt.LeftButton
        pressAndHoldInterval: 30000
        cursorShape: Qt.CrossCursor
        onPressAndHold: { calibrator.timeout = 100}
    }

    StackView {
        id: stackView
        anchors.fill: parent
        initialItem: helloForm
        anchors.margins:  50

        onCurrentItemChanged: {
            //currentItem.forceActiveFocus()
            if(stackView.depth > 1) {
                stackTimer.restart()
            }
            else {
                stackTimer.stop()
            }
        }

    Hello {
        id: helloForm
    }

    Number {
        id: numberForm
    }

    Help {
        id: helpForm
    }

    Tickets {
        id: ticketsForm
    }

    }

    Timeout {
        id: stackTimer
        interval: 10
        hiddeninterval: 40
    }

    Touch {
        id: calibrator
    }

    Settings {
        id: settingsForm
    }

    Lock {
        id: kioskLock
        visible: false

        function showLock() {
            if (KioskPrinter.tcount > 1)
                visible = false
            else
                visible = true
        }

        Component.onCompleted: {
            KioskPrinter.on_counter.connect(showLock)
            showLock()
            console.log(KioskPrinter.tcount)
        }

    }

}

