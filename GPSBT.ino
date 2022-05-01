#define _USE_MATH_DEFINES
#include <math.h>

#include <SoftwareSerial.h>

SoftwareSerial GPSSerial(9, 10); // RX, TX
#include <Adafruit_GPS.h>
  
#include <Adafruit_GPS.h>
#include <SoftwareSerial.h>

Adafruit_GPS GPS(&GPSSerial);

// Set GPSECHO to 'false' to turn off echoing the GPS data to the Serial console
// Set to 'true' if you want to debug and listen to the raw GPS sentences
#define GPSECHO false
// this keeps track of whether we're using the interrupt
// off by default!
boolean usingInterrupt = false;

uint32_t timer = millis();
float latitude;
float longitude;
char lat;
char lon;

float testlat[] = {
  36.13403869374745, //0: reynolda hall -- side stairs
  36.13407769957198, //1: reynolda hall -- top of stairs
  36.13390005112619, //2: reynolda hall -- front sidewalk
  36.133797722934105,//3: reynolda hall -- right out front
  36.13369730391507, //4: reynolda hall -- on location
  36.13581239439343, //5: wakerspace
  36.135299190856244 //6: chapel
  
};

float testlon[] = {
  80.27719713212093,
  80.27738731358706,
  80.27745337662266,
  80.27756664171382,
  80.27747768049953,
  80.28091585407873,
  80.27906573915102
};
int testlocation = 5;

float latitudes[] = {
  36.13369730391507, //reynolda hall
  36.137113596106744, //starbucks
  36.13550713600733, //gravel lot
  36.133478462875104 //manchester
};
float longitudes[] = {
  -80.27747768049953,
  -80.27952469795977,
  -80.28104438125831,
  -80.27649646356159
};
int numLocations = 4;
float threshold = 0.03;                                   //settings
float currDistance;

const int buzzer = 6;

void setup()
{
  pinMode(buzzer, OUTPUT); 
  Serial.begin(115200);
  GPS.begin(9600);
  delay(1000);
}


void loop() // run over and over again
{

  if (timer > millis()) timer = millis();
  // approximately every 2 seconds or so, print out the current stats
  if (millis() - timer > 5000) {
    timer = millis(); // reset the timer
    Serial.print("\nTime: ");
    Serial.print(GPS.hour, DEC); Serial.print(':');
    Serial.print(GPS.minute, DEC); Serial.print(':');
    Serial.print(GPS.seconds, DEC); Serial.print('.');
    Serial.println(GPS.milliseconds);
    Serial.print("Date: ");
    Serial.print(GPS.day, DEC); Serial.print('/');
    Serial.print(GPS.month, DEC); Serial.print("/20");
    Serial.println(GPS.year, DEC);
    Serial.print("Fix: "); Serial.print((int)GPS.fix);
    Serial.print(" quality: "); Serial.println((int)GPS.fixquality);
  
    Serial.print("Location: ,");
    latitude = GPS.latitude;
    longitude = GPS.longitude;
    lat = GPS.lat;
    lon = GPS.lon;
    Serial.print(GPS.latitude, 4); 
    Serial.print(", ");
    Serial.print(GPS.lat);
    Serial.print(", ");
    Serial.print(GPS.longitude, 4); 
    Serial.print(", ");
    Serial.println(GPS.lon);
   }  
   
   //start testing code for no GPS connection
   latitude = testlat[testlocation];
   longitude = testlon[testlocation];
   lat = 'N';
   lon = 'W';
   //end testing code

   Serial.println(latitude);
   Serial.println(lat);
   Serial.println(longitude);
   Serial.println(lon);
   if (lat == 'S'){
    latitude = -1*latitude;
   }
   if(lon == 'W'){
    longitude = -1*longitude;
   }

  Serial.println(latitude, 10);

   bool perimiter = checkDist(latitude, longitude);

   Serial.println(perimiter);
   if (perimiter){
    tone(buzzer, 1000); // Send 1KHz sound signal...
    delay(100);        // ...for 1 sec
    if (currDistance > 0){
      noTone(buzzer);
    }
    delay(currDistance*100000);
    Serial.println(currDistance, 4);
   }
  
  delay(100); 
}

bool checkDist(float currLat, float currLon){
  for (int i = 0; i<numLocations; i++){
    float dist = calcDist(currLat, currLon, i);
    if (dist <= threshold){
      currDistance = dist;
      return true;
    }
  }
  return false;
};

float calcDist(float currLat, float currLon, int loc){
  float lat1 = toRadians(latitudes[loc]);
  float long1 = toRadians(longitudes[loc]);
  float lat2 = toRadians(currLat);
  float long2 = toRadians(currLon);

  // Haversine Formula
  float dlong = long2 - long1;
  float dlat = lat2 - lat1;

  float ans = pow(sin(dlat / 2), 2) +
      cos(lat1) * cos(lat2) *
      pow(sin(dlong / 2), 2);

  ans = 2 * asin(sqrt(ans));

  // Radius of Earth in
  // Kilometers, R = 6371
  // Use R = 3956 for miles
  float R = 3956;

  // Calculate the result
  ans = ans * R;

  return ans;
};

float toRadians(const float degree)
{
    // cmath library in C++
    // defines the constant
    // M_PI as the value of
    // pi accurate to 1e-30
    float one_deg = (M_PI) / 180;
    return (one_deg * degree);
}
