import QtQuick 2.0
import QtQuick 2.10
import QtQuick.Controls 2.12
import QtQuick.Controls.Material 2.12
import QtQuick.Layouts 1.3
import QtWebEngine 1.8


Page {

    background: Rectangle { color: "transparent" }

    anchors.margins: -50

    footer: DialogButtonBox {
        background: Rectangle { color: "transparent" }
        font.pixelSize: Qt.application.font.pixelSize * 3
        onRejected: {
             stackView.pop(null)
        }
        ToolButton {
            text: qsTr("Назад")
            DialogButtonBox.buttonRole: DialogButtonBox.RejectRole
            padding: 20
        }
    }

    visible: false

    property string link: "#"
    Flickable {
        id: helpFlick
        anchors.fill: parent
        WebEngineView {
            id: helpView
            anchors.fill: parent
            focus: false

            url: KioskSettings.help + helpForm.link
            onLoadingChanged: {
                  if (helpView.loadProgress == 100) {
                      helpView.runJavaScript(
                          "document.documentElement.scrollHeight;",
                          function (i_actualPageHeight) {
                              console.log(i_actualPageHeight)
                              helpFlick.contentHeight = Math.max (
                                  i_actualPageHeight, helpFlick.height);
                          })
                  }
              }
        }

    }


}

