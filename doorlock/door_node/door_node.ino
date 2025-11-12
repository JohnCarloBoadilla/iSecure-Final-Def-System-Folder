#include <WiFi.h>
#include <HTTPClient.h>
#include <SPI.h>
#include <MFRC522.h>

// ================================
// DOOR CONFIG
// ================================
#define DOOR_NAME "DOOR1"   // <-- Door this ESP32 controls (both entry + exit)

// ================================
// WIFI CONFIG
// ================================
const char* WIFI_SSID = "RensterSheymar2.4G";
const char* WIFI_PASS = "1720selaznog";
const char* SERVER_HOST = "192.168.100.21";
#define API_PATH "/doorlock/check.php"

// ================================
// RELAY (Active LOW)
// ================================
#define RELAY_PIN 22   // Active LOW relay

// ================================
// RFID Readers
// ================================
// Entrance Reader
#define SS_ENT   5
#define RST_ENT 27

// Exit Reader
#define SS_EXT   4
#define RST_EXT 26

MFRC522 readerEntry(SS_ENT, RST_ENT);
MFRC522 readerExit(SS_EXT, RST_EXT);

// ================================
// Indicators
// ================================

// Entrance indicators
#define LED_ENT_GREEN 13
#define LED_ENT_RED   14
#define BUZZ_ENT      12

// Exit indicators
#define LED_EXT_GREEN 25
#define LED_EXT_RED    2     // GPIO33 replaced with GPIO2
#define BUZZ_EXT      21

// Active high
const bool LED_ACTIVE_HIGH = true;
const bool BUZZER_ACTIVE_HIGH = true;

#define UNLOCK_MS 3000
#define REPEAT_SCAN_GUARD 1500
#define BEEP_SHORT 80
#define BEEP_LONG 300
#define GAP 80

String lastUID = "";
unsigned long lastReadTime = 0;

// ================================
// Helper Functions
// ================================
inline void writeLED(int pin, bool on) {
  digitalWrite(pin, (LED_ACTIVE_HIGH ? on : !on));
}

inline void writeBuzzer(int pin, bool on) {
  digitalWrite(pin, (BUZZER_ACTIVE_HIGH ? on : !on));
}

void indicatorsIdle() {
  writeLED(LED_ENT_GREEN, false);
  writeLED(LED_ENT_RED,   false);
  writeBuzzer(BUZZ_ENT,   false);

  writeLED(LED_EXT_GREEN, false);
  writeLED(LED_EXT_RED,   false);
  writeBuzzer(BUZZ_EXT,   false);
}

String uidToHex(MFRC522::Uid *uid) {
  String hex = "";
  for (byte i = 0; i < uid->size; i++) {
    if (uid->uidByte[i] < 16) hex += "0";
    hex += String(uid->uidByte[i], HEX);
  }
  hex.toUpperCase();
  return hex;
}

// ================================
// WIFI CONNECT
// ================================
void connectWiFi() {
  Serial.println("Connecting WiFi...");
  WiFi.begin(WIFI_SSID, WIFI_PASS);

  int tries = 0;
  while (WiFi.status() != WL_CONNECTED && tries < 40) {
    delay(250);
    Serial.print(".");
    tries++;
  }
  Serial.println();

  if (WiFi.status() == WL_CONNECTED) {
    Serial.println("✅ WiFi Connected");
    Serial.print("IP: ");
    Serial.println(WiFi.localIP());
  } else {
    Serial.println("❌ WiFi FAILED");
  }
}

// ================================
// Access Patterns
// ================================
void grantedEntrance() {
  for (int i = 0; i < 2; i++) {
    writeLED(LED_ENT_GREEN, true);
    writeBuzzer(BUZZ_ENT, true);
    delay(BEEP_SHORT);
    writeBuzzer(BUZZ_ENT, false);
    writeLED(LED_ENT_GREEN, false);
    delay(GAP);
  }
}

void rejectedEntrance() {
  writeLED(LED_ENT_RED, true);
  writeBuzzer(BUZZ_ENT, true);
  delay(BEEP_LONG);
  writeBuzzer(BUZZ_ENT, false);
  writeLED(LED_ENT_RED, false);
}

void grantedExit() {
  for (int i = 0; i < 2; i++) {
    writeLED(LED_EXT_GREEN, true);
    writeBuzzer(BUZZ_EXT, true);
    delay(BEEP_SHORT);
    writeBuzzer(BUZZ_EXT, false);
    writeLED(LED_EXT_GREEN, false);
    delay(GAP);
  }
}

void rejectedExit() {
  writeLED(LED_EXT_RED, true);
  writeBuzzer(BUZZ_EXT, true);
  delay(BEEP_LONG);
  writeBuzzer(BUZZ_EXT, false);
  writeLED(LED_EXT_RED, false);
}

// ================================
// API CALL
// ================================
bool callAPI(const String &uidHex, const String &doorName, String &statusOut, String &reasonOut) {
  statusOut = "REJECTED";
  reasonOut = "NO_HTTP";

  if (WiFi.status() != WL_CONNECTED) {
    connectWiFi();
    if (WiFi.status() != WL_CONNECTED) return false;
  }

  HTTPClient http;

  String url = "http://" + String(SERVER_HOST) + API_PATH +
               "?uid=" + uidHex +
               "&door=" + doorName;

  Serial.print("➡️ Sending: ");
  Serial.println(url);

  if (!http.begin(url)) return false;

  int code = http.GET();
  if (code <= 0) {
    http.end();
    return false;
  }

  String payload = http.getString();
  Serial.print("⬅️ Response: ");
  Serial.println(payload);

  // Simple extraction
  int sIdx = payload.indexOf("\"status\"");
  int sQ1 = payload.indexOf("\"", sIdx + 9);
  int sQ2 = payload.indexOf("\"", sQ1 + 1);
  if (sIdx >= 0 && sQ2 > sQ1) statusOut = payload.substring(sQ1 + 1, sQ2);

  int rIdx = payload.indexOf("\"reason\"");
  int rQ1 = payload.indexOf("\"", rIdx + 9);
  int rQ2 = payload.indexOf("\"", rQ1 + 1);
  if (rIdx >= 0 && rQ2 > rQ1) reasonOut = payload.substring(rQ1 + 1, rQ2);

  http.end();
  return true;
}

// ================================
// Door Unlock (Active LOW Relay)
// ================================
void unlockDoor() {
  Serial.println("✅ Unlocking...");

  digitalWrite(RELAY_PIN, LOW);  // ACTIVE LOW = ON

  writeLED(LED_ENT_GREEN, true);
  writeLED(LED_EXT_GREEN, true);

  delay(UNLOCK_MS);

  digitalWrite(RELAY_PIN, HIGH); // ACTIVE LOW = OFF

  writeLED(LED_ENT_GREEN, false);
  writeLED(LED_EXT_GREEN, false);

  Serial.println("🔒 Locked");
}

// ================================
// Handle Scan
// ================================
void handleScan(MFRC522 &reader, const String &doorName, bool isEntry) {
  String uidHex = uidToHex(&reader.uid);

  unsigned long now = millis();
  if (uidHex == lastUID && (now - lastReadTime) < REPEAT_SCAN_GUARD) return;

  lastUID = uidHex;
  lastReadTime = now;

  Serial.println("=================================");
  Serial.print("📌 Door: ");
  Serial.println(doorName);
  Serial.print("UID: ");
  Serial.println(uidHex);

  String status, reason;
  bool ok = callAPI(uidHex, doorName, status, reason);

  Serial.print("API: ");
  Serial.println(status);

  if (ok && status == "GRANTED") {
    if (isEntry) grantedEntrance();
    else grantedExit();
    unlockDoor();
  } else {
    if (isEntry) rejectedEntrance();
    else rejectedExit();
  }

  reader.PICC_HaltA();
  reader.PCD_StopCrypto1();
}

// ================================
// SETUP
// ================================
void setup() {
  Serial.begin(115200);

  pinMode(RELAY_PIN, OUTPUT);
  digitalWrite(RELAY_PIN, HIGH); // ACTIVE LOW RELAY = OFF

  pinMode(LED_ENT_GREEN, OUTPUT);
  pinMode(LED_ENT_RED,   OUTPUT);
  pinMode(BUZZ_ENT,      OUTPUT);

  pinMode(LED_EXT_GREEN, OUTPUT);
  pinMode(LED_EXT_RED,   OUTPUT);
  pinMode(BUZZ_EXT,      OUTPUT);

  indicatorsIdle();

  connectWiFi();

  SPI.begin();
  readerEntry.PCD_Init();
  readerExit.PCD_Init();

  Serial.println("✅ Door node initialized (Entry + Exit)");
}

// ================================
// LOOP
// ================================
void loop() {

  // Entrance Reader
  if (readerEntry.PICC_IsNewCardPresent() && readerEntry.PICC_ReadCardSerial()) {
    handleScan(readerEntry, DOOR_NAME, true);  // ENTRY SIDE
  }

  // Exit Reader
  if (readerExit.PICC_IsNewCardPresent() && readerExit.PICC_ReadCardSerial()) {
    handleScan(readerExit, DOOR_NAME, false); // EXIT SIDE
  }

  delay(20);
}