#include <FastLED.h>
#define LED_PIN                   7

#define NUM_LEDS                  50
#define TOTAL_UPDATES_STORED      7
#define MEMORY_PER_UPDATE        (NUM_LEDS * 3)
#define TOTAL_MEMORY             (TOTAL_UPDATES_STORED * MEMORY_PER_UPDATE)

#define UPDATES_PER_SECOND        5
#define UPDATE_DELAY             (1000 / UPDATES_PER_SECOND)

uint8_t secondsData[TOTAL_UPDATES_STORED * NUM_LEDS * 3];
CRGB leds[NUM_LEDS];

int idx = 0; // The idx of data we are playing
int loadedIdx = 0; // How much data we've loaded
int requestedIdx = 0; // How much data we've requested

bool start = false;

unsigned long lastUpdate;

void setup() {
  FastLED.addLeds<WS2812, LED_PIN, GRB>(leds, NUM_LEDS);
  Serial.begin(9600);
  lastUpdate = millis();
}

void requestData() {

  bool hasRoomForData = idx + ((TOTAL_UPDATES_STORED - 1) * NUM_LEDS * 3) >= requestedIdx;
  
  // If we have room for more data and the last request is complete, request more data
  if (hasRoomForData && requestedIdx == loadedIdx) {
    String dataRequest = "DATA " + String((requestedIdx / MEMORY_PER_UPDATE) + 1);
    Serial.println(dataRequest);
    requestedIdx += MEMORY_PER_UPDATE;
  }
}

void readData() {
  // Read data from serial
  while (Serial.available() > 0) {
    secondsData[loadedIdx % TOTAL_MEMORY] = Serial.read();
    loadedIdx++;
  }
}

bool started = false;
unsigned long startedTime;

void loop() {

  requestData();
  readData();

  if (loadedIdx >= TOTAL_MEMORY && millis() / UPDATE_DELAY > lastUpdate / UPDATE_DELAY) {

    if (!started) {
      Serial.println("START");
      started = true;
      lastUpdate = millis() + 400;
      return;
    }

    // Just turn off all lights if we've passed the loaded data
    // Allow it to catch up. This shouldn't happen, but allows me
    // to disable the program before the end of a song and not have
    // it flash random lights at me
    if (idx > loadedIdx) {
      for (int i = 0; i < NUM_LEDS; i++) {
        leds[i] = CRGB(0,0,0);
      }
      FastLED.show();
      return;
    }

    // Loop through data array to show data
    for (int i = 0; i < NUM_LEDS; i++) {
      leds[i] = CRGB(secondsData[(idx % TOTAL_MEMORY) + (i*3) + 0], 
                     secondsData[(idx % TOTAL_MEMORY) + (i*3) + 1],
                     secondsData[(idx % TOTAL_MEMORY) + (i*3) + 2]);
    }
    FastLED.show();
    
    idx += MEMORY_PER_UPDATE;
    lastUpdate += UPDATE_DELAY;
  }
}
