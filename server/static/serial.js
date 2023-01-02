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

async function getReader() {
  port = await navigator.serial.requestPort({});

  connectButton.innerText = "Disconnect";
  console.log("Connected using Web Serial API");
  const bufferSize = 1;
  let buffer = new ArrayBuffer(bufferSize);

  let string = ""

  // Set `bufferSize` on open() to at least the size of the buffer.
  await port.open({ baudRate: 9600, bufferSize });

  const reader = port.readable.getReader({ mode: "byob" });
  while (true) {
    const { value, done } = await reader.read(new Uint8Array(buffer));
    if (done) {
      break;
    }
    buffer = value.buffer;
    console.log(value)
    // Handle `value`.
    string += buf2hex(buffer);
    console.log(string)
  }
}

function buf2hex(buffer) { // buffer is an ArrayBuffer
    return [...new Uint8Array(buffer)]
        .map(x => x.toString(16).padStart(2, '0'))
        .join('');
  }
