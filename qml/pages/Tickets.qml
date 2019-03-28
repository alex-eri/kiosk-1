import QtQuick 2.10
import QtQuick.Controls 2.12
import QtQuick.Controls.Material 2.12
import QtGraphicalEffects 1.12
import QtQuick.Layouts 1.3

Page {
    visible: false
    background: Rectangle { color: "transparent" }

    Component {
            id: ticketDelegate
            Pane {
                Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
                font.pixelSize: Qt.application.font.pixelSize * 1
                Material.elevation: 4

                Column {
                    spacing: 10

                Label {
                    text: modelData.film
                    font.pixelSize: Qt.application.font.pixelSize * 2
                    wrapMode: Text.Wrap

                }
                Label { text: 'Цена: ' + modelData.price}

                Label { text: modelData.zal +" "+  modelData.seat}

                Label { text: 'Дата: '+modelData.data + ' Время: '+modelData.time}
                }
            }
        }




    Flickable {
        anchors.fill: parent
        //height: parent.header
        contentHeight: tickets_to_print_flow.height
        contentWidth:  parent.width
        Flow {
            id: tickets_to_print_flow
            spacing: 22
            width: parent.width
            Repeater {
                model: KioskPrinter.tickets
                delegate: ticketDelegate
            }
        }
    }

    Button {
        Material.elevation: 4
        Material.accent: Material.Red
        anchors.top: parent.top
        anchors.right: parent.right
        text: KioskPrinter.error
        visible: KioskPrinter.error
        highlighted: true
        DialogButtonBox.buttonRole: DialogButtonBox.HelpRole
        padding: 20
        Timer {
            id: longPressTimer

            interval: 10000 //your press-and-hold interval here
            repeat: false
            running: false

            onTriggered: {btnPrint.enabled=true}
        }

        onPressedChanged: {
            if ( pressed ) {
                longPressTimer.running = true;
            } else {
                longPressTimer.running = false;
            }
        }
    }

//    header: DialogButtonBox {

//        background: Rectangle { color: "transparent" }
//        font.pixelSize: Qt.application.font.pixelSize * 3
//        Button {
//            DialogButtonBox.buttonRole: DialogButtonBox.AcceptRole
//            highlighted: true
//            text: KioskPrinter.tickets.length
//            padding: 20
//        }

//        Label {
//                Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter
//                color: Material.color(Material.Red)
//                text: KioskPrinter.error
//                font.pixelSize: Qt.application.font.pixelSize * 2
//            }
//    }

    footer: DialogButtonBox {
        background: Rectangle { color: "transparent" }

        font.pixelSize: Qt.application.font.pixelSize * 3
        onAccepted: {
             btnPrint.enabled=false
             KioskPrinter.print(function(){
                 numberForm.form_number = ''
                 stackView.pop()
                 stackView.pop()
                 btnPrint.enabled=true
             })
        }
        onRejected: {
             numberForm.form_number = ''
             stackView.pop(null)
        }

        ToolButton {
            text: qsTr("Отмена")
            DialogButtonBox.buttonRole: DialogButtonBox.RejectRole
            padding: 20
        }

        Button {
            id: btnPrint
            text: 'Печать'
            icon.name : 'printer-symbolic'
            icon.height: 48
            icon.width: 48
            highlighted: true
            padding: 50
            DialogButtonBox.buttonRole: DialogButtonBox.AcceptRole
        }
    }

}
