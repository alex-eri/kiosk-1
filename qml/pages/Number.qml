import QtQuick 2.0
import QtQuick 2.10
import QtQuick.Controls 2.12
import QtQuick.Controls.Material 2.12
import QtQuick.Layouts 1.3

Page {
    id: numberForm
    visible: false

    property bool form_valid: false
    property alias form_number: numberField.text

    function accept(){
        if (form_number == "#07564") {
            stackView.push(settingsForm)
        } else {
            KioskPrinter.get(form_number, function(){
               stackView.push(ticketsForm);
            })
        }
    }

    background: Rectangle { color: "transparent" }

    footer: DialogButtonBox {
        Button {
            text: qsTr("Найти билет")
            DialogButtonBox.buttonRole: DialogButtonBox.AcceptRole
            highlighted: true
            padding: 20
            enabled:  form_valid
            icon.name : 'search'
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

        font.pixelSize: Qt.application.font.pixelSize * 3
        onAccepted: numberForm.accept()
        onRejected: {
             form_number = ''
             stackView.pop(null)
        }
    }

    ColumnLayout {
        spacing: 20
        anchors.fill: parent

        RowLayout {
            width: parent.width


            Layout.fillWidth: true
            spacing: 30
            Label {
                text: qsTr("Номер заказа")
            }
            TextField {
                id: numberField
                maximumLength: 12
                focus: false
                text: form_number
                Layout.fillWidth: true
                validator: RegExpValidator { regExp: /^[0-9\+\-\#\*\ ]{6,10}$/ }
                placeholderText: qsTr("введите номер")
                inputMethodHints: Qt.ImhDigitsOnly || Qt.ImhNone
                cursorVisible: true

                onAccepted: accept()

                onTextChanged: {
                    //numberField.forceActiveFocus()
                    KioskPrinter.error=''
                    stackTimer.restart()
                    form_valid = acceptableInput
                }

//                    EnterKeyAction.actionId: EnterKeyAction.Search
//                    EnterKeyAction.enabled:  acceptableInput || inputMethodComposing

                Button {
                    anchors.right: parent.right
                    background: Rectangle {color: 'transparent'}
                    text: "⌫"
                    onClicked: {
                        var pos = numberField.cursorPosition
                        form_number = form_number.slice(0, pos-1)+form_number.slice(pos)
                        numberField.cursorPosition = pos-1
                    }
                }
            }


        }
        Label {
            Layout.alignment: Qt.AlignHCenter | Qt.AlignVCenter

            id: numberError
            color: Material.color(Material.Red)
            text: KioskPrinter.error
            //visible: text.length>1
            font.pixelSize: Qt.application.font.pixelSize * 2
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
                    font.pixelSize: Qt.application.font.pixelSize * 5
                    text: (index+1) % 10
                    onPressed:  {
                        var pos = numberField.cursorPosition
                        form_number = form_number.slice(0, pos)+ text + form_number.slice(pos)
                        numberField.cursorPosition = pos+1
                    }
                    onPressAndHold: {
                        if (index==9) {
                            var pos = numberField.cursorPosition
                            form_number = form_number.slice(0, pos-1)+ "#" + form_number.slice(pos)
                            numberField.cursorPosition = pos+1
                        }
                    }
                }

            }
        }

    }
}
