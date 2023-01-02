/*
 * Web Serial API (Google Chrome)
 *
 * Useful information used to this implementation:
 * https://github.com/svendahlstrand/web-serial-api/
 * https://dev.to/unjavascripter/the-amazing-powers-of-the-web-web-serial-api-3ilc
 * https://github.com/rafaelaroca/web-serial-terminal
 *
 */

const connectButton = document.getElementById("SerialConnectButton");
let port;

if ("serial" in navigator) {
  connectButton.addEventListener("click", function () {
    if (port) {
      console.log("Disconnected from Serial Port");
      port.close();
      port = undefined;
      connectButton.innerText = "Connect";
    } else {
      connectButton.innerText = "Disconnect";
      getReader();
    }
  });

  connectButton.disabled = false;
} else {
  console.log(
    "<p>Support for Serial Web API not enabled. Please enable it using chrome://flags/ and enable Experimental Web Platform fetures</p>"
  );
}

let lineBuffer = "";
let latestValue = 0;

async function getReader() {
  port = await navigator.serial.requestPort({});
  var speed = 9600;
  await port.open({ baudRate: [speed] });

  connectButton.innerText = "Disconnect";
  console.log("Connected using Web Serial API");

  const textDecoder = new TextDecoderStream();
  const readableStreamClosed = port.readable.pipeTo(textDecoder.writable);
  const reader = textDecoder.readable.getReader();

  // Listen to data coming from the serial device.
  while (true) {
    const { value, done } = await reader.read();
    if (done) {
      // Allow the serial port to be closed later.
      reader.releaseLock();
      break;
    }
    // value is a string.
    console.log(value);
  }
}
