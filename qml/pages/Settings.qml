import QtQuick 2.0
import QtQuick 2.10
import QtQuick.Controls 2.12
import QtQuick.Controls.Material 2.12
import QtQuick.Layouts 1.3

Page {
    id: settingsPage
    visible: false

    property alias loaded: loadedField.text
    property alias form_number: loadedField


    function accept() {
        KioskPrinter.feed_and_cut(loaded)
    }
    font.pixelSize: Qt.application.font.pixelSize * 2
    GridLayout {
        columns: 2
        rowSpacing: 22
        columnSpacing: 35


        Label {
            text: "Объект"
        }
        Label {
            text: KioskSettings.title
        }
        Label {
            text: "Идентификатор"
        }
        Label {
            text: KioskSettings.system_id
        }
        Label {
            text: "Напечатанно"
        }
        Label {
            text: KioskPrinter.pcount
        }
        Label {
            text: "Остаток"
        }
        TextField {
            id: loadedField
            text: KioskPrinter.tcount
            Layout.fillWidth: true
            Layout.maximumWidth: 500
        }
        Label {

        }
        GridLayout {


            Layout.maximumWidth: 500
            rows: 4
            columns: 3
            //height: parent.height - row.height

            Layout.fillWidth: true
            rowSpacing: 15
            columnSpacing: 15
            Layout.fillHeight: true
            Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter

            Repeater {
                model: 10
                delegate: Button {

                    Layout.fillHeight: true
                    Layout.fillWidth: true
                    font.pixelSize: Qt.application.font.pixelSize * 2
                    text: (index+1) % 10
                    onPressed:  {
                        var pos = form_number.cursorPosition
                        form_number.text = form_number.text.slice(0, pos)+ text + form_number.text.slice(pos)
                        form_number.cursorPosition = pos+1
                    }
                    onPressAndHold: {
                        if (index==9) {
                            var pos = form_number.cursorPosition
                            form_number.text = form_number.text.slice(0, pos-1)+ "#" + form_number.text.slice(pos)
                            form_number.cursorPosition = pos+1
                        }
                    }
                }

            }
            Button {
                Layout.fillHeight: true
                Layout.fillWidth: true
                Layout.columnSpan:2
                text: "←"
                onClicked: {
                    var pos = form_number.cursorPosition
                    form_number.text = form_number.text.slice(0, pos-1)+form_number.text.slice(pos)
                    form_number.cursorPosition = pos-1
                }
            }
        }




    }

    footer: DialogButtonBox {
        Button {
            text: qsTr("Сохранить")
            DialogButtonBox.buttonRole: DialogButtonBox.AcceptRole
            highlighted: true
            padding: 20
            enabled: loadedField.text
            icon.name : 'save'
            icon.height: 48
            icon.width: 48

        }

        ToolButton {
            text: qsTr("Отмена")
            DialogButtonBox.buttonRole: DialogButtonBox.RejectRole
            //highlighted: true
            padding: 20
        }

        background: Rectangle { color: "transparent" }

        font.pixelSize: Qt.application.font.pixelSize * 2
        onAccepted: settingsPage.accept()
        onRejected: {
             stackView.pop(null)
        }
    }
}
