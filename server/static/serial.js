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
let reader;

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
    const bufferSize = 1;

    port = await navigator.serial.requestPort({});

  connectButton.innerText = "Disconnect";
  console.log("Connected using Web Serial API");
  await port.open({ baudRate: 9600, bufferSize });

  reader = port.readable.getReader({ mode: "byob" });

  

  /*<
  let buffer = new ArrayBuffer(bufferSize);
  let bl = 0;
  let string = "";

  // Set `bufferSize` on open() to at least the size of the buffer.

  const reader = port.readable.getReader({ mode: "byob" });
  while (true) {
    const { value, done } = await reader.read(new Uint8Array(buffer));
    if (done) {
      break;
    }
    buffer = value.buffer;*/

  

  // Handle `value`.
}

async function readString() {
    let buffer = new ArrayBuffer(4);
  // Read the first 512 bytes.
  buffer = await readInto(reader, buffer);
  str = buf2hex(buffer).toUpperCase()
  console.log(str)
  return str
}

async function readInto(reader, buffer) {

  if (!port){
    await getReader()
  }  
  let offset = 0;
  while (offset < buffer.byteLength) {
    const { value, done } = await reader.read(new Uint8Array(buffer, offset));
    if (done) {
      break;
    }
    buffer = value.buffer;
    offset += value.byteLength;
  }
  return buffer;
}

function buf2hex(buffer) {
  // buffer is an ArrayBuffer
  return [...new Uint8Array(buffer)]
    .map((x) => x.toString(16).padStart(2, "0"))
    .join("");
}



document.getElementById("readtag").addEventListener("click", async ()=>{
    str = await readString()
    
    document.getElementById("login_form_id").value = str
    document.getElementById("login_form_key").value = str
})