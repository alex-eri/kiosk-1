import QtQuick 2.0
import QtQuick 2.10
import QtQuick.Controls 2.12
import QtQuick.Controls.Material 2.12
import QtQuick.Layouts 1.3
import QtGraphicalEffects 1.12

Page {


    background: Rectangle { color: "transparent" }

    visible: false


    ColumnLayout {

        spacing: 50
        anchors.fill: parent

        Label {
                //anchors.horizontalCenter: parent.horizontalCenter
                Layout.alignment: Qt.AlignHCenter
                color: Material.foreground
                //width: parent.width
                text: main.title
                //elide: Label.ElideRight
                //Layout.fillWidth: true
                horizontalAlignment: Text.AlignCenter
                //verticalAlignment: Qt.AlignTop
                layer.enabled: true
                layer.effect: Glow {

                    color: Material.background
                    radius: 8
                    samples: 17
                }

        }
        Item {
            Layout.fillHeight: true
        }

        Button {
            padding: 50
            Layout.fillWidth: true
            //font.pixelSize: Qt.application.font.pixelSize * 3

            id: numberButton
            width: parent.width
            text: qsTr("Распечатать билет")

            onClicked: {
                stackView.push(numberForm)
            }
            highlighted: true
        }

        Button {
            Layout.fillWidth: true
            //font.pixelSize: Qt.application.font.pixelSize * 3

            width: parent.width
            text: qsTr("Помощь")

            onClicked: {
                stackView.push(helpForm)
            }
        }

        Item {
            Layout.fillHeight: true
        }

    }
}

