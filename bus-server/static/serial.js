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

  
}


async function readInto() {


  if (!port) {
    await getReader();
  }
  reader = port.readable.getReader({ mode: "byob" });


  const myStack = ["", "", "", "", "", "", "", ""];
  const fistHalfNull = (arr) => arr.slice(0, 4).every((e) => e == "FF");
  while (1) {
    const { value, done } = await reader.read(new Uint8Array(1));

    myStack.push(buf2hex(value.buffer).toUpperCase());

    if (myStack.length > 8) myStack.shift();


    if (fistHalfNull(myStack)) {
      console.log("Stream: " + myStack.join());
      break;
    }
  }
  reader.releaseLock()
  return myStack.slice(4, 8).join("");

}

function buf2hex(buffer) {
  // buffer is an ArrayBuffer
  return [...new Uint8Array(buffer)]
    .map((x) => x.toString(16).padStart(2, "0"))
    .join("");
}

document.getElementById("readtag").addEventListener("click", async () => {
  str = await readInto();

  document.getElementById("login_form_id").value = str;
  document.getElementById("login_form_key").value = str;
});
