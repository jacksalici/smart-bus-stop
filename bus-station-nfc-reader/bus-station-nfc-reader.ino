//source https://www.diyengineers.com/2021/04/15/learn-how-to-read-an-rfid-tag-with-rc522-and-arduino/

#include <SPI.h> //for further details and other examples see: https://github.com/miguelbalboa/rfid
#include <MFRC522.h>
 
#define SS_PIN 10
#define RST_PIN 5
 
MFRC522 rfid(SS_PIN, RST_PIN); // Instance of the class
 
MFRC522::MIFARE_Key key; 
 
void setup() { 
  Serial.begin(9600);
  SPI.begin(); // Init SPI bus
  rfid.PCD_Init(); // Init RC522 
}
 
void loop() {
 
  // Reset the loop if no new card present on the sensor/reader. This saves the entire process when idle.
  if ( ! rfid.PICC_IsNewCardPresent())
    return;
 
  // Verify if the NUID has been readed
  if ( ! rfid.PICC_ReadCardSerial())
    return;
 
  MFRC522::PICC_Type piccType = rfid.PICC_GetType(rfid.uid.sak);
 
  printHex(rfid.uid.uidByte, rfid.uid.size);
 
  rfid.PICC_HaltA(); // Halt PICC
}
 
//Routine to dump a byte array as hex values to Serial. 
void printHex(byte *buffer, byte bufferSize) {
  for (int i = 0; i<4; i++)
    Serial.write(0xff);
  
  Serial.write(buffer, bufferSize);

  


}